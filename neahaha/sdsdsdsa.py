from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QTimer
from PyQt5.QtGui import *
import sys
import time
import math
import random

lastcard = ["diamond","jack"]


pile = []
player_hand = []
ai_hand = []
suits = ['heart', 'club', 'diamond', 'spade']
cardsa = [1,2,3,4,5,6,7,8,9,10,'jack', 'queen', 'king']

    
class Card:
    def __init__(self,value,suit,face):
        self.value = value
        self.suit = suit
        self.face = face
        




        


def newcards():
    for suit in suits:
        for cards in cardsa:
            if isinstance(cards, str):
                tempcard = Card(cards,suit,True)
            else:
                tempcard = Card(cards,suit,False)
            pile.append(tempcard)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        self.over = False
        self.ptotal = 0
        self.atotal = 0
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Blackjack NEA")
        self.setStyleSheet("QMainWindow {background-color: darkgreen; border: 3px solid black};")
        self.setFixedHeight(540)
        self.setFixedWidth(960)
        central = QWidget()
        self.setCentralWidget(central)
        self.a = QLabel(self)
        self.b = QPushButton(self)
        self.a.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("Blackjack.png")
        pixmap2 = pixmap.scaled(256,128,Qt.KeepAspectRatio)
        pixmap3 = QPixmap("coolbutton.png")
        pixmap4 = pixmap3.scaled(100,100,Qt.KeepAspectRatio)
        pixmap7 = QPixmap("coolbutton2.png")
        pixmap8 = pixmap7.scaled(100,100,Qt.KeepAspectRatio)
        pixmap9 = QPixmap("dealbutton.png")
        pixmap10 = pixmap9.scaled(100,100,Qt.KeepAspectRatio)
        pixmap11 = QPixmap("dealbutton2.png")
        pixmap12 = pixmap11.scaled(100,100,Qt.KeepAspectRatio)
        self.a.setPixmap(pixmap2)
        self.a.adjustSize()
        self.buttonicon1 = QIcon()
        self.buttonicon1.addPixmap(pixmap4, QIcon.Normal, QIcon.Off)
        self.buttonicon1.addPixmap(pixmap8, QIcon.Normal, QIcon.On)
        self.buttonicon1.addPixmap(pixmap8, QIcon.Disabled)
        self.buttonicon2 = QIcon()
        self.buttonicon2.addPixmap(pixmap10, QIcon.Normal, QIcon.Off)
        self.buttonicon2.addPixmap(pixmap12, QIcon.Normal, QIcon.On)
        self.buttonicon2.addPixmap(pixmap12, QIcon.Disabled)
        self.b.setIcon(self.buttonicon1)
        self.b.setIconSize(QSize(100,100))
        self.b.setFixedSize(100,100)
        self.b.move(10,430)
        self.b.setDefault(True)
        self.b.setStyleSheet("QPushButton {background-color: rgba(255, 255, 255, 0)};")
        self.e = QLabel(self)
        pixmapa = QPixmap("standtext.png").scaled(160,160,Qt.KeepAspectRatio)
        self.e.setPixmap(pixmapa)
        self.e.adjustSize()
        self.e.move(680,455)
        self.c = QLabel(self)
        pixmap5 = QPixmap("HITtext.png")
        pixmap6 = pixmap5.scaled(100,100,Qt.KeepAspectRatio)
        self.c.setPixmap(pixmap6)
        self.c.adjustSize()
        self.c.move(120,455)
        self.d = QPushButton(self)
        self.d.setIcon(self.buttonicon2)
        self.d.setIconSize(QSize(100,100))
        self.d.setFixedSize(100,100)
        self.d.move(850,430)
        self.d.setStyleSheet("QPushButton {background-color: rgba(255, 255, 255, 0)};")
        self.d.setCheckable(True)
        self.b.setCheckable(True)
        self.b.clicked.connect(self.this)
        self.d.clicked.connect(self.that)
        ############################################ player hand line
        self.playerframe = QFrame(self)
        self.playerframe.setLineWidth(2)
        self.playerframe.move(35,120)
        self.playerframe.resize(400,300)
        self.uberlayout = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.uberlayout.addLayout(self.layout)
        self.playerframe.setLayout(self.uberlayout)
        self.layout.setSpacing(0)
        self.yourhand = QLabel(self)
        self.yourhand.setPixmap(QPixmap("yourhand.png").scaled(150,150,Qt.KeepAspectRatio))
        self.yourhand.adjustSize()
        self.yourhand.move(130,70)
        self.aihand = QLabel(self)
        self.aihand.setPixmap(QPixmap("dealerhand.png").scaled(150,150,Qt.KeepAspectRatio))
        self.aihand.adjustSize()
        self.aihand.move(670,70)

        ################################################### ai hand line
        self.aiframe = QFrame(self)
        self.aiframe.setLineWidth(2)
        self.aiframe.move(575,120)
        self.aiframe.resize(400,300)
        self.uberlayout1 = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.uberlayout1.addLayout(self.layout1)
        self.aiframe.setLayout(self.uberlayout1)
        self.layout1.setSpacing(0)
        ################################################# value counters
        self.playercounter = QLabel(self)
        self.playercounter.setText("VALUE OF HAND:   ")
        self.playercounter.move(80,350)
        font=QFont("Montserrat",16)
        font2 = font.setBold(True)
        self.playercounter.setFont(font)
        self.playercounter.adjustSize()
        ################################################# ai value counter
        self.playercounter1 = QLabel(self)
        self.playercounter1.setText("VALUE OF HAND:   ")
        self.playercounter1.move(600,350)
        font=QFont("Montserrat",16)
        font2 = font.setBold(True)
        self.playercounter1.setFont(font)
        self.playercounter1.adjustSize()
        ############################################### win counter
        self.wincounter = QLabel(self)
        self.drawpixmap = QPixmap("draw.png").scaled(300,100,Qt.KeepAspectRatio)
        self.playerbustpixmap = QPixmap("playerbust.png").scaled(300,100, Qt.KeepAspectRatio)
        self.dealerbustpixmap = QPixmap("dealerbust.png").scaled(300,100, Qt.KeepAspectRatio)
        self.playerwinpixmap = QPixmap("playerwin.png").scaled(300,100, Qt.KeepAspectRatio)
        self.dealerwinpixmap = QPixmap("dealerwin.png").scaled(300,100, Qt.KeepAspectRatio)
        self.wincounter.move(330,25)
        self.wincounter.setPixmap(self.playerwinpixmap)
        self.wincounter.adjustSize()
        self.wincounter.setVisible(False)
        ################################################# new game button
        self.buttonicon3 = QIcon()
        self.buttonicon3.addPixmap(QPixmap("newgamebutton.png").scaled(200,200,Qt.KeepAspectRatio),QIcon.Normal, QIcon.Off)
        self.buttonicon3.addPixmap(QPixmap("newgamebutton2.png").scaled(200,200,Qt.KeepAspectRatio),QIcon.Normal, QIcon.On)
        self.newgamebutton = QPushButton(self)
        self.newgamebutton.setIcon(self.buttonicon3)
        self.newgamebutton.setIconSize(QSize(200,200))
        self.newgamebutton.setFixedSize(200,200)
        self.newgamebutton.move(375,300)
        self.newgamebutton.setStyleSheet("QPushButton {background-color: rgba(255, 255, 255, 0)};")
        self.newgamebutton.setCheckable(True)
        self.newgamebutton.clicked.connect(self.haha)
        
        
        
    def this(self):
        time.sleep(.1)
        self.b.setChecked(False)
        selected = random.choice(pile)
        player_hand.append(selected)
        pile.remove(selected)
        self.templabel = cardLabel()
        self.templabel.makecardimage(selected.suit, selected.value)
        self.layout.addWidget(self.templabel)
        if selected.face == True:
            self.ptotal = self.ptotal + 10
        else:
            self.ptotal = self.ptotal + selected.value
        print(self.ptotal)
        self.playercounter.setText("VALUE OF HAND: "+str(self.ptotal))
        self.playercounter.adjustSize()
        self.checkwin()
        
    def that(self):
        self.d.setChecked(False)
        self.b.setDisabled(True)
        self.d.setDisabled(True)
        if self.over == False:
            print("Hi")
            QTimer.singleShot(1000, self.aidraw)
        self.over = False

    def haha(self):
        self.wincounter.setVisible(False)
        time.sleep(.1)
        self.over = False
        self.newgamebutton.setChecked(False)
        self.atotal = 0
        self.ptotal = 0
        for i in player_hand:
            player_hand.remove(i)
            pile.append(i)

        

        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.layout1.count())): 
            self.layout1.itemAt(i).widget().setParent(None)
            
        self.playercounter1.setText("VALUE OF HAND: "+str(self.atotal))
        self.playercounter1.adjustSize()
        self.playercounter.setText("VALUE OF HAND: "+str(self.ptotal))
        self.playercounter.adjustSize()
        pile.clear()
        ai_hand.clear()
        player_hand.clear()
        newcards()
        self.b.setDisabled(False)
        self.d.setDisabled(False)

    def checkwin(self):
        print("abbbbb")
        if self.ptotal > 21:
            self.b.setDisabled(True)
            self.d.setDisabled(True)
            print("ai win")
            self.wincounter.setPixmap(self.playerbustpixmap)
            self.wincounter.setVisible(True)
        elif self.atotal > 21:
            self.wincounter.setPixmap(self.dealerbustpixmap)
            self.wincounter.setVisible(True)
            print("p win")
        elif self.atotal <=21 and self.atotal > self.ptotal and self.over == True:
            self.wincounter.setPixmap(self.dealerwinpixmap)
            self.wincounter.setVisible(True)
            print("ai win")
        elif self.ptotal <= 21 and self.ptotal > self.atotal and self.over == True:
            self.wincounter.setPixmap(self.playerwinpixmap)
            self.wincounter.setVisible(True)
            print("ai win")
        elif self.ptotal == self.atotal and self.over == True:
            self.wincounter.setPixmap(self.drawpixmap)
            self.wincounter.setVisible(True)
            print("ai win")
        self.wincounter.adjustSize()
        
        
        

    def aidraw(self):
        self.drawn = False
        self.chancetodraw = 1-(0.1**(1-(self.atotal/21)))
        print(self.chancetodraw)
        self.roll = random.randint(0,100)/100
        if self.roll < self.chancetodraw or (self.ptotal <= 21 and self.atotal < self.ptotal):
            self.drawn = True
            selectedcard = random.choice(pile)
            ai_hand.append(selectedcard)
            pile.remove(selectedcard)
            self.templabel = cardLabel()
            self.templabel.makecardimage(selectedcard.suit, selectedcard.value)
            self.layout1.addWidget(self.templabel)
            if selectedcard.face == True:
                self.atotal = self.atotal + 10
            else:
                self.atotal = self.atotal + selectedcard.value
            print(self.atotal)
            self.playercounter1.setText("VALUE OF HAND: "+str(self.atotal))
            self.playercounter1.adjustSize()
        if self.drawn == False:
            print("game over")
            self.over = True
            self.checkwin()
        else:
            QTimer.singleShot(500, self.aidraw)


        

        


class cardLabel(QLabel):
    def __init__(self,*args,**kwargs):
        super(cardLabel, self).__init__(*args, **kwargs)

    def makecardimage(self, suit, card):
        self.suit = suit
        self.cardname = card
        self.imagetoget = "cards/{}_{}.png".format(self.cardname,self.suit)
        self.pixmap = QPixmap(self.imagetoget).scaled(100,100,Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)
        self.adjustSize()




app = QApplication(sys.argv)
window = MainWindow()

newcards()

window.show()
app.exec_()

