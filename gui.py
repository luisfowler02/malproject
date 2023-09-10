from random import choice
import tkinter as tk
from tkinter import ttk, messagebox, Label, Frame
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
		root.title("Anime Chooser")
		root.maxsize(900,600)
		self.root.config(bg="skyblue")
		self.create_widgets()

	def create_widgets(self):

		self.left_frame = Frame(self.root, width=200, height=400, bg='grey')
		self.left_frame.grid(row=0, column=0, padx=10, pady=5)

		self.right_frame = Frame(self.root, width=650, height=400,bg='skyblue')
		self.right_frame.grid(row=0, column=1, padx=10, pady=5)

		genre_label = Label(self.left_frame, text = "Select Genre:")
		genre_label.grid(row=0,column=0,padx=5,pady=5)

		self.genre_var = tk.StringVar()
		genre_combo = ttk.Combobox(self.left_frame, textvariable=self.genre_var, state='readonly', values=genre_list)
		genre_combo.grid(row=1,column=0,padx=5,pady=5)

		self.label = Label(self.right_frame, text='',bg='skyblue')
		self.label.grid(row=0,column=0,padx=5,pady=5)

		self.image_label = Label(self.right_frame,bg='skyblue')
		self.image_label.grid(row=1,column=0,padx=5,pady=5)

		self.label2 = Label(self.left_frame,bg='grey')
		self.label2.grid(row=3,column=0,padx=5,pady=5)

		self.label3 = Label(self.left_frame,bg='grey')
		self.label3.grid(row=4,column=0,padx=5,pady=5)

		self.label4 = Label(self.left_frame,bg='grey')
		self.label4.grid(row=5,column=0,padx=5,pady=5)

		random_anime_button = ttk.Button(self.left_frame,text='Generate Anime',command=self.anime_choice).grid(row=2,column=0,padx=5,pady=5)

	def anime_choice(self):
		selected_genre = self.genre_var.get()
		random_anime = my_database.get_anime_by_genre(selected_genre)

		self.label.config(text=random_anime['title'],bg='white')
		self.label2.config(text=f'Rank: {random_anime["rank"]}',bg='white')
		self.label3.config(text=f'Score: {random_anime["score"]}',bg='white')
		seperator = "\n"
		result_string = seperator.join(random_anime["genres"])
		self.label4.config(text=f'Genres: \n{result_string}',bg='white')

		image_url = random_anime['image link']
		response = requests.get(image_url)

		if response.status_code == 200:
			image_data = io.BytesIO(response.content)
			img = Image.open(image_data)
			img = img.resize((400,500))
			img = ImageTk.PhotoImage(img)
			
			if self.image_label:
				self.image_label.config(image=img)
				self.image_label.image = img
			else:
				self.image_label = Label(self.right_frame, image=img)
				self.image_label.grid(row=1,column=0,padx=5,pady=5)
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