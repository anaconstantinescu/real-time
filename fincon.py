import sys
from PyQt4 import QtGui, QtCore
from ftplib import FTP
from time import gmtime, strftime
import serial.tools.list_ports
import numpy as np
import pyqtgraph as pg
import serial
import os
import urllib2




class FinCon(QtGui.QWidget):

    data = [0]
    data2 = [0]
    model = [0]
    trig = [0]
    trig2 = [0]
    repetari = 0
    tura = 0
    port = ""

    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.initUI()

#   Create folder for files if not exists
        if not os.path.exists("files"):
            os.makedirs("files")


#   Define updating plot
        self.p1 = self.plotGW.addPlot()
        self.p1.setXRange(0,10000,padding=0)
        self.p1.setYRange(0,150,padding=0)
        self.curve = self.p1.plot(pen='y')
        self.curve2 = self.p1.plot(pen='w')
        self.curve3 = self.p1.plot(pen='r')

#   Define timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

#   Event listener
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.stopBtn.clicked.connect(self.stopBtnClicked)
        
        pg.QtGui.QApplication.instance().exec_()
        
    def initUI(self):
  
#   Define elements      
        numeLbl = QtGui.QLabel('Nume')
        senzorLbl = QtGui.QLabel('Alege Senzor')
        repetariLbl = QtGui.QLabel('Nr Repetari')
        validRepetari = QtGui.QIntValidator(1,500)
        validDurata = QtGui.QIntValidator(1,99)
        validSensibil = QtGui.QIntValidator(1,999)

        self.labelComBox = QtGui.QLabel('Model')
        self.labelSensibilitate = QtGui.QLabel('Alege sensibilitate')
        self.labelNrTrepte = QtGui.QLabel('Numar trepte')
        self.labelTreapta1 = QtGui.QLabel('Treapta 1')
        self.labelTipModel1 = QtGui.QLabel('Alege Model')
        self.labelDurataModel1 = QtGui.QLabel('Durata Model')
        self.labelSensibilitateInitModel1 = QtGui.QLabel('Sensibilitate Initiala')
        self.labelTreapta2 = QtGui.QLabel('Treapta 2')
        self.labelTipModel2 = QtGui.QLabel('Alege Model')
        self.labelDurataModel2 = QtGui.QLabel('Durata Model')
        self.labelSensibilitateInitModel2 = QtGui.QLabel('Sensibilitate Initiala')
        self.labelTreapta3 = QtGui.QLabel('Treapta 3')
        self.labelTipModel3 = QtGui.QLabel('Alege Model')
        self.labelDurataModel3 = QtGui.QLabel('Durata Model')
        self.labelSensibilitateInitModel3 = QtGui.QLabel('Sensibilitate Initiala')
        self.labelTreapta4 = QtGui.QLabel('Treapta 4')
        self.labelTipModel4 = QtGui.QLabel('Alege Model')
        self.labelDurataModel4 = QtGui.QLabel('Durata Model')
        self.labelSensibilitateInitModel4 = QtGui.QLabel('Sensibilitate Initiala')
        
        self.numeLineEdit = QtGui.QLineEdit()
        self.senzorComBox = QtGui.QComboBox()
        self.senzorComBox.addItems(['Senzor Superior', 'Senzor Lateral'])
        self.repetariInputDialog = QtGui.QLineEdit()
        self.repetariInputDialog.setValidator(validRepetari)
        self.startBtn = QtGui.QPushButton('Start')
        self.stopBtn = QtGui.QPushButton('Stop')

        self.sensibilComBox = QtGui.QComboBox()
        self.sensibilComBox.addItems(['50', '100', '150', '300', '600', '1000'])
        self.modelComBox = QtGui.QComboBox()
        self.modelComBox.addItems(['Alege', 'Da', 'Nu'])
        self.nrTrepteComBox = QtGui.QComboBox()
        self.nrTrepteComBox.addItems(['1', '2', '3','4'])
#        self.model1ComBox = QtGui.QComboBox()
#        self.model1ComBox.addItems(['Alege','Platou'])
        self.durataModel1InputDialog = QtGui.QLineEdit()
        self.durataModel1InputDialog.setValidator(validDurata)
        self.sensibilitInitModel1 = QtGui.QLineEdit()
        self.sensibilitInitModel1.setValidator(validSensibil)
