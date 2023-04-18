
import struct
import pycurl
# Define constants for input event types
EV_KEY = 0x01
EV_SYN = 0x00

# Open the input device file
input_file = open('/dev/input/by-id/usb-MOSART_Semi._2.4G_Keyboard_Mouse-event-kbd', 'rb')



#keycodeToGrid
matrix = {
    #numlock = on
    98:'0_1', # /
    55:'0_2', # *
    14:'0_3', # <_
    #__
    71:'1_0', #7
    72:'1_1', #8
    73:'1_2', #9
    74:'1_3', #10
    # __
    75:'2_0', #4
    76:'2_1', #5
    77:'2_2', #6
    78:'2_3', #7
    #__
    79:'3_0', #1
    80:'3_1', #2
    81:'3_2', #3
    96:'3_3', # enter
    #__
    82:'4_0', # 0 ins
    83:'4_1' # . del
}

def call_api(gridCode):
    # curl -X POST -d '{ "key": "value" }' 
    # homeassistant.local:8123/api/webhook/keypad_0_1^C
    c = pycurl.Curl()
    c.setopt(pycurl.TIMEOUT_MS, 1500)
    c.setopt(pycurl.HTTPHEADER, ['Accept: application/json','Content-Type: application/json'])
    c.setopt(c.POSTFIELDS, '{ "key": "value" }')                      
    c.setopt(c.URL, 'http://homeassistant.local:8123/api/webhook/keypad?keyCode='+gridCode)
    c.perform()

    status_code = c.getinfo(pycurl.RESPONSE_CODE)
    print(status_code)
    c.close()

    return

# Loop indefinitely, reading and processing input events
while True:
    # Read the next input event
    event_data = input_file.read(16)

    # Unpack the event data into variables
    (event_time_sec, event_time_usec, event_type, event_code, event_value) = struct.unpack('iihhi', event_data)

    # Print the event data if it is a key event
    if event_type == EV_KEY:
        print(f'Keycode: {event_code}, Value: {event_value} \n')
        if event_code in matrix:
            call_api(matrix[event_code])
    # If it is a SYN event, print a newline character to separate events
    elif event_type == EV_SYN:
        print()
