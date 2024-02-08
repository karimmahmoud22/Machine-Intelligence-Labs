from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
                valid_values.append(value)
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i + 1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # Initialize variables, domains, and constraints
        problem.variables = []
        problem.domains = {}
        problem.constraints = []

        # General Steps:
        # loop on each letter in the output from the right to the left
        # for example: OUT ==> T, U, O
        # look if the 2 letters in the left are exist or not 
        # example: if there is 2 letters in the left for the charater 'T' ==> add carry C1
        # make the relation C0 + O + O = T + 10 * C1
        # in this case we need 3 binary constraints
        # 1- C0 with C0OO ==> first digit in C0OO = C0
        # 2- O with C0OO ==> second digit in C0OO = O
        # 3- O with C0OO ==> third digit in C0OO = O
        # in case of 2 letters in the left for the charater 'T' ==> add carry C1
        # example: C1T we need 2 binary constraints
        # 1- C1 with C1T ==> first digit in C1T = C1
        # 2- T with C1T ==> second digit in C1T = T    
        # append the characters close to each other in one string
        # example: C0OO & C1T
        # if they are 3 ==> the domain is from 0 to 199
        # if they are 2 ==> the domain is from 0 to 99
        # if they are 1 ==> the domain is from 0 to 9
        # if there is only one character in the left ==> make the character equal to the carry
        # example: C2 = O
        # if the LHS is zero and RHS is not zero or vice versa ==> add the previous carry to the LHS either 0 or 1
        # example: if LHS = 0 and RHS = 1 ==> add carry C0

        # Case study:
        # LHS0 = "Go"
        # LHS1 = "TO"
        # RHS = "OUT"

        # Equation: Go + TO = OUT
        # C0 + O + O = T + 10 * C1
        # C1 + G + T = U + 10 * C2
        # C2 = O
        
        # Variables:
        # 1- Carries  ==> for each output char
        # 2- C0.O.O, C1.G.T  ==> each 2 corresponding variables with the carry
        # 3- C1.T, C2.U ==> each output char with the carry
        
        # Constraints:
        # 1- C0OO & C1T where C0 + O + O = T + 10 * C1
        # 2- C1GT & C2U where C1 + G + T = U + 10 * C2
        # 3- C2 = O
        # 4- C0 with C0OO ==> first digit in C0OO = C0
        # 5- O with C0OO ==> second digit in C0OO = O
        # 6- 0 with C0OO ==> third digit in C0OO = O
        # 7- C1 with C1GT ==> first digit in C1GT = C1
        # 8- G with C1GT ==> second digit in C1GT = G
        # 9- T with C1GT ==> third digit in C1GT = T
        # 10- C1 with C1T ==> first digit in C1T = C1
        # 11- T with C1T ==> second digit in C1T = T
        # 12- C2 with C2U ==> first digit in C2U = C2
        # 13- U with C2U ==> second digit in C2U = U

        def add_variable_constraints(var_label, carry_label):
            nonlocal problem
            problem.variables.append(var_label)
            problem.variables.append(carry_label)
            problem.domains[var_label] = set(range(10))
            problem.domains[carry_label] = {0, 1}
            problem.constraints.append(BinaryConstraint(
                variables=(var_label, carry_label),
                condition=lambda v, c: v + c * 10
            ))

        def add_binary_constraint(variables, condition_lambda):
            nonlocal problem
            problem.variables.extend(variables)
            for variable in variables:
                problem.domains[variable] = set(range(10))
            problem.constraints.append(BinaryConstraint(
                variables=variables,
                condition=condition_lambda
            ))

        for char in (problem.LHS[0][0], problem.LHS[1][0], problem.RHS[0]):
            problem.constraints.append(UnaryConstraint(
                variable=char,
                condition=lambda c: c != 0
            ))

        for char in reversed(problem.RHS):
            if char in problem.LHS[0] and char in problem.LHS[1]:
                carry_label = f'C{len(problem.variables) // 2}'
                add_variable_constraints(char, carry_label)
                problem.constraints.append(UnaryConstraint(
                    variable=carry_label,
                    condition=lambda c: c,
                    relation=lambda c: c
                ))
            else:
                add_variable_constraints(char, None)

        for lhs_char, rhs_char in zip(problem.LHS[0], problem.LHS[1]):
            add_binary_constraint((lhs_char, rhs_char), lambda l, r: l - r)

        for i in range(len(problem.variables)):
            for j in range(i + 1, len(problem.variables)):
                problem.constraints.append(BinaryConstraint(
                    variables=(problem.variables[i], problem.variables[j]),
                    condition=lambda v1, v2: v1 != v2
                ))

        return problem

    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