#        self.model2ComBox = QtGui.QComboBox()
#        self.model2ComBox.addItems(['Alege','Platou'])
        self.durataModel2InputDialog = QtGui.QLineEdit()
        self.durataModel2InputDialog.setValidator(validDurata)
        self.sensibilitInitModel2 = QtGui.QLineEdit()
        self.sensibilitInitModel2.setValidator(validSensibil)
#        self.model3ComBox = QtGui.QComboBox()
#        self.model3ComBox.addItems(['Alege','Platou'])
        self.durataModel3InputDialog = QtGui.QLineEdit()
        self.durataModel3InputDialog.setValidator(validDurata)
        self.sensibilitInitModel3 = QtGui.QLineEdit()
        self.sensibilitInitModel3.setValidator(validSensibil)
        self.model4ComBox = QtGui.QComboBox()
        self.model4ComBox.addItems(['Alege','Platou'])
        self.durataModel4InputDialog = QtGui.QLineEdit()
        self.durataModel4InputDialog.setValidator(validDurata)
        self.sensibilitInitModel4 = QtGui.QLineEdit()
        self.sensibilitInitModel4.setValidator(validSensibil)

        self.plotGW = pg.GraphicsWindow(title="FinCon")
        
        self.repLbl = QtGui.QLabel('')
        self.turaLbl = QtGui.QLabel('')
        pg.setConfigOptions(antialias=True)

#   Define Layout
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(numeLbl, 1, 0)
        self.grid.addWidget(self.numeLineEdit, 1, 1)
        self.grid.addWidget(senzorLbl, 2, 0)
        self.grid.addWidget(self.senzorComBox, 2, 1)
        self.grid.addWidget(repetariLbl, 3, 0)
        self.grid.addWidget(self.repetariInputDialog, 3, 1)
        self.grid.addWidget(self.labelComBox, 4, 0)
        self.grid.addWidget(self.modelComBox, 4, 1)
        self.grid.addWidget(self.plotGW, 2, 2, 25, 3)
        self.grid.addWidget(self.startBtn, 26, 0)
        self.grid.addWidget(self.stopBtn, 26, 1)
        self.grid.addWidget(self.repLbl, 1, 2)
        self.grid.addWidget(self.turaLbl, 1, 3)
        
        self.modelComBox.currentIndexChanged.connect(self.afisarModel)


        self.setLayout(self.grid) 
        self.showMaximized()
        
        width = self.startBtn.width()
        self.stopBtn.setMaximumWidth(int(width))
        self.startBtn.setMaximumWidth(int(width))
        self.senzorComBox.setMaximumWidth(150)
        self.repetariInputDialog.setMaximumWidth(20)
        self.sensibilComBox.setMaximumWidth(150)
        self.modelComBox.setMaximumWidth(150)
        self.numeLineEdit.setMaximumWidth(150)
        self.durataModel1InputDialog.setMaximumWidth(20)
        self.durataModel2InputDialog.setMaximumWidth(20)
        self.durataModel3InputDialog.setMaximumWidth(20)
        self.durataModel4InputDialog.setMaximumWidth(20)
        self.sensibilitInitModel1.setMaximumWidth(50)
        self.sensibilitInitModel2.setMaximumWidth(50)
        self.sensibilitInitModel3.setMaximumWidth(50)
        self.sensibilitInitModel4.setMaximumWidth(50)
        
        self.setWindowTitle('FinCon 2.4')    
        self.show()

    def afisarModel(self):
        if(int(self.modelComBox.currentIndex()) == 1):

            self.grid.addWidget(self.labelNrTrepte, 5, 0)
            self.grid.addWidget(self.nrTrepteComBox, 5, 1)  
            self.grid.addWidget(self.labelTreapta1, 6, 0)
#            self.grid.addWidget(self.labelTipModel1, 7, 0)
            self.grid.addWidget(self.labelDurataModel1, 7, 0)
            self.grid.addWidget(self.labelSensibilitateInitModel1, 8, 0)
