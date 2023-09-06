from random import choice
import tkinter as tk
from tkinter import ttk, messagebox, Label
import anime_database as my_database
import pymongo
from PIL import Image, ImageTk
import requests
import io

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['anime_db']
collection = db['animes']

genre_list = ['Action','Adventure','Avant Garde','Award Winning','Boys Love','Comedy',
				  'Drama','Fantasy','Girls Love','Gourmet','Horror','Mystery','Romance',
				  'Sci-Fi','Slice of Life','Sports','Supernatural','Suspense','Ecchi',
				  'Erotica','Hentai','Adult Cast', 'Anthropomorphic','CGDCT','Childcare',
				  'Combat Sports','Crossdressing','Delinquents','Detective','Educational',
				  'Gag Humor','Gore','Harem','High Stakes Game','Historical','Idols (Female)',
				  'Idols (Male)','Isekai','Iyashikei','Love Polygon','Magical Sex Shift',
				  'Mahou Shoujo','Martial Arts','Mecha','Medical','Military','Music','Mythology',
				  'Organized Crime','Otaku Culture','Parody','Performing Arts','Pets',
				  'Psychological','Racing','Reincarnation','Reverse Harem','Romantic Subtext',
				  'Samurai','School','Showbiz','Space','Strategy Game','Super Power','Survival',
				  'Team Sports','Time Travel','Vampire','Video Game','Visual Arts','Workplace']

class AnimeChooserApp:

	def __init__(self, root):
		self.root = root
		self.root.title("Anime Chooser")
		self.create_widgets()


	def create_widgets(self):

		genre_label = ttk.Label(self.root, text = "Select Genre:")
		genre_label.pack()

		self.genre_var = tk.StringVar()
		genre_combo = ttk.Combobox(self.root,textvariable=self.genre_var, state='readonly', values=genre_list)
		genre_combo.pack()

		self.label = Label(root, text='')
		self.label.pack()

		self.image_label = Label(self.root)
		self.image_label.pack()

		random_anime_button = ttk.Button(self.root,text='Generate Anime',command=self.anime_choice)
		random_anime_button.pack()

	def anime_choice(self):
		selected_genre = self.genre_var.get()
		random_anime = my_database.get_anime_by_genre(selected_genre)
		self.label.config(text=random_anime['title'])

		image_url = random_anime['image link']
		response = requests.get(image_url)

		if response.status_code == 200:
			image_data = io.BytesIO(response.content)
			img = Image.open(image_data)
			img = ImageTk.PhotoImage(img)
			self.image_label.config(image=img)
			self.image_label.image = img
		else:
			print(f'Failed to retrieved image from URL: {image_url}')		

	def confirm_exit(self):
		result = messagebox.askyesno("Confirmation", "Are you sure you want to exit?")
		if result:
			self.root.destroy()

if __name__ == '__main__':
	root = tk.Tk()
	app = AnimeChooserApp(root)
	root.protocol('WM_DELETE_WINDOW', app.confirm_exit)
	root.mainloop()