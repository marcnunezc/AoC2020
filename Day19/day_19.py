lines_list =open("test2.txt").read().splitlines()
import copy
rules = {}
i=0
while lines_list[i] != "":
    key, value = lines_list[i].split(": ")
    if "\"" in value:
        rules[key] = value.replace("\"","")
    else:
        rules[key] = [rule.split(" ") for rule in value.split(" | ")]
    i += 1
i += 1

def get_length(rule_key):
    length = 0
    for rule in rules[rule_key][0]:
        if rule.isdigit():
            length += get_length(rule)
        else:
            return 1
    return length

def check_sub_rule(line, subrule):
    if isinstance(rules[subrule], list):
        return check_rule(line, subrule)
    else:
        return line==rules[subrule]

def check_rule(line, rule_key):
    if not sum(get_length(rule) for rule in rules[rule_key][0]) == len(line):
        return False
    rule_check = False
    starting_length = 0
    for rule in rules[rule_key]:
        starting_sub_length = starting_length
        sub_rule_check = True
        for subrule in rule:
            this_length = starting_sub_length + get_length(subrule)
            this_check = check_sub_rule(line[starting_sub_length:this_length], subrule)
            sub_rule_check = min(this_check, sub_rule_check)
            starting_sub_length = this_length
        rule_check = max(sub_rule_check, rule_check)
    return rule_check

part_1=len([check for check in (check_rule(line,"0") for line in lines_list[i:]) if check])
print("Part 1:",  part_1)


def check_sub_rule2(line, subrule):
    if isinstance(rules[subrule], list):
        return check_rule2(line, subrule)
    else:
        return line==rules[subrule]

dict_history = {}
def check_rule2(line, rule_key):
    # if not sum(get_length(rule) for rule in rules[rule_key][0]) == len(line):
        # return False
    if line=="":
        return False
    stopnow = False
    for rule in rules[rule_key]:
        if rule_key in rule:
            stopnow=True
            copy_to_replace = copy.deepcopy(rules[rule_key])
            rules[rule_key].pop()
            for j in range(1, 2):
                aux_list = []
                for x in copy_to_replace[-1]:
                    if x == rule_key:
                        for y in copy_to_replace[1]:
                            aux_list.append(y)
                    else:
                        aux_list.append(x)
                copy_to_replace.append(aux_list)
                rules[rule_key].append([x for x in aux_list if x != rule_key])

    rule_check = False
    starting_length = 0
    for rule in rules[rule_key]:
        # print("################## Rule", rule)
        starting_sub_length = starting_length
        sub_rule_check = True
        for subrule in rule:
            this_length = starting_sub_length + get_length(subrule)
            this_check = check_sub_rule2(line[starting_sub_length:this_length], subrule)
            print(line[starting_sub_length:this_length])
            sub_rule_check = min(this_check, sub_rule_check)
            starting_sub_length = this_length
        rule_check = max(sub_rule_check, rule_check)
    return rule_check

rules["8"] = [['42'], ['42','8']]
rules["11"] =  [['42','31'], ['42','11','31']]
part_2=len([check for check in (check_rule2(line,"0") for line in lines_list[i:]) if check])
print("Part 2:",  part_2)