### 주어진 리스트 숫자들의 중간값 구하기

# 1. 입력된 값이 짝수인지 홀수인지 확인
# 2. 숫자들을 크기 순서대로 나열하기
# 3. 중앙값의 index를 가져오기
#    - 짝수일 때 :
#    - 홀수일 때 :
# return 중앙값

def get_median(number_list):

    # len을 쓰지 않고
    # counter = 0
    # for _ in number_list:
    #     counter += 1

    counter = len(number_list)          # n번 순회
    flag_odd = counter % 2 if True else False # 삼항연산자, 1번 순회
    number_list.sort()          # n log n 순회
    # sort(): 리턴값이 없는 함수
    # sorted(): 리턴됨

    if flag_odd: # 홀수일 때 (True), 1번 순회
        target_index = int((len(number_list) - 1) / 2) # n+ 3 순회
        median = number_list[target_index] # 1 순회
    else: # 짝수일 때 (False)
        t_index1 = int((len(number_list) - 1) / 2) # n + 3
        t_index2 = int((len(number_list) + 1) / 2) # n + 3
        value = number_list[t_index1] + number_list[t_index2] # 2 순회
        median = value / 2 # 1 순회
    return median

number_list = [39, 11, 454, 11, 99]
result = get_median(number_list)
print(result)