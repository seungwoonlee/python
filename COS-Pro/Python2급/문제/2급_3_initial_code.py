def func_a(month, day):
    month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    total = 0;
    for i in @@@:
        total += @@@
    total += @@@
    return total - 1
        
def solution(start_month, start_day, end_month, end_day):
    start_total = func_a(start_month, start_day)
    end_total = func_a(end_month, end_day)
    return end_total - start_total

#아래는 테스트케이스 출력을 해보기 위한 코드입니다.
start_month = 1
start_day = 2
end_month = 2
end_day = 2
ret = solution(start_month, start_day, end_month, end_day)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret, "입니다.")