#            self.grid.addWidget(self.labelSensibilitateFinalaModel1, 10, 0)
            self.grid.addWidget(self.labelTreapta2, 9, 0)
#            self.grid.addWidget(self.labelTipModel2, 11, 0)
            self.grid.addWidget(self.labelDurataModel2, 10, 0)
            self.grid.addWidget(self.labelSensibilitateInitModel2, 11, 0) 
#            self.grid.addWidget(self.labelSensibilitateFinalaModel2, 15, 0)
            self.grid.addWidget(self.labelTreapta3, 12, 0)
#            self.grid.addWidget(self.labelTipModel3, 16, 0)
            self.grid.addWidget(self.labelDurataModel3, 13, 0)
            self.grid.addWidget(self.labelSensibilitateInitModel3, 14, 0) 
#            self.grid.addWidget(self.labelSensibilitateFinalaModel3, 20, 0)
            self.grid.addWidget(self.labelTreapta4, 15, 0)
#            self.grid.addWidget(self.labelTipModel4, 21, 0)
            self.grid.addWidget(self.labelDurataModel4, 16, 0)
            self.grid.addWidget(self.labelSensibilitateInitModel4, 17, 0) 
#            self.grid.addWidget(self.labelSensibilitateFinalaModel4, 25, 0)         


#            self.grid.addWidget(self.model1ComBox, 7, 1)
            self.grid.addWidget(self.durataModel1InputDialog, 7, 1)
            self.grid.addWidget(self.sensibilitInitModel1, 8, 1)
#            self.grid.addWidget(self.sensibilitFinModel1, 10, 1)
#            self.grid.addWidget(self.model2ComBox, 11, 1)
            self.grid.addWidget(self.durataModel2InputDialog, 10, 1)
            self.grid.addWidget(self.sensibilitInitModel2, 11, 1)
#            self.grid.addWidget(self.sensibilitFinModel2, 15, 1)
#            self.grid.addWidget(self.model3ComBox, 16, 1)
            self.grid.addWidget(self.durataModel3InputDialog, 13, 1)
            self.grid.addWidget(self.sensibilitInitModel3, 14, 1)
#            self.grid.addWidget(self.sensibilitFinModel3, 20, 1)
#            self.grid.addWidget(self.model4ComBox, 21, 1)
            self.grid.addWidget(self.durataModel4InputDialog, 16, 1)
            self.grid.addWidget(self.sensibilitInitModel4, 17, 1)
#            self.grid.addWidget(self.sensibilitFinModel4, 25, 1)

            try:
                self.grid.removeWidget(self.labelSensibilitate)
                self.grid.removeWidget(self.sensibilComBox)
                self.labelSensibilitate.setParent(None)
                self.sensibilComBox.setParent(None)
            except:
                pass


        if(int(self.modelComBox.currentIndex()) == 2):

            self.grid.addWidget(self.labelSensibilitate, 5, 0)
            self.grid.addWidget(self.sensibilComBox, 5, 1)
            
            try:
                self.grid.removeWidget(self.labelNrTrepte)
                self.grid.removeWidget(self.nrTrepteComBox)
                self.grid.removeWidget(self.labelTreapta1)
#                self.grid.removeWidget(self.labelTipModel1)
                self.grid.removeWidget(self.labelDurataModel1)
                self.grid.removeWidget(self.labelSensibilitateInitModel1)
#                self.grid.removeWidget(self.labelSensibilitateFinalaModel1)
                self.grid.removeWidget(self.labelTreapta2)
#                self.grid.removeWidget(self.labelTipModel2)
                self.grid.removeWidget(self.labelDurataModel2)
                self.grid.removeWidget(self.labelSensibilitateInitModel2) 
#                self.grid.removeWidget(self.labelSensibilitateFinalaModel2)
                self.grid.removeWidget(self.labelTreapta3)
#                self.grid.removeWidget(self.labelTipModel3)
                self.grid.removeWidget(self.labelDurataModel3)
                self.grid.removeWidget(self.labelSensibilitateInitModel3) 
#                self.grid.removeWidget(self.labelSensibilitateFinalaModel3)
                self.grid.removeWidget(self.labelTreapta4)
