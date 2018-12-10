def func_a(string, length):
    padZero = ""
    padSize = @@@
    for i in range(padSize):
        padZero += "0"
    return padZero + string

def solution(binaryA, binaryB):
    max_length = max(len(binaryA), len(binaryB))
    binaryA = func_a(binaryA, max_length)
    binaryB = func_a(binaryB, max_length)
    
    hamming_distance = 0
    for i in range(max_length):
        if @@@:
            hamming_distance += 1
    return hamming_distance

#아래는 테스트케이스 출력을 해보기 위한 코드입니다.
binaryA = "10010"
binaryB = "110"
ret = solution(binaryA, binaryB)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret, "입니다.")