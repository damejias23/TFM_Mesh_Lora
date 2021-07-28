import os
import socket
import time
import struct
from network import LoRa
import uos
import ubinascii, network

_LORA_PKG_FORMAT = "!BBIBB"
_LORA_PKG_ACK_FORMAT = "!BBB"

def pack_Lora(DEVICE_ID,Device_next, UID_msg, location, Px):
    global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
    pkg = struct.pack(_LORA_PKG_FORMAT, DEVICE_ID, Device_next, UID_msg, location, Px)
    return pkg

def pack_AckLora(DEVICE_ID, DEVICE_Resp, Px):
    global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
    pkg_ack = struct.pack(_LORA_PKG_ACK_FORMAT, DEVICE_ID, DEVICE_Resp, Px)
    return pkg_ack


def unpack_Lora(recv_pkg,  recv_pkg_len):
   global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
   #device_id, location, Px, Device_next = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
   device_id, Device_next, UID_msg, location, Px = struct.unpack(_LORA_PKG_FORMAT, recv_pkg)
   return device_id, Device_next, UID_msg, location, Px


def unpack_AckLora(recv_ack,  recv_pkg_len):
   global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
   #device_id, data_null, ack_Px = struct.unpack(_LORA_PKG_ACK_FORMAT % recv_pkg_len, recv_ack)
   device_id, device_respond, ack_Px = struct.unpack(_LORA_PKG_ACK_FORMAT, recv_ack)
   return device_id, device_respond, ack_Px

def get_IDdest(recv_pkg):
    global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
    ID_send, ID_end, UID = struct.unpack_from("BBI", recv_pkg, 0)
    return ID_send, ID_end, UID


def set_IDorigen(pack, ID_sent):
    global _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT
    device_id, Device_next, UID_msg, location, Px = struct.unpack(_LORA_PKG_FORMAT, pack)
    pkg = struct.pack(_LORA_PKG_FORMAT, ID_sent, Device_next, UID_msg, location, Px)
    return pkg
    #struct.pack_into('B', pack, offset, v1, v2, ...)

def Random():
    result = (uos.urandom(1)[0] / 256) * 1000
    return int(result)


def Def_ID(lora):
    id = ubinascii.hexlify(lora.mac()).upper().decode('utf-8')
    id = id[14:16]
    return int(id, 16)

def UID_message(id_device):
    return (id_device * 1000) + Random()

def get_SendID(UID):
    SendID = UID/1000
    return int(SendID)


def Open_Test(file_test):
    f = open (file_test,'r')
    mensaje = f.readlines()
    mensaje = [int(x) for x in mensaje]
    f.close()
    return mensaje
