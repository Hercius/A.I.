import copy

class Formula(object):
    def __init__(self):
        self.clauses = []
        self.model = []

    ## Read formula in DIMACS CNF format
    def readcnf(self,fp):
        raw = fp.readlines()
        lines = []
        for line in raw:
            line = line.strip()
            if line != "" and line[0] != 'c':
                lines.append(line);

        _,_,n,m = lines[0].split()
        n, m = int(n), int(m)
        del lines[0]
        
        self.clauses = [[]]*m

        for i in range(m):
            self.clauses[i] = list(map(int,lines[i].split(" ")[:-1]));

    ## Assign a variable to make lit true
    def assign(self,lit):
        ## Remove clauses satisfied when lit = true
        self.clauses = list(filter(lambda clause: lit not in clause,self.clauses))

        ## Remove false literals where -lit = false
        for i in range(len(self.clauses)): self.clauses[i] = [l for l in self.clauses[i] if l != -lit]

        ## Add lit to model
        self.model.append(lit);

    ## Find a unit clause
    def unit(self):
        if 1 in list(map(len,self.clauses)):
            return self.clauses[list(map(len,self.clauses)).index(1)][0];        
        else: return None

    ## Find a pure literal
    def pure(self):
        lits = set([lit for clause in self.clauses for lit in clause])
        for lit in lits:
            if -lit not in lits: return lit
        return None

    ## Is this formula a tautology? 
    def istrue(self):
        return len(self.clauses) == 0

    ## Is this formula a contradiction?
    def isfalse(self):
        return [] in self.clauses


class Solver(object):
    def __init__(self):
        self.nodes = 0

    ## Unit propagation
    def unit_propagation(self,F):
       E = F.unit() #finds all of the unit clauses
       while E is not None:
           F.assign(E)
           E = F.unit()
        
    ## Pure literal rule        
    def solve_pure_literals(self,F):
        
        P = F.pure()
        while P is not None:
            F.assign(P)
            P = F.pure()

        
    ## Pick literal to branch
    def dpll_branch(self,F):
        flat_list = []
        for sublist in F.clauses:
            for item in sublist:
                flat_list.append(item)
        M = max(set(flat_list), key = flat_list.count)
        return M
        
    ## Main DPLL routine
    def dpll(self,F):
        ## Add this call to search node counter
        self.nodes = self.nodes+1

        ## YOU FILL THE FOLLOWING IN        
        ## 1. Perform unit propagation
        ## 2. Apply pure literal rule
        ## 3. Check for satisfiability or contradiction (and return if necessary)
        ## 4. Pick the branching literal
        ## 5. Make recursive calls on branches (hint: make copies of F)
        self.unit_propagation(F)
        self.solve_pure_literals(F)
        if F.istrue():
            return True
        elif F.isfalse():
            return  False
        lit = self.dpll_branch(F)
        CopyOfFP = copy.deepcopy(F)
        CopyOfFN = copy.deepcopy(F)
        CopyOfFP.assign(lit)
        CopyOfFN.assign(-1*lit)
        return self.dpll(CopyOfFP) or self.dpll(CopyOfFN) 

    def solve(self,filename):
        ## Open file and read into formula structure
        fp = open(filename,'r')
        F = Formula()
        F.readcnf(fp)
        fp.close()
        
        ## Reset node counter
        self.nodes = 0

        ## Solve formula
        status = self.dpll(F)

        ## Output result
        print(filename,"\t",status,"\t",self.nodes)

s = Solver()
s.solve("/Users/Alex/Documents/A.I/lab5/Formulas/formula04.cnf")

