import serial
import struct
import time

#Open serial connection at /dev/ttyCOM11, at 2305400 baud (datarate from IMU)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()

raw_data = ser.readline()

ctr = 0
start = int(round(time.time() * 1000))

output = open("data/accelerometer_data.csv","a+")

while True:
  rv = struct.unpack('h',ser.read(2))
  if(rv[0] == 255):
    ax_r = ser.read(2)
    ay_r = ser.read(2)
    az_r = ser.read(2)
    ser.read(2)
    gx_r = ser.read(2)
    gy_r = ser.read(2)
    gz_r = ser.read(2)

    line_end = ser.readline()
    rv = struct.unpack('h',line_end[0:2])
    #double check that the data had correct format
    ax = struct.unpack('h',ax_r)[0]
    ay = struct.unpack('h',ay_r)[0]
    az = struct.unpack('h',az_r)[0]
    gx = struct.unpack('h',gx_r)[0]
    gy = struct.unpack('h',gy_r)[0]
    gz = struct.unpack('h',gz_r)[0]
    if(rv[0] == -256):
      ax = struct.unpack('h',ax_r)[0]
      ay = struct.unpack('h',ay_r)[0]
      az = struct.unpack('h',az_r)[0]
      gx = struct.unpack('h',gx_r)[0]
      gy = struct.unpack('h',gy_r)[0]
      gz = struct.unpack('h',gz_r)[0]
      output.write(str(int(round(time.time() * 1000)))+";"+str(ax) + ";" + str(ay) + ";" + str(az) + "\n")
      print "A x,y,x: "+ str(ax)+ ", "+str(ay)+ ", "+str(az)
      print "G x,y,z: "+ str(gx) + ", "+str(gy)+ ", "+str(gz)

  else:
    data = ser.readline()

