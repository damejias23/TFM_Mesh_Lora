from lib.LoraPack import pack_AckLora, pack_Lora, unpack_AckLora, unpack_Lora
import os
import socket
import time
import struct
from network import LoRa
from LoraPack import *

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
