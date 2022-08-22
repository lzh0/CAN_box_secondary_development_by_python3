
#python3.8.0 64位（python 32位要用32位的DLL）
#
from ctypes import *



VCI_USBCAN2 = 4
STATUS_OK = 1
canDLL=None  #【全局变量后期待优化】
vci_initconfig=None  #【全局变量后期待优化】
vci_can_obj=None #【全局变量后期待优化】
class VCI_INIT_CONFIG(Structure):  
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
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint), #十进制数 frame.dlc    #注意这里的返回数据内容是十进制的！！！，得转十六进制才好看
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),    #注意这里的返回数据内容是十进制的！！！，得转十六进制才好看
                ("Reserved", c_ubyte*3)
                ] 

def load_dll_file():
    CanDLLName = './ControlCAN_x64.dll' #把DLL放到对应的目录下
    global canDLL 
    canDLL= windll.LoadLibrary(CanDLLName)
    #Linux系统下使用下面语句，编译命令：python3 python3.8.0.py
    #canDLL = cdll.LoadLibrary('./libcontrolcan.so')
    print(CanDLLName)
 
    ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
    if ret == STATUS_OK:
        print('调用 VCI_OpenDevice成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_OpenDevice出错\r\n')

def open_can_box_device():
    global vci_initconfig
    #vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x03, 0x1C, 0)#波特率125k，正常模式
    vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x14, 0)#波特率1000k，正常模式

#初始(num)通道
def init_channel(channel_num):  #盒子上的通道1和2对应的dll中API应该是0和1，所以有-1
    if((channel_num)>2 or (channel_num)<0):
        print("init_channel fail:",channel_num,"is Undefined.")
        print("can_box only have channel 1 and channel 2.")
        return
    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, channel_num-1, byref(vci_initconfig))
    if ret == STATUS_OK:
        print('调用 VCI_InitCAN',channel_num,'成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_InitCAN',channel_num,'出错\r\n')
    
    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, channel_num-1)
    if ret == STATUS_OK:
        print('调用 VCI_StartCAN',channel_num,'成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_StartCAN',channel_num,'出错\r\n')



#初始0通道，即盒子上标的通道1
def init_channel_0():
    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
    if ret == STATUS_OK:
        print('调用 VCI_InitCAN1成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_InitCAN1出错\r\n')
    
    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
    if ret == STATUS_OK:
        print('调用 VCI_StartCAN1成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_StartCAN1出错\r\n')
 
#初始1通道，即盒子上标的通道2
def init_channel_1():
    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 1, byref(vci_initconfig))
    if ret == STATUS_OK:
        print('调用 VCI_InitCAN2 成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_InitCAN2 出错\r\n')
    
    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 1)
    if ret == STATUS_OK:
        print('调用 VCI_StartCAN2 成功\r\n')
    if ret != STATUS_OK:
        print('调用 VCI_StartCAN2 出错\r\n')
 
#通道1发送数据
def channel_1_send():
    ubyte_array = c_ubyte*8
    a = ubyte_array(1,2,3,4, 5, 6, 7, 8)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    global vci_can_obj
    vci_can_obj = VCI_CAN_OBJ(0x1, 0, 0, 1, 0, 0,  8, a, b)#单次发送
    
    ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
    if ret == STATUS_OK:
        print('CAN1通道发送成功\r\n')
    if ret != STATUS_OK:
        print('CAN1通道发送失败\r\n')
 
#通道2接收数据
def channel_2_receive():
    '''
    ubyte_array = c_ubyte*8
    a = ubyte_array(1,2,3,4, 5, 6, 7, 8)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    global vci_can_obj
    vci_can_obj = VCI_CAN_OBJ(0x1, 0, 0, 1, 0, 0,  8, a, b )
    '''
    #结构体数组类
    import ctypes
    class VCI_CAN_OBJ_ARRAY(Structure):
        _fields_ = [('SIZE', ctypes.c_uint16), ('STRUCT_ARRAY', ctypes.POINTER(VCI_CAN_OBJ))]

        def __init__(self,num_of_structs):
                                                                    #这个括号不能少
            self.STRUCT_ARRAY = ctypes.cast((VCI_CAN_OBJ * num_of_structs)(),ctypes.POINTER(VCI_CAN_OBJ))#结构体数组
            self.SIZE = num_of_structs#结构体长度
            self.ADDR = self.STRUCT_ARRAY[0]#结构体数组地址  byref()转c地址
        
    rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)#结构体数组

    ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(rx_vci_can_obj.ADDR), 2500, 0)
    #print(ret)
    while ret <= 0:#如果没有接收到数据，一直循环查询接收。
            ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(rx_vci_can_obj.ADDR), 2500, 0)
    if ret > 0:#接收到一帧数据
        print('CAN2通道接收成功\r\n')
        print('ID：')
        #print(vci_can_obj.ID)
        print(rx_vci_can_obj.ADDR.ID)
        print('DataLen：')
        #print(vci_can_obj.DataLen)
        print(rx_vci_can_obj.ADDR.DataLen)
        print('Data：')
        #print(list(vci_can_obj.Data))
        print(list(rx_vci_can_obj.ADDR.Data))



#关闭can盒子设备
def close_can_box_device():
    canDLL.VCI_CloseDevice(VCI_USBCAN2, 0) 

if __name__ == "__main__":
    load_dll_file()
    open_can_box_device()
    init_channel(2)
    while(1):
        channel_2_receive()

    print("hi");