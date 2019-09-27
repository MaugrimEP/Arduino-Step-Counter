import numpy as np
import matplotlib.pyplot as plt

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr, m_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
#return [timestamps], [x_array], [y_array], [z_array]
def read_data(filename):
  data = np.loadtxt(filename, dtype='double,double,double,double', delimiter=';', usecols=(0, 1, 2, 3), unpack=True)
  return data[0], data[1], data[2], data[3]

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr, m_arr):

  #noise reduction : remove high noise frequencies
  frequency_treshold = 3500000
  mag_fft = np.fft.fft(m_arr)
  for i in range(0,len(m_arr)):
    if abs(mag_fft[i])>frequency_treshold:
      mag_fft[i] = 0
  m_arr = np.fft.ifft(mag_fft)

  #2 - state machine
  #initialize
  current_state = "Middle"
  timestamp = dict()
  timestamp["Middle"] = None
  timestamp["Up"] = None
  timestamp["Down"] = None
  threshold_up = 7500
  threshold_down = -5500
  minimum_time_steps = 150
  #go through data
  rv = []
  for i, time in enumerate(timestamps):
    previous_state = current_state

    #change state according to data
    if m_arr[i]>threshold_up :
      current_state = "Up"
      timestamp["Down"] = None #force the dectection to begin with up
    elif m_arr[i]<threshold_down :
      current_state = "Down"
    else :
      current_state = "Middle"
    #if we do changed state, save when we did
    if(current_state != previous_state):
      timestamp[current_state] = time

    #if we've gone through all states, append the step
    if timestamp["Middle"]!=None and timestamp["Up"]!=None and timestamp["Down"]!=None :
      time_step = timestamp["Up"]

      if len(rv)==0 or time_step - rv[-1] > minimum_time_steps:
        rv.append(time_step)

      #clean the timestamps
      timestamp["Middle"] = None
      timestamp["Up"] = None
      timestamp["Down"] = None

  return rv

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 50000 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main(filename):
  #read data from a measurement file
  timestamps, x_array, y_array, z_array = read_data(f"data/{filename}")

  #magnitude array calculation
  m_array = []
  for i, x in enumerate(x_array):
    m_array.append(magnitude(x_array[i],y_array[i],z_array[i]))

  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  st = count_steps(timestamps, x_array, y_array, z_array, m_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array,m_array)

main("accelerometer_data.csv")
main("accelerometer_data_easy.csv")
main("accelerometer_data_medium.csv")
main("accelerometer_data_very_hard.csv")