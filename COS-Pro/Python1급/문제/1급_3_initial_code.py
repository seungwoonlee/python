def func_a(numA, numB, exp):
    if exp == '+':
        return numA + numB
    elif exp == '-':
        return numA - numB
    elif exp == '*':
        return numA * numB
    
def func_b(exp):
    for index, value in enumerate(exp):
        if value == '+' or value == '-' or value == '*':
            return index
        
def func_c(exp, idx):
    numA = int(exp[:idx])
    numB = int(exp[idx + 1:])
    return numA, numB

def solution(expression):
    exp_index = func_@@@(@@@)
    first_num, second_num = func_@@@(@@@)
    result = func_@@@(@@@)
    return result

#아래는 테스트케이스 출력을 해보기 위한 코드입니다.
expression = "123+12"
ret = solution(expression)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret, "입니다.")