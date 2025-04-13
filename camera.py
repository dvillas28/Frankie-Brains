import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
import os

# TODO
#	- que la camara ocupe lo maximo de la pantalla, manteniendo la proporcion

class Camera():
	def __init__(self) -> None:
		"""
		Definicion de variables globales
		"""
		
		# ventana de tkinter
		self.root = tk.Tk()
		self.root.title("Camara")
		self.fullscreen = True
		self.root.attributes("-fullscreen", True)
		
		self.status_text = tk.StringVar()
		self.status_text.set("Esperando para iniciar busqueda")
		
		self.status_label = tk.Label(self.root, textvariable=self.status_text, font=("Arial", 14))
		self.status_label.pack(pady=20, expand=True)

		# label donde ira a la imagen
		self.video_label = tk.Label(self.root, bg='black')
		self.video_label.pack(expand=True, fill='both') # geometry manager
		
		# busqueda de la camara
		self.cap = None
		self.root.bind("<Key>", self.handle_keypress) # asociar el handler al event loop
		self.root.bind("<Escape>", self.toggle_fullscreen)
		
		self.start_search_for_camera()
	
	def start_search_for_camera(self):
		"""
		Iniciar la busqueda indefinida de una camara
		"""
		
		self.search_for_camera()
	
	def search_for_camera(self):
		"""
		Buscar indefinidamente una camara
		"""
		
		self.status_text.set("Buscando camara...")
		self.root.update()
		
		found_camera = None
		
		for i in range(10):
			test_cap = cv2.VideoCapture(i)
			if test_cap.isOpened():
				ret, _ = test_cap.read()
				test_cap.release()
				if ret:
					found_camera = i
					print("camera found")
					break
					
			else:
				test_cap.release()
			
		if found_camera is not None:
			self.status_text.set(f"Camara encontrada ({i}) Mostrando video")
			self.root.after(1000, lambda: self.status_label.pack_forget())
			
			# abrir la camara
			self.cap = cv2.VideoCapture(found_camera)
			self.show_frame()
			
		else:
			# self.status_text.set("No se encontro camara. Reintentando...")
			self.root.after(2000, self.search_for_camera)
		
	def show_frame(self) -> None:
		
		if self.cap is not None:
			ret, frame = self.cap.read()
			if ret:
				# convertirlo a imagen de PIL
				frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				frame_h, frame_w = frame.shape[:2] # Dimensiones originales
				
				# Dimensionaes actuales del label
				label_w = self.video_label.winfo_width()
				label_h = self.video_label.winfo_height()
				
				if label_w < 2 or label_h < 2:
					self.root.after(10, self.show_frame)
					return
				
				# Calcular la relación de aspecto
				frame_ratio = frame_w / frame_h
				label_ratio = label_w / label_h
				
				# Ajustar sin romper la relacion de aspecto
				if frame_ratio > label_ratio:
					new_width = label_w
					new_height = int(label_w / frame_ratio)
					
				else:
					new_height = label_h
					new_width = int(label_h * frame_ratio)
					
				resized_frame = cv2.resize(frame_rgb, (new_height, new_width), interpolation=cv2.INTER_AREA)
				img = Image.fromarray(resized_frame)
				imgTk = ImageTk.PhotoImage(image=img)
			
				# mostrar la imagen
				self.video_label.imgtk = imgTk
				self.video_label.configure(image=imgTk)
				
			# llamar repetidamente para actualizar
			self.video_label.after(10, self.show_frame)
		
	def take_photo(self):
	
		# leer la foto actual de la camara
		ret, frame = self.cap.read()
		
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
	
	def toggle_fullscreen(self, event=None):
		self.fullscreen = not self.fullscreen
		self.root.attributes("-fullscreen", self.fullscreen)
		if not self.fullscreen:
			self.root.geometry("1280x720")
		else:
			self.root.geometry("") # dejar que se ajuste a fullscreen
	
	def handle_keypress(self, event):
		print(event.char)
	
		if event.char == "p":
			cam.take_photo()
		
		elif event.char == "q":
			cam.quit()
	
	def quit(self) -> None:
		if self.cap:
			self.cap.release()
		cv2.destroyAllWindows()
		self.root.quit()
		print("Exiting...")
	
	def start(self) -> None:
		print("p: take photo")
		print("q: quit camera")
		# iniciar el loop de la app
		self.root.mainloop()
		


cam = Camera()
cam.start()
