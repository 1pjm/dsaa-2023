'''
1. infix -> postfix
2. random infix 생성
3. postfix 계산기
4. infix 계산 정합성 검출기
'''
import sys
import random

def make_random_infix_formulation():
    # input 값
    # output 값
    random_infix_form = []

    iteration = random.randint(1, 15)

    for _ in range(iteration): # list
        number = random.choice("0123456789")
        sign = random.choice("+-*/")
        random_infix_form.append(number)
        random_infix_form.append(sign)

    random_infix_form = random_infix_form[:-1]
    return random_infix_form

def infix_to_postfix(expression):
        
        OPERATORS = set(['+', '-', '*', '/', '(', ')', '^'])
        PRIORITY = {'+':1, '-':1, '*':2, '/':2, '^':3}

        stack = []
        output = ''

        for ch in expression:
            if ch not in OPERATORS:  
                output+= ch
            elif ch=='(': 
                stack.append('(')
            elif ch==')':
                def is_matching_pair(open_bracket, close_bracket):
                    return (open_bracket == "(" and close_bracket == ")")
                
                if not is_matching_pair(stack.peek(), ch):
                        raise Exception('괄호의 불일치')
                else:
                    while stack and stack[-1]!= '(':
                        output += stack.pop()
                    stack.pop()
            else:
                while stack and stack[-1]!='(' and PRIORITY[ch]<=PRIORITY[stack[-1]]:
                    output+=stack.pop()
                stack.append(ch)
            print(f'단계 스택 상태: {stack}')
            
        while stack:
            output+=stack.pop()

        print(f'포스트픽스 변환 결과: {output}')

# stack&queue application에서 postfix_calculator

if __name__ == "__main__": # 여기서부터 실행
    while True:
        user_input = input('수식을 입력하시오: ')
        if user_input == "0":
            print("프로그램이 종료되었습니다.")
            break
            
        elif user_input == "1000":
            infix_form = make_random_infix_formulation()
            print(" ".join(infix_form))
            postfix_form = infix_to_postfix(infix_form)
            postfix_calculator
        else:
            if is_validate_infix(user_input):
                transform_infix_to_postfix(user_input):
            else:
                return
                
                
                

    # 수식을 입력하시오 출력
    # 사용자로부터 수식 입력받는다
    # 0 또는 1000이 입력 되었는지 확인
    # if 0이 입력: 프로그램 종료
    # if 1000이 입력: random 수식 생성
    # if 그냥 값 입력: infix -> postfix 변환
    #       값이 정확할 경우 - 변환실행
    #       값이 부정확할 경우 - 재입력 받기