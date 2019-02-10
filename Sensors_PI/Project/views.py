from django.shortcuts import HttpResponse
from django.shortcuts import render
import os
import glob
import time
import time

from picamera import PiCamera
from .models import Project

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c 
        
        
store_data = list()
store_time = list()
status = list()

status.append("Both Working")

if os.path.exists("/home/pi/Desktop/Project/Sensors_PI/media/image.jpg"):
	os.remove("/home/pi/Desktop/Project/Sensors_PI/media/image.jpg")
	
def capture_image():
	try:
		camera = PiCamera() 
		camera.capture('/home/pi/Desktop/Project/Sensors_PI/media/image.jpg')
		camera.close()
		time.sleep(2)
		
	except:
		time.sleep(1)
		camera = PiCamera() 
		camera.capture('/home/pi/Desktop/Project/Sensors_PI/media/image.jpg')
		camera.close()
	
	finally:
		camera.close()

def home_page(request):
	
	action = request.POST.get('action', False)
	
	if action == False:
		pass
	elif action == "Stop _thermal":
		status.append("Stop _thermal")
	elif action == "Stop_Camera":
		status.append("Stop_Camera")
	elif action =="Refresh":
		status.append("Refresh")
		
	
	if status[-1] == "Both Working":
		store_data.append(read_temp())
		store_time.append(time.ctime())
		capture_image()
		result = "Both Sensors are working."
		return render(request,"HomePage.html",{"result":result,'data_therm':zip(store_data, store_time)})
	
	elif status[-1] == "Stop _thermal":
		if status[-2]=="Stop_Camera":
			result = "Both Sensors have stopped working."
			return render(request,"HomePage.html",{"result":result,'data_therm':zip(store_data, store_time)})	
		capture_image()
		result = "Thermal Sensor has stopped."
		return render(request,"HomePage.html",{"result":result,'data_therm':zip(store_data, store_time)})
		
	elif status[-1] == "Stop_Camera":
		if status[-2] == "Stop _thermal":
			result = "Both Sensors have stopped working."
			return render(request,"HomePage.html",{"result":result,'data_therm':zip(store_data, store_time)})
			
		store_data.append(read_temp())
		store_time.append(time.ctime())
		result = "Camera Sensor has stopped."
		return render(request,"HomePage.html",{"result":result,'data_therm':zip(store_data, store_time)})
		
	elif status[-1] == "Refresh":
		del store_data[:]
		del store_time[:]
		os.remove("/home/pi/Desktop/Project/Sensors_PI/media/image.jpg")
		status.append("Both Working")
		result = "Both Sensors are working."
		return render(request,"HomePage.html",{"result":result,'data_therm':zip(store_data, store_time)})

		
		
		
		#{{ redirect_url }}


def home(request):	
	
	action=request.POST.get('action', False)
	
	if action == 'Thermal':
		store_data.append(read_temp())
		store_time.append(time.ctime())
		return render(request,"Home.html",{'data_therm':zip(store_data, store_time)})
		
	elif action == 'Image':	
		camera = PiCamera() 
		camera.capture('/home/pi/Desktop/Project/Sensors_PI/media/image.jpg')
		camera.close()
		return render(request,"Home.html",{'data_therm':zip(store_data, store_time)})
		
	elif action == 'Refresh':
		del store_data[:]
		del store_time[:]
		os.remove("/home/pi/Desktop/Project/Sensors_PI/media/image.jpg")
		return render(request,"Home.html")

	else:
		return render(request,"Home.html")

