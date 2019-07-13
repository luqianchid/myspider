import random
import re
import sys
def hintme(target,guess):
    n = len(target)
    a, b = 0, 0
    for i in range(n):
        if target[i] == guess[i]:
            a += 1
        elif target[i] in guess:
            b += 1
    return '%dA%dB' % (a,b)

def check(guess): #对输入进行检查
    if guess != '0':
        while len(guess) != 4 or guess.isdigit() == False:          
            guess = input("ValueError:输入不合法/请输入四位数字:")
        return guess
    else:
        sys.exit() # 输入0退出游戏

if __name__ == "__main__":
    nums = [0,1,2,3,4,5,6,7,8,9]
    target = random.sample(nums,4) #随机生成一个不重复的包含四位数的数组   
    target = ''.join([str(i) for i in target]) #转换成字符串
    print("随机不重复数字已生成%s" % target)
    print('输入0退出游戏')
    guess = check(input("请输入您所猜测的数字:")) # 判断guess是否符合条件 
    while hintme(target,guess) != '4A0B':
        print(hintme(target,guess))
        guess = check(input('请重新输入猜测的数字:'))        
        hintme(target,guess)
    print('回答正确！您猜到的数为:%s' % target)