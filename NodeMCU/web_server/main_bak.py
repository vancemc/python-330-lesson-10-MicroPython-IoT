try:
    import usocket as socket
except:
    import socket

response_template = """HTTP/1.0 200 OK

%s
"""

e404_response_template = """HTTP/1.0 404 NOT FOUND

<html>
 <body>
 <h1>404</h1>
 <p>%s</p>
 </body>
 </html>
"""

e500_response_template = """HTTP/1.0 500 INTERNAL SERVER ERROR

%s
"""
import logging
import time as t
import machine
import ntptime, utime
from machine import RTC, Pin

logging.basicConfig(level=logging.INFO)

logging.info("Begin main.py initializations.")

pin9_SD2 = Pin(9, Pin.OUT)

ntptime.timeout = 10

# seconds = ntptime.time()
# rtc = RTC()
# rtc.datetime(utime.localtime(seconds))

adc = machine.ADC(0)

def time():
    
    response = response_template & 'Disabled dute to ntptime timeouts.'
    
    try:
        
        seconds = ntptime.time()
        rtc = RTC()
        rtc.datetime(utime.localtime(seconds))
        
        body = """<html>
     <body>
     <h1>Time</h1>
     <p>%s</p>
     </body>
     </html>
        """ % str(rtc.datetime())
        
        response = response_template % body
        
    except Exception as e:
        
        response = e500_response_template % f'Server error: {e}'

    return response

def dummy():
    body = "This is a dummy endpoint"
    return response_template % body

def light_on():
     pin9_SD2.value(1)
     body = "You turned a light on!"
     return response_template % body

def light_off():
     pin9_SD2.value(0)
     body = "You turned a light off!"
     return response_template % body

handlers = {
    'time': time,
    'dummy': dummy,
    'light_on': light_on,
    'light_off': light_off,
}

def main():
    
    logging.info("Entering main(). Initializing web socket.")
    
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    keep_running = False
    
    while keep_running:
            
        logging.info("main(). Begin request processing loop.")
        
        res = s.accept()
        client_s = res[0]
        # client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        # The first line of a request looks like "GET /arbitrary/path/ HTTP/1.1".
        # This grabs that first line and whittles it down to just "/arbitrary/path/"
        try:
                
            path = req.decode().split("\r\n")[0].split(" ")[1]

            # Given the path, identify the correct handler to use
            handler = handlers[path.strip('/').split('/')[0]]

            response = handler()
                
        except KeyError:
                
            if path is None or len(path) < 1:
                    
                path = 'Resource or page'
                
            response = e404_response_template % f'404 {path} not found.'
            
        except Exception as e:
                
            response = e500_response_template % 'An internal server error occured.'
                
        # A handler returns an entire response in the form of a multi-line string.
        # This breaks up the response into single strings, byte-encodes them, and
        # joins them back together with b"\r\n". Then it sends that to the client.
        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()
            

main()