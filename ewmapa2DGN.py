import math
from tkinter import filedialog
from tkinter import *

root = Tk()
root.ewmapalink = filedialog.askopenfilename(initialdir = "/",title = "Wybierz txt z Ewmapy")
root.wzorlink = filedialog.askopenfilename(initialdir = "/",title = "Wybierz Wzorzec warstw")
root.wyniklink = filedialog.asksaveasfilename(initialdir = "/",title = "Wybierz plik wynikowy",filetypes = (("DAT Files","*.dat"),("all files","*.*")))
wejsc=open(root.ewmapalink,"r")
wzorwarstw=open(root.wzorlink, "r")
wyjsc=open(root.wyniklink+".dat", "w")

#wejsc=open("C:\\Users\\Dell\\Desktop\\miko\\NACZYSTO\\eksport\\Calosc_EWMAPA", "r")
#wzorwarstw=open("C:\\Users\\Dell\\Desktop\\miko\\NACZYSTO\\eksport\\Warstwy_Wzorzec.txt", "r")
#wyjsc=open("C:\\Users\\Dell\\Desktop\\miko\\NACZYSTO\\eksport\\wyjsc.dat", "w")
pozysklista={}

def StworzBazeWzorcowa():
    for line in wzorwarstw:
        linijki=line[:-1].split()
        pozysklista[linijki[0]]=linijki[1:]

def SprawdzZRD(value):
    if value=="P-":
        zrd=1
    elif value=="A-":
        zrd=4
    else:
        zrd=9
    return zrd


def GetTagGetTag(typTaga,tagtresc,Xpocz,Ypocz,NW,podwarstwa):
    tagD="D,"+Xpocz+","+Ypocz+",0,0.00000000\n"
    if typTaga=="EWautor":
        tagEwautor="C,"+NW.lower()+".ewautor="+tagtresc+"\n"
        return str(tagEwautor+tagD)
    elif typTaga=="rkrg":
        tagKERG="C,"+NW.lower()+".rkrg="+tagtresc+"\n"
        return str(tagKERG+tagD)
    elif typTaga=="zrd":
        tagZRD="C,"+NW.lower()+".zrd="+str(tagtresc)+"\n"
        return str(tagZRD+tagD)
    elif typTaga=="ityp":
        tagItyp="C,"+NW.lower()+".ityp="+str(tagtresc)+"\n"
        return str(tagItyp+tagD)
    elif typTaga=="Uwaga":
        tagUwaga="C,"+NW.lower()+".uwaga="+str(tagtresc)+"_"+str(podwarstwa)+"\n"
        return str(tagUwaga+tagD)


