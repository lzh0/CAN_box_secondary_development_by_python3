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
from lib_for_main import *

canbox_device=CAN_BOX() #创建CAN 盒子对象



def power_up():
    '''
    #【代码复用度太低了，在最基础的CAN帧发送的基础上，还应添加对应的协议内容，
    # 如301的SDO_send_wirte就可以默认can_frame.data[0]=0x22；
    # 再细化还能将ica401协议内容封装进来，形成进一步的如sdo_write_motor_stat_set就可以默认为"22 40 60 00"+驱动器要转移的状态】
    '''
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
    send_canframe_data=SDO_write_CS+"85, 60, 00, "+max_dece+", 00, 00"   #//急停速度限制
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    

def motion_velocity_mode_set_speed(node_id=0x00,set_speed=0): #驱动器驱动方式：速度模式——更改当前电机速度   单位是Cnts/s(counts/s) 不是RPM 
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
        
    for i in range(4):  #以下为十进制转十六进制，再转小端模式的转换 【这个可以单独抽出来成为一个函数（和上面的负数处理一起】
        set_speed_value_byte=hex((set_speed>>i*8)&0xff) #右移i个字节再按位取AND，即可得到每个字节值
        set_speed_hex_strings=set_speed_hex_strings+', '+set_speed_value_byte   #按小端的字节顺序排序

    send_canframe_data=SDO_write_CS+object_dictionary_Target_velocity_index+"00"+set_speed_hex_strings   #//速度设置共计4个字节  #小端模式从左到右，依次为速度的高位到低位
    
    #CAN帧发送
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    

def motion_position_mode_init_config(node_id=0x00,move_to_position=0,max_speed=2000,accleration=2000): #驱动器驱动方式：位置模式——初始化
    #注意位置模式第一次运行时会花时间自动找零（低转速转很多圈，然后自动停止
    '''
    附低相关内容：
    关于找零、回零
    有两种自引导速度：1.较快的速度用于寻找限位开关或参考开关；2.较慢的速度精确地定位相应控制脉冲沿上的位置。
    关于回零：
    https://blog.csdn.net/kuniqiw/article/details/116593945
    https://zhuanlan.zhihu.com/p/481474404
    MAN-CAN402IG.pdf 9: 自引导模式
    607Ch: Home offset
    6098h: Homing method
    6099h: Homing speeds
    609Ah: Homing acceleration

    #用到的指令总览：
    602#22,60,60,00,01,00,00,00 //设置位置模式

    602#22,81,60,00,0f,00,00,00//位置模式参数设置
    602#22,83,60,00,0f,00,00,00//位置模式参数设置
    602#22,84,60,00,0f,00,00,00//位置模式参数设置
    602#22,85,60,00,0f,00,00,00//位置模式参数设置

    602#22,7a,60,00,f0,00,00,00//设置运动到指定位置f0
    602#22,7a,60,00,00,00,00,00//设置运动到指定位置00
    602#22,40,60,00,0f,00,00,00//设置驱动器状态，
    602#22,40,60,00,3f,00,00,00//设置驱动器状态，该状态下才会移动到指定位置
    602#22,41,2f,00,02,00,00,00//【未能理解，但作用是防止重复设置位置两次】

    #未用到的:
    602#40,40,60,00,00,00,00,00//问驱动器状态
    602#40,63,60,00,00,00,00,00 //问驱动器电机位置
    '''
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  

    power_up()

    send_canframe_data=SDO_write_CS+"60, 60, 00, 01, 00, 00, 00"   #//进入位置模式PP Mode
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    
    accleration=hex(accleration&0xff)+', '+hex(accleration&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"83, 60, 00, "+accleration+", 00, 00"   #//加速度限制
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    
    #max_acce=hex(max_acce&0xff)+', '+hex(max_acce&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"84, 60, 00, "+accleration+", 00, 00"  #//减速度限制
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    
    max_dece=5000
    max_dece=hex(max_dece&0xff)+', '+hex(max_dece&0xff00)[:-2]   #[:-2]删去字符串最后两位
    send_canframe_data=SDO_write_CS+"85, 60, 00, "+max_dece+", 00, 00"   #//急停减速度设置
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)

    send_canframe_data=SDO_write_CS+"41,2f, 00, "+"02"+", 00, 00"   #//对象 0x2F41  //能神奇的解决每次位置更新慢一拍/需要重复发两次的问题
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    

def motion_position_mode_set_position(node_id=0x00,set_position=0): #驱动器驱动方式：速度模式——更改当前电机速度
    #位置范围[--]60*81=4860=0x1248  #实际上远比这个大...四个字节..
    #CAN_id 合成
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型
    
    #CAN_data 合成
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  can_frame.data[0]
    object_dictionary_Target_velocity_index="7A, 60, "   #can_frame.data[1][2]    #字典对象 0x607A: 名称：目标速度 Target velocity 0x60FF Sets velocity reference for velocity profiler. 访问R/W 、可映射?Y 、Data type：INTEGER32、Category：Mandatory
    set_position_hex_strings=""
    
    if(set_position<0):    #速度方向判断，正数正转，负数反转
        #负数反转处理
        set_position=(4294967295+set_position)+1#ff ff ff ff  4294967295    #ff ff ff ff==-1
        
    for i in range(4):  #以下为十进制转十六进制，再转小端模式的转换
        set_position_value_byte=hex((set_position>>i*8)&0xff) #右移i个字节再按位取AND，即可得到每个字节值
        set_position_hex_strings=set_position_hex_strings+', '+set_position_value_byte   #按小端的字节顺序排序

    send_canframe_data_postiion=SDO_write_CS+object_dictionary_Target_velocity_index+"00"+set_position_hex_strings   #//速度设置共计4个字节  #小端模式从左到右，依次为速度的高位到低位

    
    #CAN帧发送
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data_postiion,send_canframe_dlc=8)

    send_canframe_data="22, 40, 60, 00, 0f, 00, 00, 00" #//位置模式，转动到指定位置流程：设置位置→→→运动到指定位置
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=-1)

    

    send_canframe_data="22, 40, 60, 00, 3f, 00, 00, 00"
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=-1)