#                self.grid.removeWidget(self.labelTipModel4)
                self.grid.removeWidget(self.labelDurataModel4)
                self.grid.removeWidget(self.labelSensibilitateInitModel4) 
#                self.grid.removeWidget(self.labelSensibilitateFinalaModel4) 
#                self.grid.removeWidget(self.model1ComBox)
                self.grid.removeWidget(self.durataModel1InputDialog)
                self.grid.removeWidget(self.sensibilitInitModel1)
#                self.grid.removeWidget(self.sensibilitFinModel1)
#                self.grid.removeWidget(self.model2ComBox)
                self.grid.removeWidget(self.durataModel2InputDialog)
                self.grid.removeWidget(self.sensibilitInitModel2)
#                self.grid.removeWidget(self.sensibilitFinModel2)
#                self.grid.removeWidget(self.model3ComBox)
                self.grid.removeWidget(self.durataModel3InputDialog)
                self.grid.removeWidget(self.sensibilitInitModel3)
#                self.grid.removeWidget(self.sensibilitFinModel3)
#                self.grid.removeWidget(self.model4ComBox)
                self.grid.removeWidget(self.durataModel4InputDialog)
                self.grid.removeWidget(self.sensibilitInitModel4)
#                self.grid.removeWidget(self.sensibilitFinModel4)
            
                self.labelNrTrepte.setParent(None)
                self.nrTrepteComBox.setParent(None)
                self.labelTreapta1.setParent(None)
#                self.labelTipModel1.setParent(None)
                self.labelDurataModel1.setParent(None)
                self.labelSensibilitateInitModel1.setParent(None)
#                self.labelSensibilitateFinalaModel1.setParent(None)
                self.labelTreapta2.setParent(None)
#                self.labelTipModel2.setParent(None)
                self.labelDurataModel2.setParent(None)
                self.labelSensibilitateInitModel2.setParent(None)
#                self.labelSensibilitateFinalaModel2.setParent(None)
                self.labelTreapta3.setParent(None)
#                self.labelTipModel3.setParent(None)
                self.labelDurataModel3.setParent(None)
                self.labelSensibilitateInitModel3.setParent(None)
#                self.labelSensibilitateFinalaModel3.setParent(None)
                self.labelTreapta4.setParent(None)
#                self.labelTipModel4.setParent(None)
                self.labelDurataModel4.setParent(None)
                self.labelSensibilitateInitModel4.setParent(None)
#                self.labelSensibilitateFinalaModel4.setParent(None)
#                self.model1ComBox.setParent(None)
                self.durataModel1InputDialog.setParent(None)
                self.sensibilitInitModel1.setParent(None)
#                self.sensibilitFinModel1.setParent(None)
#                self.model2ComBox.setParent(None)
                self.durataModel2InputDialog.setParent(None)
                self.sensibilitInitModel2.setParent(None)
#                self.sensibilitFinModel2.setParent(None)
#                self.model3ComBox.setParent(None)
                self.durataModel3InputDialog.setParent(None)
                self.sensibilitInitModel3.setParent(None)
#                self.sensibilitFinModel3.setParent(None)
#                self.model4ComBox.setParent(None)
                self.durataModel4InputDialog.setParent(None)
                self.sensibilitInitModel4.setParent(None)
#                self.sensibilitFinModel4.setParent(None)

            except:
                pass

    def startBtnClicked(self):
        
#   Create folder with name for files if not exists
        stri = os.path.join("files", str(self.numeLineEdit.text()))
        if not os.path.exists(stri):
            os.makedirs(stri)
            
#   Create new file for recordings
        timp = strftime("%Y%m%d%H%M%S", gmtime())
        name = "files/"+self.numeLineEdit.text()+"/"+self.numeLineEdit.text()+"_"+ str(timp) +".dat"
        self.file = open(name, "w")

