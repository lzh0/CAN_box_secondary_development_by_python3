'''
目标功能：
0.旋钮功能（位置获取
1.多档开关（位置模式，位置设置
2.阻尼旋钮（0阻尼~有阻尼，0阻尼能实现看起来无摩檫力的那种一直以脱手速度旋转的状态


.多旋钮（电机）联动随动
'''
class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

print(bcolors.OK + "File Saved Successfully!" + bcolors.RESET)
print(bcolors.WARNING + "Warning: Are you sure you want to continue?" + bcolors.RESET)
print(bcolors.FAIL + "Unable to delete record." + bcolors.RESET)


print(f"{bcolors.OK}File Saved Successfully!{bcolors.RESET}")
print(f"{bcolors.WARNING}Warning: Are you sure you want to continue?{bcolors.RESET}")
print(f"{bcolors.FAIL}Unable to delete record.{bcolors.RESET}")



#if __name__ == "__main__":

    
    
