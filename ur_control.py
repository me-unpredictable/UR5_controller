import socket
import time

host='192.168.251.12'
port=30002



def ur_control(cmd,exe_time=5):
    connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.connect((host,port))

    ret_msg=''
    # send command to the robot
    if(type(cmd)==str):
        cmd=((cmd+"\n").encode("utf8"))

        connection.send(cmd)
        time.sleep(exe_time) # wait for the command execution
        ret_msg=connection.recv(1024)
        ret_msg=repr(ret_msg) # convert the message to a readable text format
    else:
        print("Command Error!!!")

    return ret_msg

# function to change robot position to home

#msg=ur_control('powerdown()')
#print(msg)

#b'\x00\x00\x007\x14\xff\xff\xff\xff\xff\xff\xff\xff\xfe\x03\tURControl\x05\x0c\x00\x00\x00\x02\x00\x00\x00\x0028-06-2022, 11:30:43\x00\x00\x00\x18\x14\xff\xff\xff\xff\xff\xff\xff\xff\xfe\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x01'

def go_home(exe_time=6):
    #set robot to home position
    ur_control('movej([0,-1.57,0,-1.57,0,1.57],a=1.0,v=0.8,t=0,r=0)',exe_time)
def go_q4_j(exe_time=6):
    #move to 4th quadrent
    ur_control('movej([0,0.45,-2.0,-1.57,0,1.57],a=1,v=0.8,t=0,r=0)',exe_time)
def go_q3_j(exe_time=6):
    #move to 3th quadrent
    ur_control('movej([0,-3.5,2.0,-1.57,0,1.57],a=1,v=0.8,t=0,r=0)',exe_time)
def go_q2_j(exe_time=6):
    #move to 2nd quardrent
    ur_control('movej([0,-2.35,0.8,-1.57,0,1.57],a=1,v=0.8,t=0,r=0)',exe_time)
def go_q1_j(exe_time=6):
    #move to 1st quardrent
    ur_control('movej([0,-0.8,-0.8,-1.57,0,1.57],a=1,v=0.8,t=0,r=0)',exe_time)

def safety_check():
    # if shoulder is at 210 deg then elbow can be between 45 to 150 deg [45,150]
    # if shoulder is at 30 deg then elbow can be between -150 to 45 deg [-150,-30]
    pass



def movej_deg(base=0,shoulder=-90,elbow=0,wrist1=-90,wrist2=0,wrist3=90,exe_time=6):
    if base > 360 or base <-360:
        print('Invalid input,\n Input should be ranged between +/- 360 degree')
    else:
        # covert values to radian because movej takes values in radians
        base=(base*3.14)/180

    if shoulder > 360 or shoulder < -360:
        # note: 0 deg shoulder is align to ground (like laying flat on the ground)
        # note: -90 deg shoulder is perpendicular (center) to ground (standing straight like a pole)
        # note: 180 deg shoulder is align to ground (like laying flat on the ground)
        # be careful if you want to go outside of this range
        #--------------------------------------------------
        # Safe range: -210 deg
        #                  to
        #              30 deg
        # [30,-210] # no greater than 30
        #--------------------------------------------------
        print('Invalid input,\n Input should be ranged between +/- 360 degree')
    else:
        # covert values to radian because movej takes values in radians
        shoulder = (shoulder * 3.14) / 180

    if elbow > 360 or elbow < -360:
        # note: 0 deg elbow is perpendicular (center) to the ground (standing straight like pole)
        # note: 90 deg shoulder is align to the ground (like laying flat on the ground)
        # note: -90 deg shoulder is align to ground (like laying flat on the ground)
        # be careful if you want to go outside of this range
        print('Invalid input,\n Input should be ranged between +/- 360 degree')
    else:
        # covert values to radian because movej takes values in radians
        elbow = (elbow * 3.14) / 180
    if wrist1 > 180 or wrist1 < -270:
        # note: 0 deg wrist1 is aligned to the ground (laying on the ground)
        # note: 90 deg wrist1 is upside down to the ground (like hanging on the head)
        # note: -90 deg wrist1 is standing straight to the ground (like a straight pole)
        # note: 180 deg wrist1 is aligned to the ground (laying on the ground)
        # note: -270 deg wrist1 is upside dow to the ground (like hanging on the head)
        # be careful if you want to go outside of this range
        print('Invalid input,\n Input should be ranged between +/- 360 degree')
        exit(0)
    else:
        # covert values to radian because movej takes values in radians
        wrist1 = (wrist1 * 3.14) / 180
    if wrist2 > 180 or wrist2 < -180:
        # note: 0 deg wrist2 is looking in the front
        # note: 180 deg wrist2 is looking in the back
        # note: 90 deg wrist2 is looking in the left
        # note: -90 deg wrist2 is looking in the right
        # note: -180 deg wrist2 is looking in the back
        # be careful if you want to go outside of this range
        print('Invalid input,\n Input should be ranged between +/- 360 degree')
        exit(0)
    else:
        # covert values to radian because movej takes values in radians
        wrist2 = (wrist2 * 3.14) / 180

    if wrist3 > 360 or wrist3 <-360:
        print('Invalid input,\n Input should be ranged between +/- 360 degree')
    else:
        #note: it's like base you can have 360 rotation
        # but be careful when you rotate check your gripper or other attachment wires
        # covert values to radian because movej takes values in radians
        wrist3=(wrist3*3.14)/180

    ur_control('movej(['+str(base)+','+str(shoulder)+','+str(elbow)+','+str(wrist1)+','+str(wrist2)+','+str(wrist3)+'],a=1,v=0.8,t=0,r=0)',exe_time)

def stand_straight():
    movej_deg(base=0, shoulder=-90, elbow=0,wrist1=-90)


# movej_deg(base=0,shoulder=-90,elbow=0,wrist1=-90,wrist2=180,wrist3=90)
# movej_deg()

# wave
def wave():
    stand_straight()
    movej_deg(shoulder=30,elbow=-150,exe_time=16)
    movej_deg(shoulder=-200,elbow=150,exe_time=16)
for i in range(2):
    wave()