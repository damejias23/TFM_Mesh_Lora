from lib.LoraPack import pack_AckLora, pack_Lora, unpack_AckLora, unpack_Lora
import os
import socket
import time
import struct
from network import LoRa
from LoraPack import *

lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

def Call_lora():
    lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)
    lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_sock.setblocking(False)
    return lora, lora_sock

def send_pack(lora_sock, id_device, location,Px, id_next):
    pck = pack_Lora(id_device, location, Px, id_next)
    lora_sock.send(pck)

def send_ack(lora_sock,id_device, Px):
    pck_ack = pack_AckLora(id_device, Px)
    lora_sock.send(pck_ack)

def recv_pack(lora_sock):
    recv_pkg = lora_sock.recv(512)
    print("Tamaño = %d" % len(recv_pkg))
    if (len(recv_pkg) > 3):
        recv_pkg_len = recv_pkg[1]
        device_id, location, My_px, Device_next = unpack_Lora(recv_pkg,  recv_pkg_len)
        rx_timestamp, rssi, snr, sftx, sfrx, tx_trials, tx_power, tx_time_on_air, tx_counter, tx_frequency = lora.stats ()
        return device_id, location, My_px, Device_next, tx_power
    elif (len(recv_pkg) < 3 and len(recv_pkg) > 1):
         recv_pkg_len = recv_pkg[1]
         device_id, ack_Px = unpack_AckLora(recv_pkg,  recv_pkg_len)
         rx_timestamp, rssi, snr, sftx, sfrx, tx_trials, tx_power, tx_time_on_air, tx_counter, tx_frequency = lora.stats ()
         return device_id, 0, ack_Px, 0, tx_power
    else:
        print ("Error en el tamaño")
        return 0, 0, 0, 0, 0




"""

def  ack(recv_pkg):
    global send_OK, id_send, ack_Px, lora
    recv_pkg_len = recv_pkg[1]
    id_send_backup = id_send
    id_send, my_id, ack_Px = unpack_AckLora(recv_pkg,  recv_pkg_len)
    print( "%d %d"%(id_send , id_recv))
    if(my_id == id_device and id_send != id_recv):
        print("Tamaño Send = %d" % len(recv_pkg))
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
            print("My id: %d - Send: %d" % (id_device, id_send))
            pck = pack_Lora(id_device, location, Px_Rx, id_send, dist)
            #pck = struct.pack(_LORA_PKG_FORMAT, id_device, location, Px_Rx, id_next)
            lora_sock.send(pck)
            #id_next, null1, Px_Tx, null2, Px_Rx = recv_pack(lora_sock)
            #print('Device: %d - Px#_Tx: %d - Px_Rx:  %s' % (id_next,  Px_Tx, Px_Rx ))
    #RECIBO RESPUESTA
            #recv_pkg = lora_sock.recv(4)
            #print("Tamaño_send = %d " % (len(recv_pkg)))

            while(send_OK == 0 and count):
                count = count - 1
            if(send_OK):
                print("Send OK")
                send_OK = 0
            else:
                print("Send failt")
            count = 100
            time.sleep(15)


def Recv():
    global lora, lora_sock, Px_Rx, id_recv, id_send, location, id_device, count, _LORA_PKG_FORMAT, _LORA_PKG_ACK_FORMAT, dist, list
    while(True):
        #Recibo
        recv_pkg = lora_sock.recv(256)
        #if(len(recv_pkg) != 0): print("Tamaño = %d" % len(recv_pkg))
        if (len(recv_pkg) > 4):
            recv_pkg_len = recv_pkg[1]
            id_next, location, My_px, id_my, dist_recv = unpack_Lora(recv_pkg,  recv_pkg_len)
            print("->%d %d" %(id_send, id_next))
            if(dist_recv > dist):
                #list = id_next
                if id_next not in list:
                    list.append(id_next)
                if(id_send != id_next):
                    id_recv = id_next
                    print("My id: %d - Recv: %d" % (id_device, id_recv))
                    rx_timestamp, rssi, snr, sftx, sfrx, tx_trials, tx_power, tx_time_on_air, tx_counter, tx_frequency = lora.stats ()
            #Envio RESPUESTA
                    pkg_ack = pack_AckLora( id_device, id_recv, Px_Rx)
                    lora_sock.send(pkg_ack)
                    count = count + 1
        elif (len(recv_pkg) > 2 and len(recv_pkg) < 4):
            ack(recv_pkg)

        #time.sleep(6)
"""
