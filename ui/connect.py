import serial, time

# Set up commlink
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

print("available ports:")
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

# If there is more than one port, ask user to choose
if len(ports) > 1:
    port = input("select port> ")
    if port == "": port = sorted(ports)[0][0]
else:
    ports = []
    while len(ports) == 0:
        ports = serial.tools.list_ports.comports()
    port = ports[0][0]

time.sleep(1)

zircon = serial.Serial(port=port, baudrate=115200, timeout=.1)
zircon.setDTR(False)
zircon.setRTS(False)

current_state = None

def write_num(num):
    global current_state
    # Only write on state changes
    if num == current_state:
        return
    data = (str(num)).encode("UTF-8")
    zircon.write(data)
    current_state = num

def reconnect():
    global zircon
    try:
        zircon = serial.Serial(port=port, baudrate=115200, timeout=.1)
    except:
        pass