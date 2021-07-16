import os
import socket
import time
import struct
import pycom
import ubinascii, network
from network import LoRa

from LoraPack import *
from env_recv import *
import _thread

#lock = _thread.allocate_lock()

# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formatted string for string
_LORA_PKG_FORMAT = "BBBBB"


# A basic ack package, B: 1 byte for the deviceId, B: 1 byte for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"

MAX_RECV = 1

modeTEST = 1

# Open a LoRa Socket, use rx_iq to avoid listening to our own messages
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)
Px_Rx = 0
id_send = 0
id_recv = 0
location = 0x01
id_device = Def_ID(lora)
thread_send = 1
thread_recv = 2
count = 100
send_OK = 0
dist = 10
list = []
list_recv = []
count_list = []



#lista ID para enviar y bloquear
ID_block = Open_Test('ID4')
ID_send = 64


def Send():
    global lora, lora_sock, Px_Rx, id_recv, id_send, location, id_device, count, send_OK, dist, ID_send, id_device, list_recv

    while(ID_send):
        #if id_send not in list:
    #ENVIO
        UID = UID_message(id_device)
        list_recv.append(UID)
        pck = pack_Lora(id_device, location, Px_Rx, ID_send, UID)
        lora_sock.send(pck)
        time.sleep(15)





def Recv():
    global lora, lora_sock, Px_Rx, id_recv, id_send, location, id_device, dist, list_recv, modeTEST
    while(True):
        #Recibo
        recv_pkg = lora_sock.recv(256)
        #if(len(recv_pkg) != 0): print("Tamaño = %d" % len(recv_pkg))
        if (len(recv_pkg) > len(_LORA_PKG_FORMAT) -1):
            recv_pkg_len = recv_pkg[1]
            id_to_send, location, My_px, id_end, UID_msg = unpack_Lora(recv_pkg,  recv_pkg_len)
            if(modeTEST):
                if id_to_send in ID_block:
                    continue
            if UID_msg in list_recv:
                continue
            else:
                list_recv.append(UID_msg)
            if(id_end == id_device):
                print("Mensaje para mi de %d" % id_to_send)
            else:
                print("Reenvio de: %d" % id_to_send)
                lora_sock.send(pack_Lora(id_device, location, My_px, id_end, UID_msg))
                #lora_sock.send(recv_pkg)
            if len(list_recv)  > 10:
                time.sleep(1)
                list_recv = []

time.sleep(10)
_thread.start_new_thread(Send, ())

_thread.start_new_thread(Recv, ())
