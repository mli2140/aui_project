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

elevator_dist = 10
stairs_dist = 10

elevator_count = 0
stairs_count = 0

 
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
    if(actual < dist):
        if(index == 1):
            global stairs_count
            stairs_count += 1
            file_stairs = open("stairs.txt", "a")
            file_stairs.write(time.ctime() + ": " + str(stairs_count))
            time.sleep(2)
        else:
            global elevator_count
            elevator_count += 1
            file_elevator = open("elevator.txt", "a")
            file_elevator.write(time.ctime() + ": " + str(elevator_count))
            time.sleep(2)

async def main():

    try:
        while True:
            actual_elevator = distance(GPIO_TRIGGER, GPIO_ECHO)
            actual_stairs = distance(GPIO_TRIGGER2, GPIO_ECHO2)
            
            #await asyncio.gather(
                #asyncio.to_thread(countPerson(actual_stairs, stairs_dist, 1)),
                #asyncio.sleep(2)
            #)
            #s.start()
            await countPerson(actual_stairs, stairs_dist, 1)
            await countPerson(actual_elevator, elevator_dist, 0)
            #e.start()
            
            print(f"Elevator: {elevator_count}")
            print(f"Stairs: {stairs_count}")
                
    except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()

if __name__ == '__main__':
    asyncio.run(
        main()
    )

