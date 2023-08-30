import re


import keywords

class equtionCleaner:
    equation:str = ''

    def __init__(self, equation:str):
        self.equation = equation
        self.equation = self.remove_spaces(self.equation)
        self.equation = self.insert_asterix_symbole(self.equation)


    def remove_spaces(self, equation:str):
        equation = equation.replace(' ', '')
        return equation


    def insert_asterix_symbole(self, equation:str):
        pattern = r"[0-9)]\("
        pattern_match = re.findall(pattern, equation)
        for x in pattern_match:
            equation = equation.replace(x, "*".join(x))
        return equation


def replace_keywords(equation:str):
        operations = keywords._dic

        for addn in operations["addn"]:
            if addn in equation:
                equation = equation.replace(addn, "+")
        
        for subs in operations["subs"]:
            if subs in equation:
                equation = equation.replace(subs, "-")

        for mul in operations["mul"]:
            if mul in equation:
                equation = equation.replace(mul, "*")

        for div in operations["div"]:
            if div in equation:
                equation = equation.replace(div, "/")

        return equation