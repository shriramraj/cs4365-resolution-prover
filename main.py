# main.py

import sys

def parse_clause(line):
    literals = set(line.strip().split())
    return frozenset(literals) if literals else None

def resolve(ci, cj):
    resolvents = []
    for li in ci:
        comp = li[1:] if li.startswith('~') else '~' + li
        if comp in cj:
            new_clause = (ci - {li}) | (cj - {comp})
            resolvents.append(frozenset(new_clause))
    return resolvents

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py inputfile")
        return

    input_file = sys.argv[1]
    
    # Determine output filename
    if '.' in input_file:
        base_name = input_file.rsplit('.', 1)[0]
        output_file = base_name + '.out'
    else:
        output_file = input_file + '.out'

    clauses = []
    parents = []
    clause_set = set()
    index_map = {}
    success = False

    # Read input
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():
                clause = parse_clause(line)
                if clause and clause not in clause_set:
                    index = len(clauses)
                    clauses.append(clause)
                    parents.append(set())
                    clause_set.add(clause)
                    index_map[clause] = index

    # Resolution loop
    new = True
    while new:
        new = False
        n = len(clauses)
        for i in range(n):
            for j in range(i+1, n):
                resolvents = resolve(clauses[i], clauses[j])
                for res in resolvents:
                    if not res:  # Empty clause found
                        clauses.append(res)
                        parents.append({i, j})
                        success = True
                        
                        # Write to output file
                        with open(output_file, 'w') as f:
                            for idx, clause in enumerate(clauses):
                                parent_str = "{" + ",".join(str(p+1) for p in parents[idx]) + "}" if parents[idx] else "{}"
                                literals = " ".join(sorted(clause)) if clause else "False"
                                f.write(f"{idx+1}. {literals} {parent_str}\n")
                            f.write(f"Size of final clause set: {len(clauses)}")
                        return
                    
                    if res not in clause_set:
                        new = True
                        index = len(clauses)
                        clauses.append(res)
                        parents.append({i, j})
                        clause_set.add(res)
                        index_map[res] = index

    # Failure case
    with open(output_file, 'w') as f:
        f.write("Failure\n")
        f.write(f"Size of final clause set: {len(clauses)}")

if __name__ == "__main__":
    main()
