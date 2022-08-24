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
from time import sleep
from urllib.parse import uses_fragment
from lib_for_main import *

canbox_device=CAN_BOX() #创建CAN 盒子对象



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

def motion_velocity_mode_init_config(node_id=0x00,max_speed=2000,max_acce=2000,max_dece=2000):  #驱动器驱动方式：速度模式——初始化
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
    

def motion_velocity_mode_set_speed(node_id=0x00,set_speed=0): #驱动器驱动方式：速度模式——更改当前电机速度
    #CAN_id 合成
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型

    #CAN_data 合成
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  can_frame.data[0]
    object_dictionary_Target_velocity_index="FF, 60, "   #can_frame.data[1][2]    #字典对象 0x60FF: 名称：目标速度 Target velocity 0x60FF Sets velocity reference for velocity profiler. 访问R/W 、可映射?Y 、Data type：INTEGER32、Category：Mandatory
    set_speed_hex_strings=""
    
    if(set_speed<0):    #速度方向判断，正数正转，负数反转
        #负数反转处理
        set_speed=(4294967295+set_speed)+1#ff ff ff ff  4294967295    #ff ff ff ff==-1
        
    for i in range(4):  #以下为十进制转十六进制，再转小端模式的转换
        set_speed_value_byte=hex((set_speed>>i*8)&0xff) #右移i个字节再按位取AND，即可得到每个字节值
        set_speed_hex_strings=set_speed_hex_strings+', '+set_speed_value_byte   #按小端的字节顺序排序

    send_canframe_data=SDO_write_CS+object_dictionary_Target_velocity_index+"00"+set_speed_hex_strings   #//速度设置共计4个字节  #小端模式从左到右，依次为速度的高位到低位
    
    #CAN帧发送
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)


def motion_position_mode_init_config(node_id=0x00,): #驱动器驱动方式：位置模式——初始化

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
    

    motion_velocity_mode_init_config(node_id=0x2)  #//设置为速度模式
    canbox_device.receive_can_frame(); 

    while(1):
        ctrl_order=input("控制指令：")
        if(ctrl_order==""):print("ctrl_order is empty") #无输入情况
        elif(ctrl_order=="off"):power_down()
        elif(ctrl_order=="on"):power_up()
        elif(ctrl_order[0]=="+" or ctrl_order[0]=="-"):   #速度设置指令检测 #ctrl_order.isdigit()#判断字符串内是否全为数字
            #除第一位外全为数字,则调节速度
            motion_velocity_mode_set_speed(2,int(ctrl_order))  #input(是堵塞的所以不用加延时)
            
        else:#直接发送帧数据
            #usage:602#22,40,60,00,06,00,00,00  #电机失能
            send_canframe=ctrl_order.split("#")
            canbox_device.send_can_frame(0x2,send_canframe[0],send_canframe[1],send_canframe_dlc=8)

        canbox_device.receive_can_frame();  #//接收帧数据

    #while(1)结束
    print("__main___end")