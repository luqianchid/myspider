#-*-coding:utf-8 -*-
import sys
import os
import random

# 生成Target
def newTarget():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    target = random.sample(nums, 4)  # 随机生成一个不重复的包含四位数的数组
    target = ''.join([str(i) for i in target])  # 转换成字符串
    # ANSWER['answer'] = target
    return target
#返回提示
def hintme(target,guess):  
    n = len(target)
    a, b = 0, 0
    if n <= 0:
        return
    for i in range(n):
        if target[i] == guess[i]:
            a += 1
        elif target[i] in guess:
            b += 1
    res = '%dA%dB' % (a,b)
    return res
# 运行中使用设置
def getSet(sets):
    eval(SETTING[sets])
# 检查输入
def check(input_str):       
    while len(input_str) != 4 or input_str.isdigit() == False:
        input_str = raw_input("不合法:请输入四位数字:")
    return input_str
# 开始游戏
def startGame(target):
    # 判断guess是否符合条件    
    guess = check(raw_input("输入你猜的四位数字(首位可以为0):"))  
    res = hintme(target, guess)
    count = 4
    while res != '4A0B':
        if count == 0:
            print '挑战失败'
            print '开始新游戏请输入4，退出游戏请按5'
            choose = getSet(raw_input('输入设置'))  
        else:  
            print(res)      
            guess = check(raw_input('不正确~重新输入:')) 
            hintme(target, guess)
        count -= 1
    print '恭喜！答案是%s' % target 
    print '开始新游戏请输入4，退出游戏请按5'
    choose = getSet(raw_input('输入设置'))    
# 获取答案
def getAnswer():
    print ANSWER['answer']
    startGame(ANSWER['answer'])
# 修改答案并重新运行
def changeAnswer():
    target = check(raw_input('修改答案:'))
    ANSWER['answer'] = target
    game = getSet(raw_input('原答案已被修改,输入1开始游戏'))
#重置
def reset():
    ANSWER["answer"] = newTarget()
    startGame(ANSWER["answer"])
# 退出游戏
def exitGame():
    print '游戏已结束！'
    sys.exit()

if __name__ == "__main__":
    print "------<<猜数字小游戏>>------"
    print "1.开始游戏|2.查询答案|3.修改答案|4.新建游戏|5.退出游戏"
    print '注意:你只有5次机会,格式错误不会被计入次数中'
    # 全部变量: 答案 设置
    ANSWER = {'answer':''}
    ANSWER["answer"] = newTarget()
    SETTING = {'1':'startGame(ANSWER["answer"])','2':'getAnswer()','3':'changeAnswer()','4':'reset()','5': 'exitGame()'}
    sets = raw_input("输入设置:>")
    eval(SETTING[sets])

