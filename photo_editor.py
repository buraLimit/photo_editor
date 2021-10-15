
import tkinter
from tkinter import*
from tkinter import ttk, filedialog

import numpy
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import cv2
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tkinter.Tk()
root.title("PhotoEdit Demo Version")
root.geometry("1400x700")
root.configure(padx=10,pady=10)

img = Image
imgBackup = Image
imgBackupContrast = Image
imgBackupBrightness = Image
leftFrame = Frame(root)
fotoFrame = Frame(root)
imgLabel = Label(fotoFrame)
canvas = FigureCanvasTkAgg()

#funkcija za otvaranje fotografije
def fnOpenPhoto():
    filename = filedialog.askopenfilename(initialdir="/Desktop", title="Select A File", filetype=
    (("jpeg files", "*.jpg"), ("png files", "*.png"),("all files", "*.*")))
    global imgLabel
    global imgBackup
    imgLabel.config(image='')
    global img
    fixed_height = 400
    try:
        img = Image.open(filename)
    except IOError:
        print("Unable to load image ")
        sys.exit(1)
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    img = img.resize((width_size, fixed_height), Image.NEAREST)
    # image.nearest - Pick one nearest pixel from the input image. Ignore all other input pixels.

    varContrast.set(1.0)
    varBrightness.set(1.0)
    lblContrastUpdate.config(text="0")
    lblBrightnessUpdate.config(text="0")

    #pravi rezervnu kopiju fotografije kako bi mogli da iskoristimo opciju UNDO
    imgBackup=img

    photo = ImageTk.PhotoImage(img)
    fnUpdatePhotoLabel(photo)

#funkcija za GRAYSCALE
def fnGrayScale():
    global img
    global imgBackup
    imgBackup = img
    gray = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2GRAY)
    photo =  ImageTk.PhotoImage(Image.fromarray(gray))
    img = ImageTk.getimage(photo)
    fnUpdatePhotoLabel(photo)

#funkcija za zamucenje fotografije
def fnBlur():
    global img
    global imgBackup
    imgBackup=img
    value = int(entryBlur.get())
    gaussImage =  ImageTk.PhotoImage(img.filter( ImageFilter.GaussianBlur(radius=value)))
    img = ImageTk.getimage(gaussImage)

    fnUpdatePhotoLabel(gaussImage)
    entryBlur.delete(0,END)

#funkcija za izostravanje fotografije
def fnSharpen():
    global img
    global imgBackup
    imgBackup = img
    value = int(entrySharpen.get())
    sharpImage = ImageTk.PhotoImage( ImageEnhance.Sharpness(img).enhance(value))
    img = ImageTk.getimage(sharpImage)

    fnUpdatePhotoLabel(sharpImage)
    entrySharpen.delete(0,END)

#funkcija za rotiranje fotografije
def fnRotate():
    global img
    global imgBackup
    imgBackup = img
    img = img.transpose(Image.ROTATE_90)
    photo =  ImageTk.PhotoImage(img)

    fnUpdatePhotoLabel(photo)

#funkcija za podesavanje kontrasta fotografije
def FNscaleContrast(value):
    # global img
    # imgnp = np.array(img)
    # alpha = float(value)  # original contrast
    # beta = 0
    # new_image = cv2.convertScaleAbs(imgnp, alpha=alpha, beta=beta)
    # photo = ImageTk.PhotoImage(Image.fromarray(new_image))
    lblContrastUpdate.config(text=str(round(float(value)-1,2)))
    global img
    global imgBackupContrast

    pojacivac = ImageEnhance.Contrast(img)
    photo = ImageTk.PhotoImage(pojacivac.enhance(float(value)))
    imgBackupContrast = ImageTk.getimage(photo)

    fnUpdatePhotoLabel(photo)

#funkcija za podesavanje osvetljenja fotografije
def FNscaleBrightness(value):
    lblBrightnessUpdate.config(text=str(round(float(value)-1,2)))
    global img
    global imgBackupBrightness

    pojacivac = ImageEnhance.Brightness(img)
    photo =  ImageTk.PhotoImage(pojacivac.enhance(float(value)))
    imgBackupBrightness = ImageTk.getimage(photo)

    fnUpdatePhotoLabel(photo)

#funkcija za filter EBMOSS
def fnEmboss():
    global img
    global imgBackup
    imgBackup = img
    embossSlika =  ImageTk.PhotoImage(img.filter(ImageFilter.EMBOSS))

    fnUpdatePhotoLabel(embossSlika)

#funkcija koja azurira i prikazije histogram prilikom izmena na fotografijama
def azurirajHistogram(photo):
    global canvas
    canvas.get_tk_widget().destroy()

    fig = pyplot.Figure(figsize=(6, 3), dpi=80, frameon=False)
    plot1 = fig.add_subplot(1, 1, 1)
    imgcv = cv2.cvtColor(numpy.array(photo), cv2.COLOR_RGB2BGR)
    plot1.hist([imgcv.ravel()], 256, [0, 256])
    print(numpy.array(photo))
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([imgcv], [i], None, [256], [0, 256])
        plot1.plot(histr, color=col)
        plot1.set_xlim([0, 256])

    canvas = FigureCanvasTkAgg(fig, master=HistogramFrame)
    canvas.draw()
    canvas.get_tk_widget().pack()