#   Reset elements for this turn
        self.trig = [0]
        self.tura = 0
        self.repetari = self.repetariInputDialog.text()
        self.repLbl.setText(self.repetari)
        self.turaLbl.setText(str(self.tura))
        self.file.write("%s\n" %str(self.repetari))

        if(int(self.modelComBox.currentIndex()) > 1):
            maxim = int(self.sensibilComBox.currentText())
            self.p1.setYRange(0,maxim,padding=0)
            self.file.write("0\n" )
        else:
            if(int(self.nrTrepteComBox.currentIndex()) == 0):
                maxim = int(self.sensibilitInitModel1.text())
                self.file.write("1\n")
                self.file.write("%s %s\n" %(str(self.sensibilitInitModel1.text()) ,str(self.durataModel1InputDialog.text())))
            else:
                if(int(self.nrTrepteComBox.currentIndex()) == 1):
                    maxim = max(int(self.sensibilitInitModel1.text()), int(self.sensibilitInitModel2.text()))
                    self.file.write("2\n" )
                    self.file.write("%s %s\n" %(str(self.sensibilitInitModel1.text()) ,str(self.durataModel1InputDialog.text())))
                    self.file.write("%s %s\n" %(str(self.sensibilitInitModel2.text()) ,str(self.durataModel2InputDialog.text())))

                else:
                    if(int(self.nrTrepteComBox.currentIndex()) == 2):
                        maxim = max(int(self.sensibilitInitModel1.text()), int(self.sensibilitInitModel2.text()), int(self.sensibilitInitModel3.text()))
                        self.file.write("3\n" )
                        self.file.write("%s %s\n" %(str(self.sensibilitInitModel1.text()) ,str(self.durataModel1InputDialog.text())))
                        self.file.write("%s %s\n" %(str(self.sensibilitInitModel2.text()) ,str(self.durataModel2InputDialog.text())))
                        self.file.write("%s %s\n" %(str(self.sensibilitInitModel3.text()) ,str(self.durataModel3InputDialog.text())))
                    else:
                        if(int(self.nrTrepteComBox.currentIndex()) == 3):
                            maxim = max(int(self.sensibilitInitModel1.text()), int(self.sensibilitInitModel2.text()), int(self.sensibilitInitModel3.text()), int(self.sensibilitInitModel4.text()))
                            self.file.write("4\n" )
                            self.file.write("%s %s\n" %(str(self.sensibilitInitModel1.text()) ,str(self.durataModel1InputDialog.text())))
                            self.file.write("%s %s\n" %(str(self.sensibilitInitModel2.text()) ,str(self.durataModel2InputDialog.text())))
                            self.file.write("%s %s\n" %(str(self.sensibilitInitModel3.text()) ,str(self.durataModel3InputDialog.text())))
                            self.file.write("%s %s\n" %(str(self.sensibilitInitModel4.text()) ,str(self.durataModel4InputDialog.text())))
            self.p1.setYRange(0,maxim * 3,padding=0)

