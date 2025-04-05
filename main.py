import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
import os


# TODO:
#   tamaño de la ventana mas grande    

# ventana de tkinter
root = tk.Tk()
root.title("Camara")

# variables globales
cap = cv2.VideoCapture(0) # camara, 0 es la por defecto
lmain = None # ?

def show_frame() -> None:
	
	ret, frame = cap.read()
	if ret:
		
		# convertirlo a imagen de PIL
		cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img = Image.fromarray(cv2image)
		imgTk = ImageTk.PhotoImage(image=img)
		
		# mostrar la imagen
		lmain.imgtk = imgTk
		lmain.configure(image=imgTk)
		
		
	# llamar repetidamente para actualizar
	lmain.after(10, show_frame)
		
	
def take_photo():
	
	# leer la foto actual de la camara
	ret, frame = cap.read()
	
	if ret:
		#filepath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png")])
		
		abspath = os.path.dirname(os.path.realpath(__file__))
		now = datetime.now()
		dt_string = now.strftime("%Y_%m_%d-%H:%M:%S")
		filepath = os.path.join(abspath, "pics", f"{dt_string}.jpg")
											
		#print(f"filepath: {filepath}")
												
		if filepath:
			cv2.imwrite(filepath, frame)
			print(f"photo saved on {filepath}")
	
	
def handle_keypress(event):
	print(event.char)
	
	if event.char == "p":
		take_photo()
		
root.bind("<Key>", handle_keypress) # asociar el handler al event loop

	
lmain = tk.Label(root)
lmain.pack() # geometry manager

#btn = tk.Button(root, text="snap", command= take_photo)
#btn.pack()		


# iniciar el ciclo de actualizacion de la imagen
show_frame()
	
# iniciar el loop de la aplicacion
root.mainloop()

cap.release()
cv2.destroyAllWindows()