def motion_profiled_torque_mode_init_config(node_id=0x00,): #驱动器驱动方式：力矩模式——初始化
    #【提问：不同运动模式之间能同时存在吗？
    '''
    #用到的指令总览：
    602#22,60,60,00,04,00,00,00 //设置力矩模式  Profiled torque mode

    602#22,71,60,00,0c,12,00,00//设置对象 0x6067 Position window: 位置窗口为300（0x12c）

    '''
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  

    power_up()

    send_canframe_data=SDO_write_CS+"67, 60, 00, 0c, 12, 00, 00"   #//进入力矩模式  Profiled torque mode
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)

    send_canframe_data=SDO_write_CS+"60, 60, 00, 04, 00, 00, 00"   #//进入力矩模式  Profiled torque mode
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data,send_canframe_dlc=8)
    

def motion_profiled_torque_mode_set_torque(node_id=0x00,set_torque=0): #驱动器驱动方式：速度模式——更改当前电机速度
    #函数功能：控制驱动器命令电机输出力矩
    #函数输入：节点ID, 力矩大小[-1000-1000]
    #CAN_id 合成
    SDO_ask_cob_id=0x600
    SDO_camframe_id=hex(SDO_ask_cob_id+node_id) #//注意hex()函数返回的是字符串类型
    
    #CAN_data 合成
    SDO_write_CS="22, "   #0x0022 DEFSTRUCT SDO Parameter  can_frame.data[0]
    object_dictionary_Target_velocity_index="71, 60, "   #can_frame.data[1][2]    #字典对象 0x607A: 名称：目标速度 Target velocity 0x60FF Sets velocity reference for velocity profiler. 访问R/W 、可映射?Y 、Data type：INTEGER32、Category：Mandatory
    set_torque_hex_strings=""
    
    if(set_torque<0):    #速度方向判断，正数正转，负数反转
        #负数反转处理
        set_torque=(4294967295+set_torque)+1#ff ff ff ff  4294967295    #ff ff ff ff==-1
        
    for i in range(4):  #以下为十进制转十六进制，再转小端模式的转换
        set_torque_value_byte=hex((set_torque>>i*8)&0xff) #右移i个字节再按位取AND，即可得到每个字节值
        set_torque_hex_strings=set_torque_hex_strings+', '+set_torque_value_byte   #按小端的字节顺序排序

    send_canframe_data_postiion=SDO_write_CS+object_dictionary_Target_velocity_index+"00"+set_torque_hex_strings   #//速度设置共计4个字节  #小端模式从左到右，依次为速度的高位到低位

    
    #CAN帧发送
    canbox_device.send_can_frame(2,SDO_camframe_id,send_canframe_data_postiion,send_canframe_dlc=8)




if __name__ == "__main__":


    running_mode=""
    canbox_device.receive_can_frame(); 

    while(1):
        ctrl_order=input("控制指令：")
        if(ctrl_order==""):print("ctrl_order is empty") #无输入情况
        elif(ctrl_order=="pp"): #平滑位置模式
            running_mode=ctrl_order
            print("#平滑位置模式")
            motion_position_mode_init_config(node_id=0x2) #//设置为平滑位置模式
        elif(ctrl_order=="pv"): #平滑速度模式
            running_mode=ctrl_order
            print("#平滑速度模式")
            motion_velocity_mode_init_config(node_id=0x2)  #//设置为平滑速度模式
        elif(ctrl_order=="tq"): #平滑转矩模式
            running_mode=ctrl_order
            motion_profiled_torque_mode_init_config(node_id=0x02)   #//设置为平滑转矩模式
            print("#平滑转矩模式")
            pass


            
        elif(ctrl_order=="off"):power_down()
        elif(ctrl_order=="on"):power_up()
        elif(ctrl_order[0]=="+" or ctrl_order[0]=="-"):   #xx模式运动数值设置 #ctrl_order.isdigit()#判断字符串内是否全为数字
            #除第一位外全为数字,则将数字作为输入值
            if(running_mode==""):print("电机运动模式未设置")
            elif(running_mode=="pp"): motion_position_mode_set_position(2,int(ctrl_order));print("set position",ctrl_order)#平滑位置模式
            elif(running_mode=="pv"): motion_velocity_mode_set_speed(2,int(ctrl_order))  #input(是堵塞的所以不用加延时)#平滑速度模式
            elif(running_mode=="tq"): motion_profiled_torque_mode_set_torque(2,int(ctrl_order))  #平滑转矩模式  #力矩同样有正反转的方向，用正负数表示   #±125差不多刚刚好一转就转，一按就停的状态，无摩擦状态
                
            else:
                pass

            
            
        elif((ctrl_order.find(','))>-1):   #直接发送帧数据
            #usage:602#22,40,60,00,06,00,00,00  #电机失能
            send_canframe=ctrl_order.split("#")
            canbox_device.send_can_frame(0x2,send_canframe[0],send_canframe[1],send_canframe_dlc=8)
            
            
        else:
            print("undefind未定义指令，请检查")

            
        sleep(0.01)    #//10ms  #
        canbox_device.receive_can_frame();  #//接收帧数据

    #while(1)结束
    print("__main___end")