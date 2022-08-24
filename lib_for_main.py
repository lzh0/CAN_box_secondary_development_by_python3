#ubyte :0~255
#byte:-128~127
#
import platform #python 解释器平台信息获取x64/x86、windows/linux
#import ctypes    #调用dll文件
from ctypes import *
import string


class VCI_INIT_CONFIG(Structure):  ##数据结构
    _fields_ = [("AccCode", c_uint),    #过滤接收码
                ("AccMask", c_uint),    #过滤屏蔽码
                ("Reserved", c_uint),   #API保留
                ("Filter", c_ubyte),    #滤波方式 0~3

                #Timing0和Timing1用来设置CAN波特率，详情见API说明书P8表格
                #常见波特率：1000 Kbps Timing0：0x00 Timing1：0x14
                ("Timing0", c_ubyte),   #波特率定时器 0（BTR0） 
                ("Timing1", c_ubyte),   #波特率定时器 1（BTR1）
                ("Mode", c_ubyte)   #模式。=0表示正常模式（相当于正常节点），=1表示只听模式（只接收，不影响总线），=2表示自发自收模式（环回模式）。
                ]  

class VCI_CAN_OBJ(Structure):  #数据结构
    _fields_ = [("ID", c_uint), #帧ID
                ("TimeStamp", c_uint),  
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),  
                ("RemoteFlag", c_ubyte),    #远程帧标志位
                ("ExternFlag", c_ubyte),    #拓展帧标志位
                ("DataLen", c_ubyte),   #canfram.dlc 帧数据长度
                ("Data", c_ubyte*8),    #canframe.data 帧数据内容最多8*8个字节
                ("Reserved", c_ubyte*3) #系统保留，填0
                ] 


class VCI_CAN_OBJ_ARRAY(Structure): #VCI_CAN_OBJ 的数组数据结构
        _fields_ = [('SIZE', c_uint16), ('STRUCT_ARRAY', POINTER(VCI_CAN_OBJ))]
        def __init__(self,num_of_structs):
                                                                    #这个括号不能少
            self.STRUCT_ARRAY = cast((VCI_CAN_OBJ * num_of_structs)(), POINTER(VCI_CAN_OBJ))#结构体数组
            self.SIZE = num_of_structs#结构体长度
            self.ADDR = self.STRUCT_ARRAY[0]#结构体数组地址  byref()转c地址

