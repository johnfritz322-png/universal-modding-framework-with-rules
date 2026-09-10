"""Decode UE5 unversioned property serialization using a .usmap schema.

Cooked UE5 packages drop property names and types from the stream; only a
compact header of "skip N, then N values" fragments remains. Reading anything
back requires the schema from a .usmap, matched by schema index.
"""
import struct


class Reader:
    def __init__(self, buf, pos=0):
        self.b = buf
        self.o = pos

    def u8(self):
        v = self.b[self.o]; self.o += 1; return v

    def u16(self):
        v = struct.unpack_from("<H", self.b, self.o)[0]; self.o += 2; return v

    def i32(self):
        v = struct.unpack_from("<i", self.b, self.o)[0]; self.o += 4; return v

    def u32(self):
        v = struct.unpack_from("<I", self.b, self.o)[0]; self.o += 4; return v

    def i64(self):
        v = struct.unpack_from("<q", self.b, self.o)[0]; self.o += 8; return v

    def f32(self):
        v = struct.unpack_from("<f", self.b, self.o)[0]; self.o += 4; return v

    def f64(self):
        v = struct.unpack_from("<d", self.b, self.o)[0]; self.o += 8; return v

    def fstring(self):
        n = self.i32()
        if n == 0:
            return ""
        if n < 0:
            raw = self.b[self.o:self.o - 2 * n - 2]; self.o += -2 * n
            return raw.decode("utf-16-le", "replace")
        raw = self.b[self.o:self.o + n - 1]; self.o += n
        return raw.decode("utf-8", "replace")


def read_header(r):
    """FUnversionedHeader -> list of (schema_index, has_value)."""
    frags = []
    while True:
        packed = r.u16()
        # FFragment::Unpack - SkipNum 0x007F, HasZero 0x0080, IsLast 0x0100,
        # ValueNum >> 9. Note IsLast is bit 8, NOT bit 15.
        skip = packed & 0x007F
        has_zeroes = bool(packed & 0x0080)
        is_last = bool(packed & 0x0100)
        count = packed >> 9
        frags.append((skip, has_zeroes, count))
        if is_last:
            break
    zero_num = sum(c for _, hz, c in frags if hz)
    zero_mask = []
    if zero_num:
        if zero_num <= 8:
            bits, width = r.u8(), 8
        elif zero_num <= 16:
            bits, width = r.u16(), 16
        else:
            words = (zero_num + 31) // 32
            bits = 0
            for i in range(words):
                bits |= r.u32() << (32 * i)
            width = words * 32
        zero_mask = [(bits >> i) & 1 for i in range(width)]
    out = []
    schema_i = 0
    zi = 0
    for skip, hz, count in frags:
        schema_i += skip
        for _ in range(count):
            if hz:
                is_zero = bool(zero_mask[zi]); zi += 1
                out.append((schema_i, not is_zero))
            else:
                out.append((schema_i, True))
            schema_i += 1
    return out


class Decoder:
    def __init__(self, usmap, names):
        self.m = usmap
        self.names = names

    def name(self, r):
        idx = r.u32(); num = r.u32()
        base = self.names[idx] if 0 <= idx < len(self.names) else "?%d" % idx
        return base if num == 0 else "%s_%d" % (base, num - 1)

    def value(self, r, pt):
        t = pt.type
        if t == "Bool":
            return None            # value lives in the header's zero mask
        if t in ("Int", "Int32"):
            return r.i32()
        if t == "UInt32":
            return r.u32()
        if t == "Float":
            return r.f32()
        if t == "Double":
            return r.f64()
        if t in ("Int64", "UInt64"):
            return r.i64()
        if t in ("Int16", "UInt16"):
            v = r.u16(); return v
        if t in ("Byte", "Int8"):
            return r.u8()
        if t == "Name":
            return self.name(r)
        if t == "Str":
            return r.fstring()
        if t == "Text":
            return self.text(r)
        if t == "Object":
            return r.i32()          # FPackageIndex
        if t in ("SoftObject", "AssetObject"):
            pkg = self.name(r)
            asset = self.name(r)
            sub = r.fstring()
            path = pkg if not asset or asset == "None" else "%s.%s" % (pkg, asset)
            return path + ("#" + sub if sub else "")
        if t == "Enum":
            idx = r.u8() if pt.inner and pt.inner.type == "Byte" else r.i32()
            table = self.m.enums.get(pt.enum_name or "", {})
            return table.get(idx, idx)
        if t == "Struct":
            return self.struct(r, pt.struct_name)
        if t in ("Array", "Set"):
            n = r.i32()
            return [self.value(r, pt.inner) for _ in range(n)]
        if t == "Map":
            n = r.i32()
            return [(self.value(r, pt.inner), self.value(r, pt.value)) for _ in range(n)]
        raise NotImplementedError("property type %s" % t)

    # Structs whose C++ type provides its own binary serializer, so they write
    # raw fields instead of an unversioned property header. Anything NOT in here
    # -- GameplayTag included -- writes a normal header and goes through props().
    NATIVE_STRUCTS = {
        "Guid": 16, "Vector": 24, "Vector2D": 16, "Vector4": 32, "Rotator": 24,
        "Quat": 32, "Color": 4, "LinearColor": 16, "IntPoint": 8, "IntVector": 12,
        "Box": 52, "Box2D": 36, "DateTime": 8, "Timespan": 8, "FrameNumber": 4,
    }

    def text(self, r):
        """FText: flags, then a history type that selects the payload."""
        r.u32()                          # flags
        history = struct.unpack_from("<b", r.b, r.o)[0]; r.o += 1
        if history == -1:                # None
            if r.i32():                  # bHasCultureInvariantString
                return r.fstring()
            return ""
        if history == 0:                 # Base: namespace, key, source
            r.fstring()
            key = r.fstring()
            src = r.fstring()
            return src or key
        if history == 11:                # StringTableEntry: table id + key
            table = self.name(r)
            key = r.fstring()
            return "%s[%s]" % (table.split("/")[-1], key)
        raise NotImplementedError("FText history type %d" % history)

    def struct(self, r, struct_name):
        n = self.NATIVE_STRUCTS.get(struct_name)
        if n is not None:
            raw = r.b[r.o:r.o + n]; r.o += n
            return raw.hex()
        if struct_name not in self.m.structs:
            raise NotImplementedError("no schema for struct %s" % struct_name)
        return self.props(r, struct_name)

    def props(self, r, struct_name):
        schema = self.m.flat_props(struct_name)
        out = {}
        for idx, has_value in read_header(r):
            pr = schema.get(idx)
            if pr is None:
                raise KeyError("schema index %d not in %s" % (idx, struct_name))
            if pr.type.type == "Bool":
                out[pr.name] = has_value
                continue
            if not has_value:
                out[pr.name] = None
                continue
            out[pr.name] = self.value(r, pr.type)
        return out
