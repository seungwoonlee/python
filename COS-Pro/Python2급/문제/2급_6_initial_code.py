def solution(number):
    count = 0
    for i in range(1, number + 1):
        current = i
        temp = count
        while current != 0:
            if @@@:
                count += 1
                print("짝", end = '')
            current = current // 10
        if temp == count:
            print(i, end = '')
        print(" ", end = '')
    print("")
    return count

#아래는 테스트케이스 출력을 해보기 위한 코드입니다.
number = 40
ret = solution(number)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret, "입니다.")