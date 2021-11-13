#!/usr/bin/env python3
import os
import sys
import time
import random
import _thread

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from python import Panda  # noqa: E402

# This script is intended to be used in conjunction with the echo_loopback_test.py test script from panda jungle.
# It sends a reversed response back for every message received containing b"test".

def heartbeat_thread(p):
  while True:
    try:
      p.send_heartbeat()
      time.sleep(0.5)
    except Exception:
      continue

def reader_thread(p):
  while True:
    incoming = p.can_recv()
    for message in incoming:
      address, unused, data, bus = message
      msgs[bus]+=1
      if PRINT_MSGS: print(address, unused, data, bus)

# Resend every CAN message that has been received on the same bus, but with the data reversed
if __name__ == "__main__":
  pandas = Panda.list()
  if len(pandas) < 2:
    raise Exception("Need minimum 2 pandas!")
  print(f"Found pandas, using first in the list {pandas[0]}")
  p = Panda(pandas[0])

  _thread.start_new_thread(heartbeat_thread, (p,))
  p.set_can_data_speed_kbps(0, 3000)
  p.set_can_data_speed_kbps(1, 3000)
  p.set_can_data_speed_kbps(2, 3000)
  p.set_can_speed_kbps(0, 500)
  p.set_can_speed_kbps(1, 500)
  p.set_can_speed_kbps(2, 500)
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT) # SAFETY_ELM327
  p.set_power_save(False)

  msg_count=1
  stop = 500
  TIMEOUT=1000
  msgs={0:0, 1:0, 2:0, 128:0, 129:0, 130:0}
  sent_msgs = {0:0, 1:0, 2:0}
  elapsed_s = 0
  thr = 0
  READBACK_BUSES = True
  PRINT_MSGS = False

  _thread.start_new_thread(reader_thread, (p,))

  while True:
    start_time = time.time()

    address = random.randint(10, 0x1FFFFFFD) # 2047 for non-extended address
    #address = 0x1FFFFFFD
    #address = 0x18DB33F1 # ELM327 allowed address
    #address = 256

    # p.can_send_many([
    #   (address, 0, b'test0001', 0),
    #   (address, 0, b'test0002', 0),
    #   (address, 0, b'test0003', 0),
    #   (address, 0, b'test0004', 0),
    #   (address, 0, b'test006', 0),
    #  ]*msg_count, timeout=TIMEOUT)
    #data = bytes(f"test{random.randint(1000, 9999)}", encoding="utf-8")
    data1 = bytes(f"{random.choice(['t','te','tes','test'])}{random.randint(1, 9999)}", encoding="utf-8")
    data2 = bytes(f"{random.choice(['t','te','tes','test'])}{random.randint(1, 9999)}", encoding="utf-8")
    data3 = bytes(f"{random.choice(['t','te','tes','test'])}{random.randint(1, 9999)}", encoding="utf-8")
    #data = bytes(f"Sending this awesome long long CAN FD 64 bytes message at 6Mbps!", encoding="utf-8")

    ## ==================================================
    if msg_count <= stop:
      try:
        p.can_send_many([(address, 0, data1, 0), (address, 0, data2, 1), (address, 0, data3, 2)] * msg_count, timeout=TIMEOUT)
        sent_msgs[0]+=msg_count
        sent_msgs[1]+=msg_count
        sent_msgs[2]+=msg_count
      except Exception as e:
        print("Got send timeout! Reseting CANs and retrying")
        # p.set_can_speed_kbps(0, 500)
        # p.set_can_speed_kbps(1, 500)
        # p.set_can_speed_kbps(2, 500)
    ## ==================================================
    #data = bytes(f"{random.choice(['t','te','tes','test'])}{random.randint(1, 9999)}", encoding="utf-8")
    #p.can_send_many([(address, 0, data, 0)] * msg_count, timeout=TIMEOUT)
    #msgs[0]+=msg_count
    ## ==================================================
    #data = bytes(f"{random.choice(['t','te','tes','test'])}{random.randint(1, 9999)}", encoding="utf-8")
    #p.can_send_many([(address, 0, data, 1)] * msg_count, timeout=TIMEOUT)
    #msgs[1]+=msg_count
    ## ==================================================
    #data = bytes(f"{random.choice(['t','te','tes','test'])}{random.randint(1, 9999)}", encoding="utf-8")
    #p.can_send_many([(address, 0, data, 2)] * msg_count, timeout=TIMEOUT)
    #msgs[2]+=msg_count

    #time.sleep(0.1)

    elapsed_s += time.time()-start_time

    #print(msg_count)


    if elapsed_s >= 1:
      print(f"Sent: {sent_msgs}")
      print(f"Returned: {msgs}")
      elapsed_s=0
      msg_count += 1
