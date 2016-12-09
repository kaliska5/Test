import sys
import linecache
from PyQt4 import QtCore, QtGui
import string
from serial.tools import list_ports
import serial
 
#----------------------------------------------------------------------

class MainWindow(QtGui.QMainWindow):
 
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setGeometry(0, 0, 1300, 900)
		self.setWindowTitle('Mastech RLC')
		self.setAutoFillBackground(True)
		font = QtGui.QFont()
		font.setPointSize(100)
		font_l = QtGui.QFont()
		font_l.setPointSize(20)
		font_c = QtGui.QFont()
		font_c.setPointSize(14)
        
        
		self.lcd = QtGui.QLCDNumber(self)
		self.lcd.setGeometry(30, 40, 800, 500)
		self.lcd.setNumDigits(6)
 
		self.upper_ohm_edit = QtGui.QLineEdit(self)
		self.upper_ohm_edit.setGeometry(450, 550, 100, 30)
		self.upper_ohm_edit.setEnabled(False)
 
		self.lower_ohm_edit = QtGui.QLineEdit(self)
		self.lower_ohm_edit.setGeometry(450, 600, 100, 30)
		self.lower_ohm_edit.setEnabled(False)

		self.upper_ohm_label = QtGui.QLabel(self)
		self.upper_ohm_label.setText("Granica dolna:")
		self.upper_ohm_label.setGeometry(350, 540, 100, 50)
 
		self.lower_ohm_label = QtGui.QLabel(self)
		self.lower_ohm_label.setText("Granica g"+u'\u1F78'+"rna:")
		self.lower_ohm_label.setGeometry(350, 590, 100, 50)
        
		self.button_group = QtGui.QButtonGroup(self)
		self.coil1=QtGui.QRadioButton(self)
		self.coil1.setFont(font_c)
		self.coil1.setText("AWEX 50mH")
		self.coil1.setGeometry(50,550,400,30)
		self.coil1.pressed
		self.button_group.addButton(self.coil1)
		self.connect(self.coil1,QtCore.SIGNAL("clicked()"),self.awex50)
        
		self.coil2=QtGui.QRadioButton(self)
		self.coil2.setFont(font_c)
		self.coil2.setText("AWEX 67mH")
		self.coil2.setGeometry(50,590,400,30)
		self.button_group.addButton(self.coil2)
		self.connect(self.coil2,QtCore.SIGNAL("clicked()"),self.awex67)
        
		self.coil3=QtGui.QRadioButton(self)
		self.coil3.setFont(font_c)
		self.coil3.setText("BATERTECH 50mH")
		self.coil3.setGeometry(50,630,400,30)
		self.button_group.addButton(self.coil3)
		self.connect(self.coil3,QtCore.SIGNAL("clicked()"),self.bat50)
        
		self.ohm = QtGui.QLabel(self)
		self.ohm_l= QtGui.QLabel(self)
		self.ohm_l2 = QtGui.QLabel(self)
		self.achtung = QtGui.QLabel(self)
		self.unit_label = QtGui.QLabel(self)
        
		self.ohm.setGeometry(1200, 320, 100, 120)
		self.ohm.setFont(font)
        
		self.ohm_l.setFont(font_l)
		self.ohm_l2.setFont(font_l)
        
       
		self.unit_label.setFont(font)
		self.unit_label.setGeometry(900,290,300,120)
		self.unit_label.setText("mH")
        
		self.ohm_l.setGeometry(200,550,50,50)
		self.ohm_l2.setGeometry(200,600,50,50)
		self.limit_up = '0'
		self.limit_down = '0'
        
		self.lower_ohm_edit.setText(self.limit_down)
		self.upper_ohm_edit.setText(self.limit_up)
		self.Tim = QtCore.QTimer()
		QtCore.QObject.connect(self.Tim, QtCore.SIGNAL("timeout()"), self.update_values)
		self.Tim.start(100)

	def awex50(self):
		
		self.lower_ohm_edit.setText("45")
		self.upper_ohm_edit.setText("57.5")

       
	def awex67(self):
		self.lower_ohm_edit.setText("60.3")
		self.upper_ohm_edit.setText("77.05")


       
	def bat50(self):
		self.lower_ohm_edit.setText("45")
		self.upper_ohm_edit.setText("55")

      
       
       
	def red_window(self):
		palette_red = QtGui.QPalette()
		palette_red.setColor(QtGui.QPalette.Background, QtCore.Qt.red)
		self.setPalette(palette_red)
 
	def green_window(self):
		palette_green = QtGui.QPalette()
		palette_green.setColor(QtGui.QPalette.Background, QtCore.Qt.green)
		self.setPalette(palette_green)
 
	def update_values(self):

		self.rlc_bridge = Device("/dev/ttyUSB0")
		temp_read = self.rlc_bridge.read_value();
		if temp_read[5] == '8':
			temp = float(temp_read[1]+temp_read[2]+temp_read[3]+temp_read[4])/100
			temp2 = temp
		else:
			temp = float(temp_read[2]+temp_read[3]+temp_read[4])/10
			temp2 = temp

		self.lcd.display(temp)
		a=self.upper_ohm_edit.text()
		b=self.lower_ohm_edit.text()
		a= float(a)
		b=float(b)
		print a
		print b

			
		if temp2 < a and temp2 > b:
			self.green_window()
			self.repaint()
		else:
			self.red_window()
			self.repaint()
		
#----------------------------------------------------------------------
 
class Device():
 
    def __init__(self,device):
        self.device = device        
        self.data = 0
 
        
        
    def read_value(self):
        
        
        self.connection = serial.Serial(self.device,19200,7,timeout=1)
        self.data = self.connection.readline()
        self.connection.close()
        print self.data
        print self.data[1]+self.data[2]+self.data[3]+self.data[4]
        try:
            return self.data
        except:
            pass
 
    def close_port(self):
        self.connection.close() 
        return 0
 
#----------------------------------------------------------------------
 
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
