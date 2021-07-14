import os
import socket
import time
import struct
import pycom
from network import LoRa

from LoraPack import *
from env_recv import *
import _thread

#lock = _thread.allocate_lock()

# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formatted string for string
_LORA_PKG_FORMAT = "BBBBB"

# A basic ack package, B: 1 byte for the deviceId, B: 1 byte for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"

MAX_RECV = 2

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
id_device = location
thread_send = 1
thread_recv = 2
count = 100
send_OK = 0
dist = 10
list = []
list_recv = []
count_list = []


def  ack(recv_pkg):
    global send_OK, id_send, ack_Px, lora
    recv_pkg_len = recv_pkg[1]
    id_send_pack, my_id, ack_Px = unpack_AckLora(recv_pkg,  recv_pkg_len)
    if(my_id == id_device and id_send_pack != id_recv):
        id_send = id_send_pack
        #print("Tamaño Send = %d" % len(recv_pkg))
        rx_timestamp, rssi, snr, sftx, sfrx, tx_trials, tx_power, tx_time_on_air, tx_counter, tx_frequency = lora.stats ()
        send_OK =  1
    elif(id_send == id_recv):
        id_send = 0


def Send():
    global lora, lora_sock, Px_Rx, id_recv, id_send, location, id_device, count, _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT, send_OK, dist, list

    while(True):
        print
        if id_send not in list:
    #ENVIO
            pck = pack_Lora(id_device, location, Px_Rx, id_send, dist)
            lora_sock.send(pck)
            print("My id: %d - Send: %d" % (id_device, id_send))
    #RECIBO RESPUESTA
            while(send_OK == 0 and count):
                count = count - 1
            if(send_OK):
                print("Send OK")
                send_OK = 0
            else:
                print("Send failt")
                id_send  = 0
            count = 100
            time.sleep(15)



def Recv():
    global lora, lora_sock, Px_Rx, id_recv, id_send, location, id_device, dist, list, list_recv, count_list
    i = 0
    while(True):
        #Recibo
        recv_pkg = lora_sock.recv(256)
        #if(len(recv_pkg) != 0): print("Tamaño = %d" % len(recv_pkg))
        if (len(recv_pkg) > 4):
            recv_pkg_len = recv_pkg[1]
            id_next, location, My_px, id_my, dist_recv = unpack_Lora(recv_pkg,  recv_pkg_len)
            if(dist_recv > dist and (id_my == id_device or id_my == 0)):
                #list = id_next


                if(id_my == 0 and len(list_recv) < MAX_RECV and id_next not in list_recv):
                    list_recv.append(id_next)
                    count_list.append(0)

                if id_next not in list:
                    list.append(id_next)

                if((id_send != id_next) and id_next in list_recv):

                    id_recv = id_next
                    count_list[list_recv.index(id_recv)] = 0
                    print("My id: %d - Recv: %d" % (id_device, id_recv))
                    rx_timestamp, rssi, snr, sftx, sfrx, tx_trials, tx_power, tx_time_on_air, tx_counter, tx_frequency = lora.stats ()
            #Envio RESPUESTA
                    pkg_ack = pack_AckLora( id_device, id_recv, Px_Rx)
                    lora_sock.send(pkg_ack)
                    i = 0
            elif id_my != id_device or id_my == 0:
                i = i + 1


            if (dist_recv < dist) and (id_next in list):
                list.remove(id_next)
                if id_next == id_recv:
                    id_recv = 0
                if id_next in list_recv:
                    count_list.pop(list_recv.index(id_next))
                    list_recv.remove(id_next)


            for j in range(len(count_list)):
                if id_next != list_recv[j]:
                    count_list[j] = count_list[j] + 1


        elif (len(recv_pkg) > 2 and len(recv_pkg) < 4):
            ack(recv_pkg)
        if MAX_RECV > 1:
            for j in range(len(count_list)):
                if (count_list[j] == 5):
                    list_recv.pop(j)
                    count_list.pop(j)
                    break
        else:

            if(i > 2):
                list_recv = []
                count_list = []
                id_my = 0
                i = 0

time.sleep(10)
_thread.start_new_thread(Send, ())

_thread.start_new_thread(Recv, ())
