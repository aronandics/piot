import subprocess, os, sys

files = {}
dependencies = longest = passed = failed = skipped = prevstate = i = 0
print("Gathering files...")
for file in os.listdir("tests"):
    name = file.rsplit(".", 1)[0]
    if name == "":
        if file == ".dependencies":
            with open("tests/.dependencies", "r") as f:
                dependencies = f.read()
        continue
    if name not in files:
        files[name] = {"done": 0}
    if name + ".out" == file:
        files[name]["out"] = file
    else:
        files[name]["in"] = file
    if len(name) > longest:
        longest = len(name)

if dependencies:
    print("Adding dependencies...")
    for dep in dependencies.splitlines():
        dep = dep.replace(" ", "").split(":", 1)
        dept = dep[0]
        deps = dep[1].split(",")
        if dept in deps:
            print("Error: " + dept + " depends itself.")
            exit()
        if dept in files:
            files[dept]["deps"] = deps

fns = list(files.keys())
print("-" * (longest + 19))
while len(files) > passed + failed + skipped:
    if i == len(files):
        done = passed + failed + skipped
        if done == prevstate:
            print(
                "Found \033[43mCIRCULAR DEPENDENCY\033[49m in "
                + ("remaining " if done > 0 else "all ")
                + str(len(files) - done)
                + " tests."
            )
            break
        i = 0
        prevstate = done
    file = fns[i]
    i += 1
    if files[file]["done"] != 0:
        continue
    if "in" not in files[file] or "out" not in files[file]:
        print(
            "Skipping %s\033[43mCANCEL\033[49m (missing %s"
            % (
                file + (" " * (longest + 4 - len(file))),
                ("input)" if "out" in files[file] else "output)"),
            )
        )
        files[file]["done"] = -1
        skipped += 1
        continue
    if "deps" in files[file]:
        for dep in files[file]["deps"]:
            if dep not in files or files[dep]["done"] == -1:
                print(
                    "Can't run %s\033[43mCANCEL\033[49m (%s"
                    % (
                        file + (" " * (longest + 3 - len(file))),
                        dep + (" failed)" if dep in files else " not found)"),
                    )
                )
                files[file]["done"] = -1
                skipped += 1
                break
            if files[dep]["done"] == 0:
                files[file]["done"] = 2
                break
        if files[file]["done"] != 0:
            if files[file]["done"] == 2:
                files[file]["done"] = 0
            continue
    sys.stdout.write("Testing " + file + "..." + (" " * (longest + 2 - len(file))))
    sys.stdout.flush()
    out = subprocess.check_output(
        sys.argv[1:] + ["tests/" + files[file]["in"]]
    ).splitlines()
    with open("tests/" + files[file]["out"], "r") as f:
        exp = f.read().splitlines()
        line = 0 if len(out) == len(exp) else -1
        for l in range(min(len(out), len(exp))):
            if out[l].decode() != exp[l]:
                line = l + 1
                break
        if line == 0:
            print("\033[42mPASSED\033[49m")
            files[file]["done"] = 1
            passed += 1
        else:
            print(
                "\033[41mFAILED\033[49m "
                + (
                    "at line " + str(line)
                    if line > 0
                    else "expected "
                    + ("more" if len(out) < len(exp) else "less")
                    + " output"
                )
            )
            files[file]["done"] = -1
            failed += 1

print("-" * (longest + 19))
print(
    "SUMMARY: \033[4%dm%d / %d\033[49m passed (%d failed, %d skipped)"
    % (
        2 if passed == len(files) else 3 if passed == len(files) - 1 else 1,
        passed,
        len(files),
        failed,
        skipped,
    )
)
