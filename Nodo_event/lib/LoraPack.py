import os
import socket
import time
import struct
from network import LoRa
import uos
import ubinascii, network

_LORA_PKG_FORMAT = "BBBBB"
_LORA_PKG_ACK_FORMAT = "BBB"

def pack_Lora(DEVICE_ID, location, Px, Device_next, UID_msg):
    global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
    pkg = struct.pack(_LORA_PKG_FORMAT, DEVICE_ID, location, Px, Device_next, UID_msg)
    return pkg

def pack_AckLora(DEVICE_ID, DEVICE_Resp, Px):
    global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
    pkg_ack = struct.pack(_LORA_PKG_ACK_FORMAT, DEVICE_ID, DEVICE_Resp, Px)
    return pkg_ack


def unpack_Lora(recv_pkg,  recv_pkg_len):
   global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
   #device_id, location, Px, Device_next = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
   device_id, location, Px, Device_next, UID_msg = struct.unpack(_LORA_PKG_FORMAT, recv_pkg)
   return device_id, location, Px, Device_next, UID_msg


def unpack_AckLora(recv_ack,  recv_pkg_len):
   global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
   #device_id, data_null, ack_Px = struct.unpack(_LORA_PKG_ACK_FORMAT % recv_pkg_len, recv_ack)
   device_id, device_respond, ack_Px = struct.unpack(_LORA_PKG_ACK_FORMAT, recv_ack)
   return device_id, device_respond, ack_Px

def Random():
    result = (uos.urandom(1)[0] / 256) * 1000
    return int(result)


def Def_ID(lora):
    id = ubinascii.hexlify(lora.mac()).upper().decode('utf-8')
    id = id[14:16]
    return int(id, 16)

def UID_message(id_device):
    return (id_device * 1000) + Random()


def Open_Test(file_test):
    f = open (file_test,'r')
    mensaje = f.readlines()
    mensaje = [int(x) for x in mensaje]
    f.close()
    return mensaje
