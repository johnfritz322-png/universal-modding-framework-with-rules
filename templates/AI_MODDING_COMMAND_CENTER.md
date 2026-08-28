# AI Modding Copy/Paste Command Center

Claude, Codex, ChatGPT, and GitHub shared workflow.

Use these workflow commands when the user's request matches the named task. Treat the user's current request as authoritative; these templates guide process and quality gates, but do not override specific user instructions.

## 1. Shared Workspace / Start Here

You are working in my shared GitHub modding workspace.

Repository:
https://github.com/johnfritz322-png/universal-modding-framework-with-rules

This repository is the single source of truth for all AI-assisted game modding work.

Before making any changes:
1. Read AGENTS.md.
2. Read the universal modding rules.
3. Read the relevant game-specific folder and rules.
4. Read the current project manifest for the mod you are working on.
5. Inspect the existing repository structure and working code before proposing changes.
6. Do not invent APIs, IDs, UUIDs, hooks, files, engine functions, or modding behavior.
7. Mark anything not verified as UNVERIFIED or NEEDS TESTING.
8. Preserve stable identifiers and working systems.
9. Make the smallest necessary change.
10. Do not rewrite working architecture just because you are uncertain.
11. Use a branch for meaningful changes whenever possible.
12. Commit changes clearly and preferably open a pull request instead of directly overwriting main.
13. Update the project manifest, changelog, sources, limitations, or test files whenever your work changes those areas.
14. Never claim something is working unless it has actually reached the relevant verified state such as compiled, loaded, tested in-game, or regression tested.
15. Treat the repository's current main branch as the stable baseline unless I explicitly tell you otherwise.

## 2. Start a New Feature

Read AGENTS.md, the relevant game-specific rules, and the current project manifest.

Inspect the existing project before making changes.

Propose the smallest verified implementation plan for this feature first. Map each requested feature to a real engine or modding-framework capability.

Do not invent APIs, IDs, hooks, files, engine behavior, or dependencies. Mark anything unresolved as UNVERIFIED or NEEDS TESTING.

Do not code until the implementation plan is grounded in the actual target game and current project architecture.

## 3. Reviewer - Check Another AI's Work

Review the latest branch or pull request in my shared modding repository.

First read AGENTS.md, the universal rules, the relevant game-specific rules, and the current project manifest.

Do not rewrite anything yet.

Inspect the actual changed files and review for:
- hallucinated APIs, IDs, UUIDs, hooks, or engine behavior
- unsupported assumptions
- conflicts with existing architecture
- unnecessary rewrites
- compatibility risks
- broken references or stable identifiers
- missing or incorrect dependencies
- missing tests
- weak error handling
- save or persistence risks
- violations of AGENTS.md

Separate findings into:
BLOCKER
IMPORTANT
MINOR
VERIFIED GOOD

For every issue, explain exactly why it matters and point to the exact file, function, record, or section involved.

Do not approve unless the repository rules are satisfied.

## 4. Fix Review Findings

Read the review findings on the current pull request.

Verify every reviewer claim before changing code.

Fix all valid BLOCKER and IMPORTANT issues using the smallest necessary changes.

Do not blindly follow an incorrect review.

Preserve stable IDs, working systems, and existing architecture unless evidence shows they must change.

Update tests, sources, limitations, project manifest, and changelog where relevant.

Push the fixes to the same branch and keep the existing pull request as the review thread.

## 5. Re-Review After Fixes

Re-review the updated pull request after the implementer addressed the previous findings.

First verify whether every prior BLOCKER and IMPORTANT issue was actually resolved.

Then inspect the new changes for regressions, new assumptions, compatibility problems, broken references, or violations of AGENTS.md.

Do not assume a fix is correct because the implementer says it is.

Report:
RESOLVED
STILL BLOCKING
NEW ISSUE
VERIFIED GOOD

Do not approve the pull request while any valid BLOCKER remains.

## 6. Research Before Coding

Research the exact game build, modding framework/toolchain, APIs, identifiers, limitations, persistence behavior, and known-working examples relevant to this feature.

Use primary or maintainer documentation and actual project/game files whenever possible.

Do not rely on AI memory as technical proof.

Add verified findings to the appropriate game-specific rules, sources, or limitations files in the repository.

Clearly label unresolved claims as UNVERIFIED or NEEDS TESTING.

Do not begin implementation until there is a defensible technical path.

## 7. Compare Two Implementations

Compare the two proposed implementations against:

- AGENTS.md
- verified engine support
- compatibility risk
- amount of vanilla behavior replaced
- maintainability
- testability
- save/persistence safety
- dependency burden
- rollback difficulty
- impact on existing working systems

Do not choose based on which solution is more clever or has more code.

Prefer the smallest, most compatible, most verifiable implementation.

Explain which approach you recommend and why, and identify any remaining UNVERIFIED assumptions.

## 8. Debug a Broken Mod

Inspect the current project and read the actual compiler output, game logs, mod-loader logs, validator output, or crash information before changing code.

Identify the failing subsystem and likely root cause.

Do not repeatedly guess.
Do not rewrite unrelated working systems.
Do not regenerate stable IDs.
Do not suppress meaningful errors just to make the build appear successful.

Make the smallest evidence-based fix possible.

After the change, state exactly what has been verified: generated, compiled, validated, loaded, tested in-game, or regression tested.

## 9. Prepare an In-Game Test

Prepare a precise in-game test plan for the current feature.

Include:
- required game version and mod/tool versions
- required save/profile or whether a fresh save is needed
- exact setup steps
- exact action I should perform
- expected result
- failure symptoms to watch for
- relevant logs to collect if it fails
- rollback point

Do not mark the feature TESTED IN-GAME until I actually report the result.

## 10. Record a Successful Test

I have successfully tested this feature in-game.

Update the project manifest and related documentation to reflect the highest verified state supported by my test.

Record:
- what feature was tested
- game version/build
- relevant mod-loader/tool versions
- test conditions
- successful result
- remaining limitations
- known-good commit or branch state

Do not upgrade unrelated features to TESTED IN-GAME unless they were part of this test.

## 11. Pre-Merge Final Check

Perform a final pre-merge audit of the current pull request.

Confirm:
- all valid BLOCKER findings are resolved
- IMPORTANT findings are resolved or explicitly accepted
- tests are documented
- stable IDs and references were preserved
- no unnecessary architecture rewrite occurred
- dependencies are verified
- manifest is current
- changelog is current
- source/limitations files are current
- rollback point exists
- the PR does not claim a higher verification state than the evidence supports

If any merge blocker remains, say DO NOT MERGE and explain exactly why.

Otherwise say READY TO MERGE and summarize the verified state.
