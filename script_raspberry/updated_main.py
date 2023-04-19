#Libraries
import RPi.GPIO as GPIO
import threading
import time
import asyncio
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins Ultrasonic 1
GPIO_TRIGGER = 11
GPIO_ECHO = 12

#set GPIO Pins Ultrasonic 2
GPIO_TRIGGER2 = 18
GPIO_ECHO2 = 13

#set GPIO direction (IN / OUT) Ultrasonic 1
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#set GPIO direction (IN / OUT) Ultrasonic 2
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

elevator_dist = 50
stairs_dist = 100

elevator_count = 0
stairs_count = 0

stairs_active = True
elevator_active = True

alpha = 0.8

 
def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

    return distance

async def countPerson(actual, dist, index):
    global stairs_active
    global stairs_count
    global elevator_active
    global elevator_count

    if(actual < dist):
        if(index == 1 and stairs_active):
            stairs_active = False
            stairs_count += 1
            file_stairs = open("stairs.txt", "a")
            file_stairs.write(time.ctime() + ": " + str(stairs_count))
        elif(index ==2 and elevator_active):
            elevator_active = False
            elevator_count += 1
            file_elevator = open("elevator.txt", "a")
            file_elevator.write(time.ctime() + ": " + str(elevator_count))
    elif(actual > dist * 1.1):
        if(index == 1):
            stairs_active = True
        elif(index == 2):
            elevator_active = True
    

async def main():
    actual_elevator = 120
    actual_stairs = 200
    try:
        while True:
            current_stairs  = distance(GPIO_TRIGGER2, GPIO_ECHO2)
            current_elevator = distance(GPIO_TRIGGER, GPIO_ECHO)
            
            if(current_elevator > 0):
                actual_elevator = alpha * current_elevator + ((1- alpha) * actual_elevator)
            if(current_stairs > 0):
                actual_stairs = alpha * current_stairs + ((1- alpha) * actual_stairs)
            

            await countPerson(actual_stairs, stairs_dist, 1)
            await countPerson(actual_elevator, elevator_dist, 2)
            
            print(f"Elevator: {elevator_count}")
            print(f"Stairs: {stairs_count}")
            
            print(f"Elevator: {actual_elevator}")
            print(f"Stairs: {actual_stairs}")                
    except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

if __name__ == '__main__':
    asyncio.run(
        main()
    )


