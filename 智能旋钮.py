'''
目标功能：
0.旋钮功能（位置获取
1.多档开关（位置模式，位置设置
2.阻尼旋钮（0阻尼~有阻尼，0阻尼能实现看起来无摩檫力的那种一直以脱手速度旋转的状态


.多旋钮（电机）联动随动
'''
from time import sleep
from lib_for_main import *

canbox_device=CAN_BOX() #创建CAN 盒子对象







if __name__ == "__main__":

    
    running_mode=""
    power_up()
    canbox_device.receive_can_frame(); 
    motion_position_mode_init_config(node_id=2)
    canbox_device.receive_can_frame(); 

    while(1):
        ctrl_order=input()
        motion_position_mode_set_position(2,int(ctrl_order));print("set position",ctrl_order)#平滑位置模式
    

    
