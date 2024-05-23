# python-330-lesson-10-MicroPython-IoT
python 330 lesson 10 MicroPython IoT

Notes:

Local comm port assigned: COM5

WebREPL default device url: ws://192.168.4.1:8266

WiFi router DHCP assigned address: ws://192.168.254.22:8266



Use puTTY console to run MicroPython through USB connection

To enable WiFi via puTTY console:

    >>> import webrepl_setup

    Connect via computer WiFi connection

    Run WebREPL.html

Wireless access point SID: MicroPython-381b3c

- Overwrite boot.py in python shell:

with open("boot.py", "w") as f:
    f.write("import gc\r\nimport webrepl\r\nwebrepl.start()\r\ngc.collect()")


- List file contents:

with open("main.py") as f:
    print(f.read())

Troubleshooting:

- WebREPL can't connect:
-	Check WiFi connection from computer

- Flash progress timeout:					
    - Disconnect ESP8266 from USB and reconnect, retry flash







