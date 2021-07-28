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
_LORA_PKG_FORMAT = "!BBIBB"


# A basic ack package, B: 1 byte for the deviceId, B: 1 byte for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "!BBB"

MAX_RECV = 1
MAX_BUFFER = 4

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

buffer = []


#lista ID para enviar y bloquear
if(modeTEST):
    namefile = "ID" + str(id_device)
    ID_block = Open_Test(namefile)
ID_send = 0


def Send():
    global lora, lora_sock, Px_Rx, location, ID_send, id_device, list_recv

    while(True):
        if len(buffer)>0:
            #if id_send not in list:
        #ENVIO
            send_pck = buffer.pop(0)
            id_to_send, id_end, UID_msg = get_IDdest(send_pck)
            if(id_to_send == id_device):
                lora_sock.send(send_pck)
            else:
                print("Reenvio de: %d" % id_to_send)
                pck_reenvio = set_IDorigen(send_pck, id_device)
                lora_sock.send(pck_reenvio)


def Packet_buffer():
    global Px_Rx, location, ID_send, id_device, list_recv, buffer

    while(True):
        if(ID_send):
            #if id_send not in list:
        #ENVIO
            UID = UID_message(id_device)
            list_recv.append(UID)
            pck = pack_Lora(id_device, ID_send, UID, location, Px_Rx)
            if(len(buffer) < MAX_BUFFER):
                buffer.append(pck)
            time.sleep(15)

def Recv():
    global lora, lora_sock, Px_Rx, id_recv, id_send, location, id_device, dist, list_recv, modeTEST, buffer
    #Recibo
    recv_pkg = lora_sock.recv(256)
    #if(len(recv_pkg) != 0): print("Tamaño = %d" % len(recv_pkg))
    if (len(recv_pkg) > len(_LORA_PKG_FORMAT) -1):
        recv_pkg_len = recv_pkg[1]
        id_to_send, id_end, UID_msg = get_IDdest(recv_pkg)
        if(modeTEST):
            if id_to_send in ID_block:
                return
        if UID_msg in list_recv:
            return
        else:
            list_recv.append(UID_msg)
        if(id_end == id_device):
            id_to_send, id_end, UID_msg, location, My_px  = unpack_Lora(recv_pkg,  recv_pkg_len)
            print("Mensaje para mi de %d" % get_SendID(UID_msg))
        #"""elif(id_end == 555):
        #    id_to_send, id_end, UID_msg, location, My_px  = unpack_Lora(recv_pkg,  recv_pkg_len)
        #    print("Mensaje broadcast: %d" % get_SendID(UID_msg))
        #   pck_reenvio = set_IDorigen(recv_pkg, id_device)
        #    lora_sock.send(pck_reenvio)"""
        else:
            if(len(buffer) < MAX_BUFFER):
                buffer.append(recv_pkg)


def clear():
    global list_recv
    time.sleep(200)
    list_recv = []


def lora_cb(lora):
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        #print('Lora packet received')
        Recv()
    #if events & LoRa.TX_PACKET_EVENT:
        #i=0
        #print('Lora packet sent')

lora.callback(trigger=(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT), handler=lora_cb)

time.sleep(10)
_thread.start_new_thread(Send, ())

_thread.start_new_thread(Packet_buffer, ())

#_thread.start_new_thread(Recv, ())

_thread.start_new_thread(clear,())
