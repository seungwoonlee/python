def solution(arr):
    left, right = 0, len(arr)-1
    while @@@:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

#아래는 테스트케이스 출력을 해보기 위한 코드입니다.
arr = [1, 4, 2, 3]
ret = solution(arr)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다.
print("solution 함수의 반환 값은 ", ret, " 입니다.")