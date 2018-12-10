def solution(prices):
    INF = 1000000001;
    tmp = INF
    answer = -INF
    for price in prices:
        if tmp != INF:
            answer = max(answer, tmp - price)
        tmp = min(tmp, price)
    return answer

#아래는 테스트케이스 출력을 해보기 위한 코드입니다. 아래 코드는 잘못된 부분이 없으니, solution함수만 수정하세요.
prices1 = [1, 2, 3];
ret1 = solution(prices1);

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret1, "입니다.")
    
prices2 = [3, 1];
ret2 = solution(prices2);

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret2, "입니다.")