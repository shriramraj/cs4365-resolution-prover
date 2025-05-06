import sys
import re

def resolve(clauseA, clauseB, clauses_set):
    clauseA_set = set(clauseA)
    clauseB_set = set(clauseB)
    for L in clauseA_set:
        neg_L = '~' + L if L[0] != '~' else L[1:]
        if neg_L in clauseB_set:
            resolvent = (clauseA_set - {L}) | (clauseB_set - {neg_L})
            if not resolvent:
                return False  # empty clause, meaning a contradiction
            if any(negated(r1, r2) for r1 in resolvent for r2 in resolvent if r1 < r2):
                continue  # skip cases of tautologies (always true)
            if resolvent in clauses_set:
                continue  # skip any duplicates
            return resolvent  # new resolvent
    return True  # no resolvent found, meaning no contradiction

def negated(lit1, lit2):
    return lit1 == ('~' + lit2) or lit2 == ('~' + lit1)

def main():
    clauses = []
    clauseNum = 1
    
    with open(sys.argv[1], 'r', errors='ignore') as input_file:
        clauses = [line.strip().split() for line in input_file if line.strip()]
    
    if not clauses:
        print("Empty input")
        sys.exit(1)
    
    # Last clause is the one to prove (negated for resolution proof)
    toProve = clauses.pop(-1)
    
    # Print initial clauses
    for cl in clauses:
        print(f"{clauseNum}. {' '.join(cl)} {{}}")
        clauseNum += 1
    
    # Negate the clause to prove
    toProve = [re.sub(r'~', '', c) if '~' in c else '~' + c for c in toProve]
    
    # Add negated literals as unit clauses
    for c in toProve:
        clauses.append([c])
        print(f"{clauseNum}. {c} {{}}")
        clauseNum += 1
    
    # Clause sets for efficient lookup
    clauses_set = {frozenset(cl) for cl in clauses}
    clauses = [set(cl) for cl in clauses]
    
    # Main resolver loop
    i = 0
    while i < len(clauses):
        for j in range(i):
            result = resolve(clauses[i], clauses[j], clauses_set)
            if result is False:
                print(f"{clauseNum}. Contradiction {{{i+1}, {j+1}}}")
                print("Valid")
                sys.exit(0)
            elif result is True:
                continue
            else:
                result = list(result)
                print(f"{clauseNum}. {' '.join(result)} {{{i+1}, {j+1}}}")
                clauseNum += 1
                clauses.append(result)
                clauses_set.add(frozenset(result))
        i += 1

if __name__ == "__main__":
    main()