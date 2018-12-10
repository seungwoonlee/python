def solution(characters):
    result = ""
    result += characters[0]
    for i in range(len(characters)):
        if characters[i - 1] != characters[i]:
            result += characters[i]
    return result

#아래는 테스트케이스 출력을 해보기 위한 코드입니다. 아래 코드는 잘못된 부분이 없으니, solution함수만 수정하세요.
characters = "senteeeencccccceeee"
ret = solution(characters)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은", ret, "입니다.")