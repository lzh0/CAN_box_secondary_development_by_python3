"""
创芯科技产品CAN盒子的二次开发方式（python语言）有两种：
    1.使用其提供的ControlCAN.dll文件（使用方法见ControlCAN.dll接口函数库（二次开发库）使用说明书.pdf）
    2.使用python库python-can

本程序使用第一种方法（ControlCAN.dll），且已自动处理python解释器位数问题，直接使用即可。

版本规划：
v0:windows平台下32/64位python解释器的基本CAN盒子配置、CAN帧收发。

待完善功能：
跨平台：windows/linux不同平台不同位数
参考https://blog.csdn.net/muyoufansem/article/details/117955581
"""
print("into ")
from time import sleep
from lib_for_main import *

canbox_device=CAN_BOX()

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
    send_canframe_data="22, 40, 60, 00, 06, 00, 00, 00"
    canbox_device.send_can_frame(2,send_canframe_id,send_canframe_data,send_canframe_dlc=-1)
    canbox_device.receive_can_frame(1);   #测试通过


    pass


if __name__ == "__main__":

    # 
    '''
    send_canframe_id=input("发送的CAN帧ID：")
    send_canframe_dlc=input("发送的CAN帧数据长度：")
    send_canframe_data=input("发送的CAN帧数据")
    '''
    
    

    

    while(1):
        power_down()
        sleep(3)
        power_up()
        sleep(3)
        power_down()
        
        sleep(3)
        pass

    
    print("__main___end")