class CAN_BOX():
    def __init__(self,) -> None:    #构造函数
        #类公有变量：
        self.VCI_USBCAN2 = 4    #盒子型号代码Device Type   USBCAN-2A、USBCAN-2C、CANalyst-II 都为4
        self.bps=1000   #CAN网络通讯波特率Baud rate 设置
        #self.device_init_config
        #过滤验收码
        #过滤屏蔽码
        #工作模式
        #滤波方式
        #选择CAN通道
        #多设备索引选择

        
        self.ubyte_array_3 = c_ubyte * 3 #Reserved 系统保留参数
        self.Reserved_3 = self.ubyte_array_3(0, 0, 0) #赋初值0  #Reserved 系统保留

        self.ubyte_array_8 = c_ubyte * 8 #帧数据 十进制
        
        #CAN盒子初始化配置
        self.ControlCAN_dll=self.load_ControlCAN_dll_file() #dll文件载入
        self.device_init_config=self.open_device()  #CAN盒子设备配置
        self.init_channel()


        pass

    def __del__(self,): #析构函数
        (self.ControlCAN_dll).VCI_CloseDevice(self.VCI_USBCAN2, 0) #关闭can盒子设备

    def load_ControlCAN_dll_file(self,):
        python_interpreter_message=platform.architecture() #获取当前python解释器位数(32位或64位)
        if(python_interpreter_message[0]=="64bit"): #windows "64bit"
            print("your python's interpreter is",(platform.architecture()))
            CAN_DLL_PATH = './dll/windows/ControlCAN_x64.dll'
            self.ControlCAN_dll= windll.LoadLibrary(CAN_DLL_PATH)  #加载ControlCAN.dll文件
            pass
        
        else:   #windows "32bit"
            print("your python's interpreter is",(platform.architecture()))
            self.ControlCAN_dll= windll.LoadLibrary("./dll/windows/ControlCAN_x32.dll")  #加载ControlCAN.dll文件
        
        #Linux系统下使用下面语句，编译命令：python3 python3.8.0.py
        #self.ControlCAN_dll = cdll.LoadLibrary('./libcontrolcan.so')
        
        return self.ControlCAN_dll
    
    def open_device(self,):
        ret = (self.ControlCAN_dll).VCI_OpenDevice(self.VCI_USBCAN2, 0, 0)
        if ret == 1:
            print('VCI_OpenDevice: 设备开启成功')
        else:
            print('VCI_OpenDevice: 设备开启失败')
        vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x14, 0)#波特率1000k，正常模式
        
        return vci_initconfig

    
    def init_channel(self):  #盒子上的通道1和2对应的dll中API应该是0和1，所以有API操作时channel_num-1
        '''
    def init_channel(self,channel_num):
        #初始化指定通道
        if((channel_num)>2 or (channel_num)<0):
            print("init_channel fail:",channel_num,"is Undefined.")
            print("can_box only have channel 1 and channel 2.")
            return
        ret = self.ControlCAN_dll.VCI_InitCAN(self.VCI_USBCAN2, 0, channel_num-1, byref(self.device_init_config))
        if ret == 1:
            print('调用 VCI_InitCAN',channel_num,'成功\r\n')
        else:
            print('调用 VCI_InitCAN',channel_num,'出错\r\n')
        
        ret = self.ControlCAN_dll.VCI_StartCAN(self.VCI_USBCAN2, 0, channel_num-1)
        if ret == 1:
            print('调用 VCI_StartCAN',channel_num,'成功\r\n')
        else:
            print('调用 VCI_StartCAN',channel_num,'出错\r\n')
        '''
        
        #初始化全部通道
        ret = (self.ControlCAN_dll).VCI_InitCAN(self.VCI_USBCAN2, 0, 0, byref(self.device_init_config))
        if ret == 1:
            print('调用 VCI_InitCAN1成功\r\n')
        else:
            print('调用 VCI_InitCAN1出错\r\n')
        
        ret = self.ControlCAN_dll.VCI_StartCAN(self.VCI_USBCAN2, 0, 0)
        if ret == 1:
            print('调用 VCI_StartCAN1成功\r\n')
        else:
            print('调用 VCI_StartCAN1出错\r\n')

        ret = self.ControlCAN_dll.VCI_InitCAN(self.VCI_USBCAN2, 0, 1, byref(self.device_init_config))
        if ret == 1:
            print('调用 VCI_InitCAN2 成功\r\n')
        else:
            print('调用 VCI_InitCAN2 出错\r\n')
        
        ret = self.ControlCAN_dll.VCI_StartCAN(self.VCI_USBCAN2, 0, 1)
        if ret == 1:
            print('调用 VCI_StartCAN2 成功\r\n')
        else:
            print('调用 VCI_StartCAN2 出错\r\n')

    def send_can_frame(self,channel_index,send_canframe_id:string,send_canframe_data:string,send_canframe_dlc=-1): #帧发送
        #【待优化 大端模式←→小端模式】
        #【待优化 十六进制模式←→十进制模式】
        is_send_successful=0;

        ubyte_3array = c_ubyte*3    #Reserved 系统保留
        Reserved = ubyte_3array(0, 0, 0)   #赋初值0  #Reserved 系统保留

        ubyte_array = c_ubyte*8
        can_frame_data_array = ubyte_array(0,0,0,0, 0, 0, 0, 0) #发送帧数据数组初始化

        send_canframe_id=int(send_canframe_id,16)
        send_canframe_data_list=send_canframe_data.split(",")    #字符串转字符串列表，分隔符检测使用“,”符号


        for byte_data_index in range(0,len(send_canframe_data_list)):    #发送帧数据数组内容替换填充
            can_frame_data_array[byte_data_index]=int(send_canframe_data_list[byte_data_index],16)    #数组内容填充为要发送的内容，且将传入参数的十六进制转换为十进制发送
        print("send:",send_canframe_id," data: " ,list(can_frame_data_array))  #显示将发送的帧数据
        
        if(send_canframe_dlc>-1):   #判断是否自动计算send_canframe_dlc
            #手动输入send_canframe_dlc模式
            vci_can_obj = VCI_CAN_OBJ(send_canframe_id, 0, 0, 1, 0, 0, send_canframe_dlc, can_frame_data_array, Reserved)    #帧数据内容填充    #单次发送
            '''
            if (len(send_canframe_data)>send_canframe_dlc): #判断dlc是否与实际数据长度相符
                print("warrning: len(send_canframe_data)!=send_canframe_dlc")   #不相符发出警告
            pass
            '''
        else:
            #自动计算send_canframe_dlc模式
            vci_can_obj = VCI_CAN_OBJ((send_canframe_id), 0, 0, 1, 0, 0, len(can_frame_data_array), can_frame_data_array, Reserved)    #帧数据内容填充    #单次发送
        #注意这里的都是十进制，无论收与发都是即0x600对应应发送的十进制数是1536
        #int("0x600",10) 强制类型转换，将十六进制下的600转化为十进制下的1536
        #python 进制转换：https://blog.csdn.net/chyuanrufeng/article/details/101478194

        is_send_successful = self.ControlCAN_dll.VCI_Transmit(self.VCI_USBCAN2, 0, channel_index-1, byref(vci_can_obj), 1)
        # VCI_USB_CAN_2: 设备类型
        # DEV_INDEX:     设备索引
        # can_index:     CAN通道索引
        # can_obj:       请求参数体
        # TRANSMIT_LEN:  发送的帧数量
        
        
        
        if is_send_successful == 1:
            print(channel_index,'通道发送成功')
        else:
            print(channel_index,'通道发送失败')
            return is_send_successful

    def receive_can_frame(self,block_flag=0,can_box_channel_index=-1):
        #【待优化 大端模式←→小端模式】
        #【待优化 十六进制模式←→十进制模式】
        #程序流程：读取缓冲区内待接收的帧数量→构建缓冲区内帧数量的容器（帧数组）→读取缓冲区内所有帧数据并存放到容器（帧数组）中→依次打印所有帧数据→返回容器（帧数组）
        
        frames_count=(self.ControlCAN_dll).VCI_GetReceiveNum(self.VCI_USBCAN2,0,1)     #缓冲区帧数计数，同时也是接收标志位
        print("接收到",frames_count,"帧数据")
        if block_flag==1:    #堵塞模式判断，堵塞模式标志位为1则为堵塞模式
            while((frames_count)==0):   #堵塞模式，一直查询缓冲区中是否有接收到的帧计数，直到接收到数据
                frames_count=(self.ControlCAN_dll).VCI_GetReceiveNum(self.VCI_USBCAN2,0,1)     #缓冲区帧数计数更新，同时也是接收标志位

        if(frames_count>0): #判断缓冲区中帧计数是否大于0，即是否有帧数据
            #有帧数据的情况，则读取
            can_frme_data = self.ubyte_array_8(0, 0, 0, 0, 0, 0, 0, 0)    ##赋初值0
            can_frame_object = VCI_CAN_OBJ(0, 0, 0, 1, 0, 0, 8, can_frme_data, self.Reserved_3)  #构造帧结构体
            can_frame_object_array=VCI_CAN_OBJ_ARRAY(frames_count)   #构造帧结构体数组，用来接收复数的帧数据
            (self.ControlCAN_dll).VCI_Receive(self.VCI_USBCAN2, 0, 1, byref(can_frame_object_array.ADDR), frames_count, 0)    #获取缓冲区中所有接收到的CAN帧，执行后会清空接收缓冲区，每个通道缓冲区中最多放2000帧左右
                
                # VCI_USB_CAN_2: 设备类型
                # DEV_INDEX:     设备索引
                # can_index:     CAN通道索引
                # can_obj_array_address:       请求参数体，帧结构体数组的首指针，注意帧结构体数量一定要大于RECEIVE_LEN，否则会出现内存错误导致程序闪退
                # RECEIVE_LEN:   用来接收帧结构体数组的长度，表示该次读取多少帧的数据
                # WAIT_TIME:     保留参数
                #VCI_Receive返回实际读取的帧数，=-1表示USB-CAN设备不存在或USB掉线。

            ##读取成功，接收到了帧数据，则打印帧对象数组中的所有帧对象
            for can_frame_index in range(frames_count):  #can_frame_object_array不能构成迭代器，只能稍微走一点弯路
                self.print_can_frame((can_frame_object_array.STRUCT_ARRAY)[can_frame_index])  #格式化显示

            return  can_frame_object_array    #返回接收到的帧对象数组
        
        else:  #没有接收到CAN帧
            print("非堵塞模式 没有接收到CAN帧数据 receive notrhing")
            return None

                    
        

            

    def print_can_frame(self,can_frame_object:object,num_system="hex"):
        """
        #【待优化：1.根据canframe.dlc显示指定范围的内容 2.不同通道显示CAN1、CAN2】
        e.g.:
        【优化前：】
        CAN2通道接收成功，帧内容如下：
        canframe.id: 0x702 canframe.dlc: 0x1 canframe.data: ['00', '00', '00', '00', '00', '00', '00', '00']
        【优化后：】
        CAN2通道接收成功，帧内容如下：
        canframe.id: 0x702 canframe.dlc: 0x1 canframe.data: ['00']
        
        canframe_id=can_frame_object.ID
        canframe_dlc=can_frame_object.DataLen
        canframe_data=can_frame_object.Data
        """

        if(num_system=="hex"):  #十六进制
            print('CAN2通道接收成功，帧内容如下：')
            print(#打印获取到的帧内容
                #"can_device_channel:",channel  #数据来自于 CAN 盒子通道 【1或2】
                "canframe.id:",hex(int(can_frame_object.ID)),    #帧ID
                "canframe.dlc:",hex(int(can_frame_object.DataLen)),   #帧数据长度
                "canframe.data:", list(map(lambda x: hex(x).split('x')[1].zfill(2), list(can_frame_object.Data)))  #帧数据  #zfill(2) 函数是指当只有一位时补充为两位，如10的十六进制为0xa，补充两位成为0x0a
            ) 
            return

        if(num_system=="dec"):  #十进制
            print('CAN2通道接收成功，帧内容如下：')
            print(#打印获取到的帧内容
                #"can_device_channel:",channel  #数据来自于 CAN 盒子通道 【1或2】
                "canframe.id:",can_frame_object.ID,    #帧ID
                "canframe.dlc:",can_frame_object.DataLen,   #帧数据长度
                "canframe.data:",list(can_frame_object.Data)  #帧数据
            ) 
            return
        if(num_system=="bin"):  #二进制
            return



        
        
        pass