from machine import Pin,SPI,PWM
import framebuf
import time
import os

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

led = Pin("LED", Pin.OUT)
led_status = ''
led.off()

class LCD_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch3()
    #color BRG
    LCD.fill(LCD.black)
    LCD.show()
    

    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
    keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)
    
    up = Pin(2,Pin.IN,Pin.PULL_UP)
    down = Pin(18,Pin.IN,Pin.PULL_UP)
    left = Pin(16,Pin.IN,Pin.PULL_UP)
    right = Pin(20,Pin.IN,Pin.PULL_UP)
    ctrl = Pin(3,Pin.IN,Pin.PULL_UP)
    
    while(True):
        # Wipe screen on each loop
        LCD.rect(0,0,240,240,0x0000, True)
        # Green background
        LCD.rect(0,0,150,150,0x001f, True)
        # White outline around green background
        LCD.rect(0,0,150,150,0xffff, False)
        # Blue background
        LCD.rect(0,151,150,150,0xf800, True)
        
        # Button A
        LCD.text('BUTTON A', 175, 20, 0xffff)
        LCD.rect(170,13,100,20,0x07E0, False)
        
        LCD.text('BUTTON B', 175, 80, 0xffff)
        LCD.rect(170,73,100,20,0x07E0, False)
        
        LCD.text('BUTTON X', 175, 140, 0xffff)
        LCD.rect(170,133,100,20,0x07E0, False)
        
        LCD.text('BUTTON Y', 175, 200, 0xffff)
        LCD.rect(170,193,100,20,0x07E0, False)
        
        # Actions to perform when button or joystick is pressed
        if keyA.value() == 0:
            LCD.rect(170,13,100,20,0x07E0, True)
            led.on()
            
        if keyB.value() == 0:
            LCD.rect(170,73,100,20,0x07E0, True)
            led.off()

        if keyX.value() == 0:
            LCD.rect(170,133,100,20,0x07E0, True)
            led.on()
            
        if keyY.value() == 0:
            LCD.rect(170,193,100,20,0x07E0, True)
            led.off()
 
        if(up.value() == 0):
            LCD.text('UP', 55, 180, 0xffff)
            led.on()

        if(down.value() == 0):
            LCD.text('DOWN', 48, 220, 0xffff)
            led.off()
            
        if(left.value() == 0):
            LCD.text('LEFT', 0, 200, 0xffff)
        
        if(right.value() == 0):
            LCD.text('RIGHT', 100, 200, 0xffff)
        
        if(ctrl.value() == 0):
            LCD.text('CTR', 50, 200, 0xffff)

        if led.value() == 0:
            led_status = "OFF"
        if led.value() == 1:
            led_status = "ON"

        # Draw lines of 0text in upper left corner of screen
        LCD.text(f"LED: {led_status}", 10, 10, 0xffff)
        LCD.text(f"LED: {led_status}", 10, 30, 0xffff)
        LCD.text(f"LED: {led_status}", 10, 50, 0xffff)
        LCD.text(f"LED: {led_status}", 10, 70, 0xffff)
        LCD.text(f"LED: {led_status}", 10, 90, 0xffff)
        LCD.text(f"LED: {led_status}", 10, 110, 0xffff)
        LCD.text(f"LED: {led_status}", 10, 130, 0xffff)
        
        LCD.show()
        

