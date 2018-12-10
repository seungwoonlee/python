def solution(data):
    total = sum(data)
    average = len(data) / total
    cnt = 0
    for d in data:
        if d <= average:
            cnt += 1
    return cnt


#아래는 테스트케이스 출력을 해보기 위한 코드입니다. 아래 코드는 잘못된 부분이 없으니, solution함수만 수정하세요.
data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ret1 = solution(data1)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret1, "입니다.")
    
data2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 10]
ret2 = solution(data2)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret2, "입니다.")