#funkcija koja cuva vrednost kontrasta na fotografiji
def saveContrast():
    global imgBackup
    global imgBackupContrast
    global img
    global imgBackupContrast
    global varContrast

    imgBackup = img
    img = imgBackupContrast
    varContrast.set(1.0)
    lblContrastUpdate.config(text="0")

    photo = ImageTk.PhotoImage(img)
    fnUpdatePhotoLabel(photo)

#funkcija koja cuva vrednost osvetljenja na fotorafiji
def saveBrightness():
    global imgBackup
    global imgBackupBrightness
    global img
    global varBrightness

    imgBackup = img
    img = imgBackupBrightness
    photo = ImageTk.PhotoImage(img)
    varBrightness.set(1.0)
    lblBrightnessUpdate.config(text="0")

    fnUpdatePhotoLabel(photo)

#funkcija koja vraca ftogorafiju na poslednju izmenu, odnosno jedan korak unazad
def undo():
    global imgBackup
    global img
    global varBrightness
    global varContrast

    img = imgBackup
    photo = ImageTk.PhotoImage(img)
    varBrightness.set(1.0)
    varContrast.set(1.0)
    lblContrastUpdate.config(text="0")
    lblBrightnessUpdate.config(text="0")

    fnUpdatePhotoLabel(photo)

#cuvanje fotografije
def savePhoto():
    global img
    file = filedialog.asksaveasfile(defaultextension="*.*",filetypes = (("JPG", "*.jpg"), ("PNG","*.png")))

    imgSave = img.convert('RGB')
    imgSave.save(file)

    tkinter.messagebox.showinfo(title=None, message="Photo saved")


#fukcija koja se poziva pri svakoj izmeni fotografije
def fnUpdatePhotoLabel(photo):
    global imgLabel
    imgLabel.config(image='')
    imgLabel.config(image=photo)  # dodati gde se prikazuje
    imgLabel.image = photo
    imgLabel.pack(side=TOP)
    azurirajHistogram(ImageTk.getimage(photo))

#--------------------------------------------GUI------------------------------------------#

leftFrame.pack(side=LEFT)

openSaveFrame = Frame(root)
openSaveFrame.pack(side=TOP)

btnFotografija = Button(openSaveFrame, text ="Choose photo", command = fnOpenPhoto, bg='white', relief=RAISED)
btnFotografija.pack(side=LEFT,padx=5)
btnSavePhoto= Button(openSaveFrame, text ="Save photo", command = savePhoto, bg='white', relief=RAISED)
btnSavePhoto.pack(side=LEFT,padx=5)

fotoFrame.pack(side=LEFT)
fotoFrame.configure(padx=50)

btnUndo = Button(leftFrame, text ="Undo", command = undo, bg='white', relief=RAISED, width=14)
btnUndo.pack(pady=10)

btnRotate = Button(leftFrame, text ="Rotate", command = fnRotate, bg='white', relief=RAISED, width=14)
btnRotate.pack(pady=10)

btnGrayScale = Button(leftFrame, text ="Gray scale", command = fnGrayScale, bg='white', relief=RAISED, width=14)
btnGrayScale.pack(pady=10)

btnEmboss = Button(leftFrame, text ="Emboss", command = fnEmboss, bg='white', relief=RAISED, width=14)
btnEmboss.pack(pady=10)

blurFrame = Frame(leftFrame)
blurFrame.pack(side=TOP)
btnBlur = Button(blurFrame, text ="Blur", command = fnBlur, bg='white', relief=RAISED, width=10)
entryBlur = Entry (blurFrame, width = 3)
btnBlur.pack(side = LEFT,pady=10)
entryBlur.pack(side = LEFT, padx=5, ipady=3)

sharpenFrame = Frame(leftFrame)
sharpenFrame.pack(side=TOP)
btnSharpen = Button(sharpenFrame, text ="Sharpen", command = fnSharpen, bg='white', relief=RAISED, width=10)
entrySharpen = Entry(sharpenFrame,width=3)
btnSharpen.pack(side=LEFT ,pady=10)
entrySharpen.pack(side = LEFT, padx=5, ipady=3)

lblContrast = Label(leftFrame, text ="Contrast", width=10)
lblContrastUpdate = Label(leftFrame,text="0",width=10)
lblContrast.pack(pady=10)
lblContrastUpdate.pack()
varContrast = DoubleVar()
varContrast.set(1.0)
scaleContrast = ttk.Scale(leftFrame, variable = varContrast, orient=HORIZONTAL,from_=0, to=2, command=lambda x : FNscaleContrast(x))
scaleContrast.pack(pady=10)
btnSaveContrast = Button(leftFrame, text ="Save", command = saveContrast, bg='white', relief=RAISED, width=14)
btnSaveContrast.pack(pady=10)


lblBrightness = Label(leftFrame, text ="Brightness", width=10)
lblBrightnessUpdate = Label(leftFrame,text="0",width=10)
lblBrightness.pack(pady=10)
lblBrightnessUpdate.pack()
varBrightness = DoubleVar()
varBrightness.set(1.0)
scaleBrightness = ttk.Scale(leftFrame, variable = varBrightness, orient=HORIZONTAL,from_=0, to=2, command=lambda x : FNscaleBrightness(x))
scaleBrightness.pack(pady=10)
btnSaveBrightness = Button(leftFrame, text ="Save", command = saveBrightness, bg='white', relief=RAISED, width=14)
btnSaveBrightness.pack(pady=10)

HistogramFrame = Frame(root)
HistogramFrame.pack(side=RIGHT)
HistogramFrame.configure(padx=70)

root.mainloop()