import serial
import binascii

class rfid:
    
    ser = serial.Serial()

    def __init__( self, port = "/dev/ttyUSB0", baudrate = 115200 ):
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = 1.0

    def isOpen( self ):
        return self.ser.is_open

    def rfidOpen( self ):
        return self.ser.open()
    
    def rfidClose( self ):
        return self.ser.close()

    def getPort( self ):
        return self.ser.port

    def setPort( self, port ):
        self.ser.port = port

    def getBaudrate( self ):
        return self.ser.baudrate

    def setBaudrate( self, baudrate ):
        self.ser.baudrate = baudrate

    def sendCom( self, hexCommand ):
        self.ser.write( serial.to_bytes( hexCommand ) )
        result = ''
        while 1:
            result = self.ser.readline()
            if( self.ser.in_waiting == 0 ):
                break
        return binascii.hexlify( result ).decode('utf-8')

    def getVersion( self ):
        command = [ 0x53, 0x57, 0x00, 0x03, 0xff, 0x10, 0x44 ]
        result = self.sendCom( command )
        return result

    def getTagID( self ):
        command = [ 0x53, 0x57, 0x00, 0x0a, 0xff, 0x02, 0x01, 0x02, 0x06, 0x00, 0x00, 0x00, 0x00, 0x42 ]
        result = self.sendCom( command )
        if( len( result ) >= 38 ):
            if( result[:4] == '4354' and result[13] == '1' ):
                return result[14:38].upper()
            else:
                return '0'
        else:
            return '0'
