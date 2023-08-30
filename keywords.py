import re


_dic={
    "addn":[
        "sum",
        "total",
        "altogether",
        "more than",
        "greater than",
        "consecutive",
        "increased by",
        "plus",
        "gained",
        "added",
        "grew by",
        "older than",
        "farther than",
        "and"],

    "subs":[
        "difference",
        "gave",
        "gave away",
        "diminished by",
        "fewer than",
        "less than",
        "decreased by",
        "removed",
        "taken away",
        "lost",
        "minus",
        "subtracted from",
        "younger than"],

    "mul":[
        "product",
        "twice",
        "doubled",
        "tripled",
        "times",
        "multiplied by",
        "of"],

    "div":[
        "quotient",
        "divided by",
        "divided into",
        "quotient of",
        "shared equally",
        "in",
        "per"],

    "equn": [
        "Is",
        "Equal to",
        "was",
        "will be",
        "result in",
        "has a value of",
        "is the same as"]
}










































# pattern1 = r"^(solve|evaluate|calculate|compute|what is|equate) [(0-9)]+"
# pattern2 = r"\d+ [a-z ]+ \d+"

# text = "calculate 237 and 2358 and 235 in 56"

# if re.match(pattern1, text):
#     if len(re.findall(pattern2, text)) > 0:
#         text = replace_keywords(text)
#         print(text)




