import time
import RPi.GPIO as GPIO
import datetime
import os
import glob

def read_temp_raw():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	 
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
	
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	
	temp_pos = lines[1].find("t=")
	temperature = lines[1][temp_pos:temp_pos+7]    
	temperature_cut = temperature[2:]

	temperature_float = float(temperature_cut)
	return temperature_float/1000
	

def relayOn(switch: bool):
	relay_ch = 21
	try:
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(relay_ch, GPIO.OUT)
		
		
		if switch == True:
			GPIO.output(relay_ch, GPIO.LOW)
			print("relay ON.")
			
		if switch == False:
			GPIO.output(relay_ch, GPIO.HIGH)
			print("relay OFF.")

			
	except:
		print("error")
	
	


def verwamingselementAan():
	relayOn(True)

def verwamingselementUit():
	relayOn(False)
	
# de gebruiker vult de gewenste temperatuur in.
gewensteTemperatuur = int(input('vul gewenste temperatuur in: '))
print(f'temperatuur wordt: {gewensteTemperatuur}°C')

while True:
	# meet de huidige temperatuur van het water
	waterTemperatuur = read_temp_raw()
	print(f'water temperatuur is: {waterTemperatuur}°C')
	# als temperatuur lager is dan gewenste temperatuur
	if waterTemperatuur < gewensteTemperatuur:
		# dan: schakel verwarmingselement aan
		verwamingselementAan()
	# anders: schakel verwarmingselement uit
	else :
		verwamingselementUit()
	# wacht een paar seconden
	
	
	time.sleep(0.5)
	# herhaal r. 14-23
	
GPIO.cleanup()

