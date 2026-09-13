"""Parser for .usmap type mappings, including the v4 layout Dawnwalker ships.

v4 differs from the widely documented v3 in two ways found by probing this file,
not from a spec:
  * enum entry count is uint16 (as v3 LargeEnums) and each entry is 12 bytes:
    int64 value followed by int32 name index. v3 wrote a bare int32 name index.
  * everything else matches v3.

Both were confirmed by round-tripping: the stride is the only one of nine
candidates under which the struct section that follows parses at all, and the
recovered enum entries read back as ACLCL_Lowest..ACLCL_MAX in order.
"""
import struct

MAGIC = 0x30C4

PROP_TYPES = [
    "Byte", "Bool", "Int", "Float", "Object", "Name", "Delegate", "Double",
    "Array", "Struct", "Str", "Text", "Interface", "MulticastDelegate",
    "WeakObject", "LazyObject", "AssetObject", "SoftObject", "UInt64",
    "UInt32", "UInt16", "Int64", "Int16", "Int8", "Map", "Set", "Enum",
    "FieldPath", "Optional", "Utf8Str", "AnsiStr",
]


class PropType:
    __slots__ = ("type", "inner", "value", "struct_name", "enum_name")

    def __init__(self, t):
        self.type = t
        self.inner = None
        self.value = None
        self.struct_name = None
        self.enum_name = None

    def __repr__(self):
        if self.type == "Struct":
            return "Struct(%s)" % self.struct_name
        if self.type == "Enum":
            return "Enum(%s:%r)" % (self.enum_name, self.inner)
        if self.type in ("Array", "Set", "Optional"):
            return "%s<%r>" % (self.type, self.inner)
        if self.type == "Map":
            return "Map<%r,%r>" % (self.inner, self.value)
        return self.type


class Prop:
    __slots__ = ("name", "schema_index", "array_size", "type")

    def __repr__(self):
        return "%s:%r" % (self.name, self.type)


class Struct:
    __slots__ = ("name", "super_name", "prop_count", "props")

    def __repr__(self):
        return "Struct(%s<-%s, %d props)" % (self.name, self.super_name, len(self.props))


class Usmap:
    def __init__(self, path):
        d = open(path, "rb").read()
        magic, ver = struct.unpack_from("<HB", d, 0)
        if magic != MAGIC:
            raise ValueError("not a .usmap (magic 0x%04X)" % magic)
        self.version = ver
        o = 3
        if ver >= 1:
            has_ver = struct.unpack_from("<i", d, o)[0]; o += 4
            if has_ver:
                o += 8
                ncust = struct.unpack_from("<i", d, o)[0]; o += 4
                o += ncust * 20 + 4
        method = d[o]; o += 1
        csize, dsize = struct.unpack_from("<2I", d, o); o += 8
        if method != 0:
            raise NotImplementedError("compressed usmap (method %d) not handled" % method)
        b = d[o:o + csize]

        p = 0
        n = struct.unpack_from("<I", b, p)[0]; p += 4
        self.names = []
        for _ in range(n):
            if ver >= 2:
                ln = struct.unpack_from("<H", b, p)[0]; p += 2
            else:
                ln = b[p]; p += 1
            self.names.append(b[p:p + ln].decode("utf-8", "replace")); p += ln

        self.enums = {}
        n = struct.unpack_from("<I", b, p)[0]; p += 4
        for _ in range(n):
            ni = struct.unpack_from("<i", b, p)[0]; p += 4
            cnt = struct.unpack_from("<H", b, p)[0] if ver >= 3 else b[p]
            p += 2 if ver >= 3 else 1
            entries = {}
            for _ in range(cnt):
                if ver >= 4:
                    val, eni = struct.unpack_from("<qi", b, p); p += 12
                else:
                    eni = struct.unpack_from("<i", b, p)[0]; p += 4
                    val = len(entries)
                entries[val] = self._n(eni)
            self.enums[self._n(ni)] = entries

        self.structs = {}
        n = struct.unpack_from("<I", b, p)[0]; p += 4
        for _ in range(n):
            s = Struct()
            ni, si = struct.unpack_from("<2i", b, p); p += 8
            s.name = self._n(ni)
            s.super_name = self._n(si)
            s.prop_count, nser = struct.unpack_from("<2H", b, p); p += 4
            s.props = []
            for _ in range(nser):
                pr = Prop()
                pr.schema_index = struct.unpack_from("<H", b, p)[0]; p += 2
                pr.array_size = b[p]; p += 1
                pni = struct.unpack_from("<i", b, p)[0]; p += 4
                pr.name = self._n(pni)
                pr.type, p = self._ptype(b, p)
                s.props.append(pr)
            self.structs[s.name] = s
        self.consumed = p
        self.total = len(b)

    def _n(self, i):
        return self.names[i] if 0 <= i < len(self.names) else None

    def _ptype(self, b, p):
        t = b[p]; p += 1
        pt = PropType(PROP_TYPES[t] if t < len(PROP_TYPES) else "Unknown%d" % t)
        if pt.type == "Enum":
            pt.inner, p = self._ptype(b, p)
            i = struct.unpack_from("<i", b, p)[0]; p += 4
            pt.enum_name = self._n(i)
        elif pt.type == "Struct":
            i = struct.unpack_from("<i", b, p)[0]; p += 4
            pt.struct_name = self._n(i)
        elif pt.type in ("Array", "Set", "Optional"):
            pt.inner, p = self._ptype(b, p)
        elif pt.type == "Map":
            pt.inner, p = self._ptype(b, p)
            pt.value, p = self._ptype(b, p)
        return pt, p

    def flat_props(self, name):
        """Global unversioned-header index -> Prop across inheritance.

        The current struct's properties occupy the first indices; its parent is
        offset by the current struct's *declared* property count, then that
        parent's parent is offset again, and so on.  This is intentionally
        derived-class-first.  CUE4Parse's mapping reader uses the same rule
        (try the current type, then recurse into its super with
        ``index - PropertyCount``).  Reversing this order makes deep data assets
        look plausible while shifting every value after their first child field.
        """
        out = {}
        offset = 0
        while name and name in self.structs:
            s = self.structs[name]
            for pr in s.props:
                out[offset + pr.schema_index] = pr
            offset += s.prop_count
            name = s.super_name
        return out
