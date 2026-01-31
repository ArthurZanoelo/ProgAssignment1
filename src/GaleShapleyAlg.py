import sys

# modes will be differentiated in the terminal with arguments
# simply writing "match" or "verify" to determine the mode
# important to note that verify requires both an input file and an output file
mode = sys.argv[1] if len(sys.argv) > 1 else "match"

# match mode

if mode == "match":

    lines = sys.stdin.read().splitlines()
    n = int(lines[0])
    hospitalPrefs = []
    studentPrefs = []

    # Iterate through hospital preferences
    # Each iteration we append a list ([1, 2, 3]) of the hospital's preferences
    # to the overall preferences list

    # Final prefs list should look like [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    for i in range(1, n + 1):
        # convert to 0-based indexing
        hospitalPrefs.append([int(x) - 1 for x in lines[i].split()])

    for i in range(n + 1, 2 * n + 1):
        # convert to 0-based indexing
        studentPrefs.append([int(x) - 1 for x in lines[i].split()])

    # Track hospitals that are matched
    # We know to stop when set length == total number of hospitals
    matchedHospitals = set()

    # -1 represents unmatched hospitals
    hospitalMatches = [-1] * n
    studentMatches = [-1] * n
    nextProposal = [0] * n

    # Precompute student rankings so comparisons are fast
    studentRank = [[0] * n for _ in range(n)]
    for s in range(n):
        for rank, h in enumerate(studentPrefs[s]):
            studentRank[s][h] = rank

    while len(matchedHospitals) < n:

        # Choose first free hospital
        currentHospital = None
        for i in range(n):
            if i not in matchedHospitals:
                currentHospital = i
                break

        # Choose student (next one on preference list)
        currentStudent = hospitalPrefs[currentHospital][nextProposal[currentHospital]]
        nextProposal[currentHospital] += 1

        # If student is free then match
        if studentMatches[currentStudent] == -1:
            hospitalMatches[currentHospital] = currentStudent
            studentMatches[currentStudent] = currentHospital
            matchedHospitals.add(currentHospital)

        # otherwise check if student prefers this hospital
        else:
            otherHospital = studentMatches[currentStudent]

            if studentRank[currentStudent][currentHospital] < studentRank[currentStudent][otherHospital]:

                # unmatch old hospital
                hospitalMatches[otherHospital] = -1
                matchedHospitals.remove(otherHospital)

                # match new hospital
                hospitalMatches[currentHospital] = currentStudent
                studentMatches[currentStudent] = currentHospital
                matchedHospitals.add(currentHospital)

    # print output in required format (1-based)
    for h in range(n):
        print(h + 1, hospitalMatches[h] + 1)


# verify mode
elif mode == "verify":

    if len(sys.argv) != 4:
        print("INVALID (usage: python GaleShapleyAlg.py verify instance.in output.out)")
        sys.exit()

    instance_file = sys.argv[2]
    output_file = sys.argv[3]

    # Here we will delete all new lines
    with open(instance_file) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    n = int(lines[0])

    hospitalPrefs = []
    studentPrefs = []

    for i in range (1, n + 1):
        hospitalPrefs.append([int(x) - 1 for x in lines[i].split()])

    for i in range(n + 1, 2 * n + 1):
        studentPrefs.append([int(x) - 1 for x in lines[i].split()])

    with open(output_file) as f:
        out_lines = [l.strip() for l in f.readlines() if l.strip()]

    # VALIDITY CHECK
    hospitalMatches = [-1] * n
    studentMatches = [-1] * n

    # Outputs created come with one new line
    if len(out_lines) != n:
        print("INVALID (wrong number of lines)")
        sys.exit()

    for line in out_lines:
        parts = line.split()
        if len(parts) != 2:
            print("INVALID (line is not two integers)")
            sys.exit()

        h, s = map(int, parts)
        h -= 1
        s -= 1

        if not (0 <= h < n and 0 <= s < n):
            print("INVALID (id out of range)")
            sys.exit()

        if hospitalMatches[h] != -1 or studentMatches[s] != -1:
            print("INVALID (duplicate match)")
            sys.exit()

        hospitalMatches[h] = s
        studentMatches[s] = h

    if -1 in hospitalMatches or -1 in studentMatches:
        print("INVALID (someone unmatched)")
        sys.exit()

    # STABILITY CHECK

    # Build student ranking
    studentRank = [[0] * n for _ in range(n)]
    for s in range (n):
        for rank, h in enumerate(studentPrefs[s]):
            studentRank[s][h] = rank

    # Check blocking pairs
    for h in range(n):
        assignedStudent = hospitalMatches[h]

        for s in hospitalPrefs[h]:

            # Stop once we hit their assigned partner
            if s == assignedStudent:
                break

            currentHospital = studentMatches[s]

            if studentRank[s][h] < studentRank[s][currentHospital]:
                print(f"UNSTABLE (blocking pair: hospital {h +1}, student {s + 1}")
                sys.exit()

    print("VALID STABLE")


else:
    print("INVALID (unknown mode, use 'match' or 'verify')")
    sys.exit()