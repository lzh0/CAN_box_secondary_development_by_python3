#!/usr/bin/env python

"""
This example shows how sending a single message works.
"""

import can
from can.bus import BusState

if __name__ == "__main__":

    """Sends a single message."""
    bus = can.interface.Bus(bustype='canalystii', channel=0, bitrate=500000)#初始化CAN1通道用来发送
    bus2 = can.interface.Bus(bustype='canalystii', channel=1, bitrate=500000)#实始化CAN2通道用来接收
    msg = can.Message(
        arbitration_id=0x123, data=[0x01,0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08], is_extended_id=False
    )
    try:
        bus.send(msg)
        print(f"Message sent on {bus.channel_info}")
        print(msg)
    except can.CanError:
        print("Message NOT sent")

    """Receives messages."""


    while True:
        msg = bus2.recv(1)
        if msg is not None:
            print(msg)
        else:
            print(msg)
    bus.shutdown()


