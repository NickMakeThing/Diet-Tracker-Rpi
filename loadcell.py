import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from hx711 import HX711
from time import sleep

def calibrate(val):
    return (((val/100)-50.8)/2)*10-135

def in_range(previous_val,val,range):
    if (val > previous_val + range or val < previous_val - range):
        return False
    else:
        return True

def check_noise(val):
    val=calibrate(val)
    if val > -100 and val < 5000:
        return True
    else:
        return False

def sense_weight(last_weight):
    start = datetime.now()
    end = start + timedelta(seconds=3)
    start_val = 99999
    hx = HX711(dout=9, pd_sck=11)
    hx.setReferenceUnit(21)
    hx.reset()
    hx.tare()
    
    while True:
        try:
            val = hx.getWeight()
            if val != 0 and check_noise(val):
                val=round(calibrate(val))
                if val < 4: 
                    print(val,end='            \r')
                    start = datetime.now()
                    end = start + timedelta(seconds=3)
                    continue
                if not in_range(start_val,val,5):
                    start_val = val
                    start = datetime.now()
                    end = start + timedelta(seconds=3)
                elif datetime.now() > end and not in_range(last_weight,val,10): 
                    last_weight = val
                    print(val,' focusing ...',end='             \r')
                    sleep(1)
                    return val
                print(val,end='             \r')

        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            sys.exit()

if __name__ == '__main__':
    last_weight=9999
    while True:
        last_weight = sense_weight(last_weight)
        print(last_weight, 'picture taken.')

