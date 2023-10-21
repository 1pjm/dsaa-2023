import random

class InfixToPostfix:
    
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
        print(f'계산 결과: ')

    exp = str(input('수식을 입력하시오: '))
    exp_list = exp.split()
    if exp == 1000:
        exp_list.append(random.randint)
        print(f'생성된 수식: {exp_list}')
        exp_list = exp.split()
        infix_to_postfix(exp_list)

    elif exp == 0:
        exit(_ExitCode = None)

    infix_to_postfix(exp_list)

# 35 * 2 * 55 + 100 / 2

'''
1. 0을 입력하면 프로그램 종료
2. 1000을 입력하면 infix 형식의 랜덤 수식 생성 (연산자 최소 5개 이상 포함된)
3. 괄호 불일치 시 Exception 발생
4. 계산 결과 출력
'''