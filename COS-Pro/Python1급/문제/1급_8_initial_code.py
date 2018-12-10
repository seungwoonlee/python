def solution(N, votes):
    vote_counter = [0 for i in range(N+1)]
    for i in votes:
        vote_counter[i] += 1
        
    max_val = max(vote_counter)

    answer = []
    for idx in range(1, N + 1):
        if vote_counter[idx] == max_val:
            answer.append(vote_counter[idx])
    return answer


#아래는 테스트케이스 출력을 해보기 위한 코드입니다. 아래 코드는 잘못된 부분이 없으니, solution함수만 수정하세요.
N1 = 5
votes1 = [1,5,4,3,2,5,2,5,5,4]
ret1 = solution(N1, votes1)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다. 
print("solution 함수의 반환 값은 ", ret1, " 입니다.")


N2 = 4
votes2 = [1, 3, 2, 3, 2]
ret2 = solution(N2, votes2)

#[실행] 버튼을 누르면 출력 값을 볼 수 있습니다. 
print("solution 함수의 반환 값은 ", ret2, " 입니다.")