def func_a(arr):
    counter = [0 for _ in range(1001)]
    for x in arr:
        counter[x] += 1
    return counter

def func_b(arr):
    ret = 0
    for x in arr:
        if ret < x:
            ret = x
    return ret

def func_c(arr):
    INF = 1001
    ret = INF
    for x in arr:
        if x != 0 and ret > x:
            ret = x
    return ret

def solution(arr):
    counter = func_@@@(@@@)
    max_cnt = func_@@@(@@@)
    min_cnt = func_@@@(@@@)
    return max_cnt // min_cnt

#아래는 테스트케이스 출력을 해보기 위한 코드입니다.
arr = [1, 2, 3, 3, 1, 3, 3, 2, 3, 2]
ret = solution(arr)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret, "입니다.")