def Wpisliniowy():
    for key, value in pozysklista.items():
        starwarstwa,wzorpodwarstwy=key.split("/")
        if SW==starwarstwa and wzorpodwarstwy==podwarstwa:
            NW=value[1]
            zrd=SprawdzZRD(value[0][:2])
            ityp=value[2]
            Xpocz=format(float(rozbite[2]),".8f")
            Ypocz=format(float(rozbite[3]),".8f")
            Xkonc=format(float(rozbite[4]),".8f")
            Ykonc=format(float(rozbite[5]),".8f")
            KERG=rozbite[8]
            tag="D,"+Xpocz+","+Ypocz+",0,0.00000000\n"
            wyjsc.write("A,L,"+NW+",7,0,0,0\n"+"B,1,"+Xpocz+","+Ypocz+",0.00000000,1\nB,2,"+Xkonc+","+Ykonc+",0.00000000,1\n")
            wyjsc.write(str(GetTagGetTag("rkrg",KERG,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("EWautor",daneaut,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("zrd",zrd,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("ityp",ityp,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("Uwaga",starwarstwa,Xpocz,Ypocz,NW,podwarstwa)))

def WpisLukowy():
    for key, value in pozysklista.items():
        starwarstwa,wzorpodwarstwy=key.split("/")
        if SW==starwarstwa and wzorpodwarstwy==podwarstwa:
            NW=value[1]
            zrd=SprawdzZRD(value[0][:2])
            ityp=value[2]
            Xpocz=format(float(rozbite[2]),".8f")
            Ypocz=format(float(rozbite[3]),".8f")
            Xkonc=format(float(rozbite[4]),".8f")
            Ykonc=format(float(rozbite[5]),".8f")
            Promien=format(float(rozbite[6]),".8f")
            firstXrad=math.sqrt((float(Promien)+float(Xpocz))*(float(Promien)+float(Xkonc)))
            secondXrad=math.sqrt((float(Promien)-float(Xpocz))*(float(Promien)-float(Xkonc)))
            firstYrad=math.sqrt((float(Promien)+float(Ypocz))*(float(Promien)+float(Ykonc)))
            secondYrad=math.sqrt((float(Promien)-float(Ypocz))*(float(Promien)-float(Ykonc)))
            Xcieciw=firstXrad+secondXrad
            Xcieciw/=2
            Ycieciw=firstYrad+secondYrad
            Ycieciw/=2
            cieciwa=(math.sqrt((float(Xkonc)-float(Xpocz))**2+(float(Ykonc)-float(Ypocz))**2))/2
            t=float(Promien)-math.sqrt(float(Promien)**2-cieciwa**2)
            dy=float(Ykonc)-float(Ypocz)
            dx=float(Xkonc)-float(Xpocz)
            azymut=math.degrees(math.atan2(dx,dy))
            if azymut<0:
                azymut+=360
            elif azymut >= 360:
                azymut-=360
            azymutluku=azymut-90
            przyrostX=float((t*math.sin(math.radians(azymutluku))))
            przyrostY=float((t*math.cos(math.radians(azymutluku))))
            Xluku=float(Xcieciw)+przyrostX
            Yluku=float(Ycieciw)+przyrostY
            KERG=rozbite[9]
            wyjsc.write("A,A,"+NW+",7,0,0,0\nB,1,"+Xpocz+","+Ypocz+",0.00000000,0\nB,2,"+str(Xluku)+","+str(Yluku)+",0.00000000,1\n"+"B,3,"+Xkonc+","+Ykonc+",0.00000000,0\n")
            wyjsc.write(str(GetTagGetTag("rkrg",KERG,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("EWautor",daneaut,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("zrd",zrd,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("ityp",ityp,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("Uwaga",starwarstwa,Xpocz,Ypocz,NW,podwarstwa)))

def WpisKolowy():
    for key, value in pozysklista.items():
        starwarstwa,wzorpodwarstwy=key.split("/")
        if SW==starwarstwa and wzorpodwarstwy==podwarstwa:
            NW=value[1]
            zrd=SprawdzZRD(value[0][:2])
            ityp=value[2]
            Xpocz=format(float(rozbite[2]),".8f")
            Ypocz=format(float(rozbite[3]),".8f")
            Promien=format(float(rozbite[4]),".8f")
            KERG=rozbite[7]
            wyjsc.write("A,P,"+NW+",7,0,0,"+str(Promien)+"\nB,1,"+Xpocz+","+Ypocz+",0.00000000,0\n")
            wyjsc.write(str(GetTagGetTag("rkrg",KERG,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("EWautor",daneaut,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("zrd",zrd,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("ityp",ityp,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("Uwaga",starwarstwa,Xpocz,Ypocz,NW,podwarstwa)))

def WpisPunktowy(line): 
    ind=7
    for key,value in pozysklista.items():
        starwarstwa,wzorpodwarstwy=key.split("/")
        if SW==starwarstwa and wzorpodwarstwy==podwarstwa:
            NW=value[1]
            zrd=SprawdzZRD(value[0][:2])
            Xpocz=format(float(rozbite[1]),".8f")
            Ypocz=format(float(rozbite[2]),".8f")
            Skala=format(float(rozbite[3]),".8f")
            Obrot=format(float(rozbite[4]),".8f")
            for text in rozbite:
                if "#" in text:
                    ind=rozbite.index(text)
            KERG=rozbite[ind]
            tekstCelki=line.split('"')
            Celka=tekstCelki[1]
            if "ţ" in Celka:
                Celka=Celka.replace("ţ","")
                Celka=Celka.replace('"','')
                TrescTekstu=Celka
            else:
                TrescTekstu=Celka
                Celka='PKO'
            wyjsc.write("A,S,"+NW+",0,0,0,0,"+str(Celka)+","+str(Skala)+","+Obrot+"\nB,1,"+Xpocz+","+Ypocz+",0.00000000,0\n")
            wyjsc.write(str(GetTagGetTag("rkrg",KERG,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("EWautor",daneaut,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("zrd",zrd,Xpocz,Ypocz,NW,podwarstwa))+str(GetTagGetTag("Uwaga",starwarstwa,Xpocz,Ypocz,NW,podwarstwa)))
            wyjsc.write("C,"+NW.lower()+".opis="+str(TrescTekstu)+"\n"+"D,"+Xpocz+","+Ypocz+",0,0.00000000\n")
try:
    StworzBazeWzorcowa()

    for line in wejsc:
        if  line.endswith(" 23\n"):
            SW=line.split()
            SW=SW[0]+"_L"
        elif line.endswith(" 121\n"):
            SW=line.split()
            SW=SW[0]+"_T"
        elif "*" not in line:
            rozbite=line.split()
            daneaut=line.split("'")
            daneaut=daneaut[1]
            typ=rozbite[1]
            podwarstwa=rozbite[0]
            if typ=="20":
                Wpisliniowy()
            elif typ=="21":
                WpisLukowy()
            elif typ=="22":
                WpisKolowy()
            elif float(typ)>100:
                WpisPunktowy(line)
            else:
                Wpisliniowy()
                print("wykryto nieprawidzłową linie:",line)
except Exception as e:
    print("Blad:"+str(e))