#   Find port
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino Micro" in port[1] or "USB" in port[1]:
                self.port = port[0]
                self.ser = serial.Serial(self.port, 9600, timeout=1)

        
        self.timer.start(0)

    def stopBtnClicked(self):
        self.ser.close()
        self.timer.stop()
        self.file.close()

        if(self.internet_on() == True):
            ftp = FTP('ftp.domain.com')
            ftp.login('user@domain.com', 'password')

            for dirname, dirnames, filenames in os.walk('./files'):
            # print path to all subdirectories first.
            #    for subdirname in dirnames:
            #        print(os.path.join(dirname, subdirname))

            # print path to all filenames.
                for filename in filenames:
                    file_path = os.path.join(dirname, filename)
                    print(file_path)
                    file = open(file_path,'rb')   
                    ftp.storbinary('STOR ./' + filename , file)


    def internet_on(self):
        try:
            urllib2.urlopen('http://techdex.ro', timeout=1)
            return True
        except urllib2.URLError as err: 
            return False


    def zerolistmaker(self, n):
        listofzeros = [0] * n
        return listofzeros

    def showdialog(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText('Date incomplete: Introduce-ti numele')
        msg.setWindowTitle('Date incomplete')
        msg.setStandardButtons(QtGui.QMessageBox.Ok)

    def makeModel(self, time, val1, val2 = 0):
        return [val1]*time

    def update(self):
        if(self.repLbl.text() == self.turaLbl.text()):
            return self.stopBtnClicked()
        try:
            var = self.ser.readline()
            var = var.split()
        except:
            pass

        try:
            dat = int(var[self.senzorComBox.currentIndex()])
            self.data.append(dat)
#            varmV = mymap(int(var),0,1023,0,5000)
#            varRes = ((5000-varmV)*10000)/varmV
#            varCond = 1000000/varRes
#            if varCond <=1000:
#                varForce = 101.97*varCond/80 #grams (if you want N erace 101.97)
#            else:
#                varForce = 101.97*(varCond-1000)/30 #grams (if you want N erace 101.97)
        except:
            pass

        if(self.data[-100:] == self.zerolistmaker(100)):
            l = len(self.data)
            if(self.data != self.zerolistmaker(l)):
                self.trig = self.data
                self.tura += 1
                self.turaLbl.setText(str(self.tura))
                for read in self.trig:
                    self.file.write("%s " % str(read))
                self.file.write("\n")
                self.file.flush()
            self.data = [0]
        else:
            self.data = self.data[-9000:]

#   Select model
        if(int(self.modelComBox.currentIndex()) == 1):
            if(int(self.nrTrepteComBox.currentIndex()) == 0):
                timp = int(self.durataModel1InputDialog.text())*100
                presiuneInit = (int(self.sensibilitInitModel1.text()))
                self.model = self.makeModel(timp, presiuneInit)
                self.model[-1] = 0
            else:
                if(int(self.nrTrepteComBox.currentIndex()) == 1):
                    timp = int(self.durataModel1InputDialog.text())*100
                    presiuneInit = (int(self.sensibilitInitModel1.text()))
                    subModel1 = self.makeModel(timp, presiuneInit)

                    timp = int(self.durataModel2InputDialog.text())*100
                    presiuneInit = (int(self.sensibilitInitModel2.text()))
                    subModel2 = self.makeModel(timp, presiuneInit)
                    self.model = subModel1 + subModel2
                    self.model[-1] = 0
                else:
                    if(int(self.nrTrepteComBox.currentIndex()) == 2):
                        timp = int(self.durataModel1InputDialog.text())*100
                        presiuneInit = (int(self.sensibilitInitModel1.text()))
                        subModel1 = self.makeModel(timp, presiuneInit)

                        timp = int(self.durataModel2InputDialog.text())*100
                        presiuneInit = (int(self.sensibilitInitModel2.text()))
                        subModel2 = self.makeModel(timp, presiuneInit)

                        timp = int(self.durataModel3InputDialog.text())*100
                        presiuneInit = (int(self.sensibilitInitModel3.text()))
                        subModel3 = self.makeModel(timp, presiuneInit)
                        self.model = subModel1 + subModel2 + subModel3
                        self.model[-1] = 0
                    else:
                        if(int(self.nrTrepteComBox.currentIndex()) == 3):
                            timp = int(self.durataModel1InputDialog.text())*100
                            presiuneInit = (int(self.sensibilitInitModel1.text()))
                            subModel1 = self.makeModel(timp, presiuneInit)

                            timp = int(self.durataModel2InputDialog.text())*100
                            presiuneInit = (int(self.sensibilitInitModel2.text()))
                            subModel2 = self.makeModel(timp, presiuneInit)

                            timp = int(self.durataModel3InputDialog.text())*100
                            presiuneInit = (int(self.sensibilitInitModel3.text()))
                            subModel3 = self.makeModel(timp, presiuneInit)

                            timp = int(self.durataModel4InputDialog.text())*100
                            presiuneInit = (int(self.sensibilitInitModel4.text()))
                            subModel4 = self.makeModel(timp, presiuneInit)
                            self.model = subModel1 + subModel2 + subModel3 + subModel4
                            self.model[-1] = 0
        else:
            self.model = [0]

        xdata = np.array(self.data, dtype='float64')
        xdata2 = np.array(self.trig, dtype='float64')
        xdata3 = np.array(self.model, dtype='float64')
        self.curve.setData(xdata)
        self.curve2.setData(xdata2)
        self.curve3.setData(xdata3)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = FinCon()
