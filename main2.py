def check_parentheses(input_str):
    stack = []
    result = ""

    for char in input_str:
        if char == '(' or "(":
            stack.append(char)
        elif char == ')' or ")":
            if stack:
                stack.pop()
            else:
                result += "?"

    for _ in stack:
        result += "x"

    return input_str + "\n" + result

# 从用户输入读取测试用例
while True:
    test_case = input("请输入一个字符串（按 Enter 键提交，输入 quit 退出）: ")
    if test_case == 'quit':
        break
    else:
        print(check_parentheses(test_case))
