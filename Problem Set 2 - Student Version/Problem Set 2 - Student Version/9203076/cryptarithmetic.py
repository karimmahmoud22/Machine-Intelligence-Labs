from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

def check_equal(lhs, rhs):
    sum_1 = 0
    sum_2 = 0
    for i in range(3):
        sum_1 += lhs % 10
        lhs = lhs // 10
        
    sum_2 += rhs % 10
    sum_2 += (rhs // 10) * 10
    
    return sum_1 == sum_2

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        
        # ==> Variables 

        # Set of variables
        variables_set = set()

        # Determine the maximum length of LHS and RHS
        max_length = max(len(problem.LHS[0]), len(problem.LHS[1]))

        # Update the variables set with individual characters from LHS and RHS
        variables_set.update([char for char in problem.LHS[0]])
        variables_set.update([char for char in problem.LHS[1]])
        variables_set.update([char for char in problem.RHS])
        variables_set.update([f"c_{i}" for i in range(max_length + 1)])

        # Generate variables for constraints involving digits at specific positions
        for i in range(max_length):
            lhs1 = '' if i >= len(problem.LHS[0]) else problem.LHS[0][-1 - i]
            lhs2 = '' if i >= len(problem.LHS[1]) else problem.LHS[1][-1 - i]
            rhs = '' if i >= len(problem.RHS) else problem.RHS[-1 - i]
            
            variables_set.add(f"${i}{lhs1}{lhs2}")
            variables_set.add(f"#{i + 1}{rhs}")

        # Update the problem's variables with the unique set
        problem.variables = list(variables_set)


        # ==> Domains 

        # Initialize domains for each character in LHS and RHS
        # Set domains for characters in LHS and RHS
        for i in range(max_length):
            
            if i < len(problem.LHS[0]): problem.domains[problem.LHS[0][-1 - i]] = set(range(10))
            
            if i < len(problem.LHS[1]): problem.domains[problem.LHS[1][-1 - i]] = set(range(10))
            
            if i < len(problem.RHS): problem.domains[problem.RHS[-1 - i]] = set(range(10))

        # Set domains for additional characters in RHS (if any)
        for i in range(max_length, len(problem.RHS), 1):
            problem.domains[problem.RHS[-1 - i]] = set(range(10))

        # Set specific domains for "$" and "#" variables
        # "$" variables can have values in the range [0, 99]
        problem.domains["c_0"] = {0}
        for var in problem.variables:
            
            if var.startswith("c_") and not var.startswith("c_0"): problem.domains[var] = {0, 1}
            
            if var.startswith("$") or var.startswith("#"): problem.domains[var] = set(range(pow(10, len(var) - 2) * 2))


        # ==>  Constraints 

        # Unary constraints to ensure the first character of LHS and RHS is not zero
        problem.constraints.append(UnaryConstraint(problem.LHS[0][0], lambda x: x != 0))
        problem.constraints.append(UnaryConstraint(problem.LHS[1][0], lambda x: x != 0))
        problem.constraints.append(UnaryConstraint(problem.RHS[0], lambda x: x != 0))

        # ==> Binary constraints for additional characters in RHS (if any)
        # ==> Ensure the first character of RHS is not zero
        # ==> Ensure the length of RHS is equal to the maximum length of LHS
        # ==> Ensure the last character of RHS is not zero (if RHS is longer than LHS)
        # ==> Ensure the last character of RHS is zero (if RHS is shorter than LHS)
        if len(problem.RHS) > max_length:
            problem.constraints.append(BinaryConstraint((problem.RHS[0], f"c_{max_length}"), lambda x, y: x == y))
            problem.constraints.append(UnaryConstraint(problem.RHS[0], lambda x: x != 0))
            problem.constraints.append(UnaryConstraint(f"c_{max_length}", lambda x: x != 0))
        else:
            problem.constraints.append(UnaryConstraint(f"c_{max_length}", lambda x: x == 0))

        # Binary constraints to ensure different characters in variables
        for i in range(len(problem.variables)):
            for j in range(i + 1, len(problem.variables), 1):
                
                if len(problem.variables[i]) == len(problem.variables[j]) == 1:
                    problem.constraints.append(BinaryConstraint((problem.variables[i], problem.variables[j]), lambda x, y: x != y))

        # Binary constraints to ensure the sum of digits in LHS and RHS is equal
        for var in problem.variables:
            
            if var.startswith("$") or var.startswith("#"):
                
                if len(var) - 2 == 2:
                    problem.constraints.append(BinaryConstraint((var, var[2]), lambda x, y: (x // 10) % 10 == y))
                    problem.constraints.append(BinaryConstraint((var, var[3]), lambda x, y: (x // 1) % 10 == y))
                    problem.constraints.append(BinaryConstraint((var, f"c_{var[1]}"), lambda x, y: (x // 100) == y))
                
                if len(var) - 2 == 1:
                    problem.constraints.append(BinaryConstraint((var, var[2]), lambda x, y: (x // 1) % 10 == y))
                    problem.constraints.append(BinaryConstraint((var, f"c_{var[1]}"), lambda x, y: (x // 10) == y))

        # Binary constraints to check equality for characters at corresponding positions
        for i in range(max_length):
            
            lhs1 = '' if i >= len(problem.LHS[0]) else problem.LHS[0][-1 - i]
            lhs2 = '' if i >= len(problem.LHS[1]) else problem.LHS[1][-1 - i]
            
            rhs = '' if i >= len(problem.RHS) else problem.RHS[-1 - i]
            
            _lhs = f"${i}{lhs1}{lhs2}"
            _rhs = f"#{i + 1}{rhs}"
            
            problem.constraints.append(BinaryConstraint((_lhs, _rhs), lambda x, y: check_equal(x, y)))
        
        # return the problem
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())