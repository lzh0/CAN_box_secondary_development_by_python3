"""
https://github.com/lzh0/CAN_box_secondary_development_by_python3.git
#本源码遵循GPLv2#   #follow GPLv2
创芯科技产品CAN盒子的二次开发方式（python语言）有两种：
www.zhcxgd.com
    1.使用其提供的ControlCAN.dll文件（使用方法见ControlCAN.dll接口函数库（二次开发库）使用说明书.pdf）
    2.使用python库python-can

本程序使用第一种方法（ControlCAN.dll），且已自动处理python解释器位数问题，直接使用即可。

版本规划：
v0:windows平台下32/64位python解释器的基本CAN盒子配置、CAN帧收发。

待完善功能：
跨平台：windows/linux不同平台不同位数
指定通道

"""
print("into ")
from time import sleep
from lib_for_main import *

canbox_device=CAN_BOX() #创建CAN 盒子对象

SDO_ask_cob_id=0x600
node_id=0x2
SDO_camframe_id=str(hex(SDO_ask_cob_id+node_id))

def power_up():
    send_canframe_id="0x600"
    send_canframe_data="22, 40, 60, 00, 80, 00, 00, 00" #清除错误
    canbox_device.send_can_frame(2,send_canframe_id,send_canframe_data,send_canframe_dlc=-1)
    canbox_device.receive_can_frame(1);   #测试通过

    send_canframe_id="0x600"
    send_canframe_data="22, 40, 60, 00, 06, 00, 00, 00" #
    canbox_device.send_can_frame(2,send_canframe_id,send_canframe_data,send_canframe_dlc=-1)
    canbox_device.receive_can_frame(1);   #测试通过

    send_canframe_id="0x600"
    send_canframe_data="22, 40, 60, 00, 0f, 00, 00, 00"
    canbox_device.send_can_frame(2,send_canframe_id,send_canframe_data,send_canframe_dlc=-1)
    canbox_device.receive_can_frame(1);   #测试通过


    send_canframe_id="0x600"
    send_canframe_data="22, 40, 60, 00, 0f, 00, 00, 00"
    canbox_device.send_can_frame(2,send_canframe_id,send_canframe_data,send_canframe_dlc=-1)
    canbox_device.receive_can_frame(1);   #测试通过


    pass

def power_down():
    send_canframe_id="0x600"
    send_canframe_data="22, 40, 60, 00, 6, 00, 00, 00"
    canbox_device.send_can_frame(2,send_canframe_id,send_canframe_data,send_canframe_dlc=-1)
    canbox_device.receive_can_frame(1);   #测试通过


    pass

def motion_velocity_init_config(node_id=0x00,max_speed=2000,max_acce=2000,max_dece=2000):
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  

    power_up()

    send_canframe_data=SDO_write_CS+"60, 60, 00, 03, 00, 00, 00"   #//进入恒速度模式
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    
    max_speed=hex(max_speed&0xff)+', '+hex(max_speed&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"83, 60, 00, "+max_speed+", 00, 00"   #//加速度限制
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    
    max_acce=hex(max_acce&0xff)+', '+hex(max_acce&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"84, 60, 00, "+max_speed+", 00, 00"  #//减速度限制
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    
    max_dece=hex(max_dece&0xff)+', '+hex(max_dece&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"85, 60, 00, "+max_speed+", 00, 00"   #//急停速度限制
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    

def motion_velocity_set_speed(change_speed_DEC=0):
    if(change_speed_DEC<0):change_speed_DEC=0   #目前不支持负速度反转   #注意如果没有负数检测，输入负数会导致速度调整为最大
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  
    change_speed_DEC=hex(change_speed_DEC&0xff)+', '+hex(change_speed_DEC&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"FF, 60, 00, "+change_speed_DEC+", 00, 00"   #//急停速度限制
    
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    pass


if __name__ == "__main__":

    # 
    '''
    send_canframe_id=input("发送的CAN帧ID：")
    send_canframe_dlc=input("发送的CAN帧数据长度：")
    send_canframe_data=input("发送的CAN帧数据")
    '''
    sleep(0.001)    #//1ms

    sleep(0.001)    #//1ms

    sleep(0.001)    #//1ms

    sleep(0.001)    #//1ms
    
                 # 22 60 60 00 03 00 00 00
    #00 00 06 02 # 22 ff 60 00 f0 00 00 00
    motion_velocity_init_config(node_id=2)
    canbox_device.receive_can_frame(); 

    while(1):
        ctrl_order=input("控制指令：")
        if(ctrl_order=="off"):power_down()
        if(ctrl_order=="on"):power_up()
        if(ctrl_order.isdigit()):   #如果全为数字
            motion_velocity_set_speed(int(ctrl_order))  #input(是堵塞的所以不用加延时)
            canbox_device.receive_can_frame(); 
        
        '''
        power_down()
        sleep(3)
        power_up()
        sleep(3)
       '''
        pass

    
    print("__main___end")