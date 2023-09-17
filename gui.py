from random import choice
import tkinter as tk
from tkinter import ttk, messagebox, Label, Frame, Menu, Toplevel
import anime_database as my_database
import pymongo
from PIL import Image, ImageTk
import requests
import io
from termcolor import colored

genre_list = ['','Action','Adventure','Avant Garde','Award Winning','Boys Love','Comedy',
				  'Drama','Fantasy','Girls Love','Gourmet','Horror','Mystery','Romance',
				  'Sci-Fi','Slice of Life','Sports','Supernatural','Suspense','Ecchi',
				  'Adult Cast', 'Anthropomorphic','CGDCT','Childcare',
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
		root.geometry('1300x800')
		root.maxsize(1500,900)
		self.root.config(bg="skyblue")
		self.create_widgets()
		self.history_stack_backward = []
		self.history_stack_forward = []
		self.current_anime = None
		self.random_anime = ''


	def create_widgets(self):

		self.left_frame = Frame(self.root, width=200, height=400, bg='grey')
		self.left_frame.grid(row=0, column=0, padx=10, pady=5)

		self.right_frame = Frame(self.root, width=650, height=400,bg='skyblue')
		self.right_frame.grid(row=0, column=1, padx=10, pady=5)

		self.button_frame = Frame(self.root, width=100,height=100,bg='grey')
		self.button_frame.grid(row=1,column=0,padx=10,pady=5)

		genre_score_label = Label(self.left_frame, text = "Select Genre and Score:")
		genre_score_label.grid(row=0,column=0,padx=5,pady=5)

		self.genre_var = tk.StringVar()
		genre_combo = ttk.Combobox(self.left_frame, textvariable=self.genre_var, state='readonly', values=genre_list)
		genre_combo.grid(row=1,column=0,padx=5,pady=5)

		self.score_var = tk.StringVar()
		score_combo = ttk.Combobox(self.left_frame, textvariable=self.score_var, state='readonly', values=['','7','8','9'])
		score_combo.grid(row=2, column=0, padx=5, pady=5)

		self.label = Label(self.right_frame, text='',bg='skyblue')
		self.label.grid(row=0,column=0,padx=5,pady=5)

		self.image_label = Label(self.right_frame,bg='skyblue')
		self.image_label.grid(row=1,column=0,padx=5,pady=5)

		self.label2 = Label(self.left_frame,bg='grey')
		self.label2.grid(row=4,column=0,padx=5,pady=5)

		self.label3 = Label(self.left_frame,bg='grey')
		self.label3.grid(row=5,column=0,padx=5,pady=5)

		self.label4 = Label(self.left_frame,bg='grey')
		self.label4.grid(row=6,column=0,padx=5,pady=5)
	
		random_anime_button = tk.Button(self.left_frame,text='Generate Anime',command=self.anime_choice).grid(row=3,column=0,padx=5,pady=5)
		info_button = tk.Button(self.left_frame,text='?',command=self.tooltip).grid(row=0,column=1,padx=5,pady=5)
		back_button = tk.Button(self.button_frame,text='Back',bg='skyblue',command=self.previous_anime).grid(row=0,column=0,padx=5,pady=5)
		forward_button = tk.Button(self.button_frame,text='Next',bg='skyblue',command=self.next_anime).grid(row=0,column=1,padx=5,pady=5)
		

		menu = Menu(self.root)
		self.root.config(menu=menu)
		filemenu = Menu(menu, tearoff=0)
		menu.add_cascade(label='Settings', menu=filemenu)
		filemenu.add_command(label='Preferences', command=self.preferences_click)


	def anime_choice(self):
		if self.current_anime is not None:
			self.history_stack_backward.append(self.current_anime)
		selected_genre = self.genre_var.get()
		selected_score = self.score_var.get()

		if not selected_genre and not selected_score:
			self.random_anime = my_database.get_random_anime()
		elif selected_genre and selected_score:
			self.random_anime = my_database.get_anime_by_genre_score(selected_genre,selected_score)
		elif selected_genre and not selected_score:
			self.random_anime = my_database.get_anime_by_genre(selected_genre)
		elif not selected_genre and selected_score:
			self.random_anime = my_database.get_anime_by_score(selected_score)

		if self.random_anime is not None:
			self.label.config(text=self.random_anime['title'],bg='white')
			self.label2.config(text=f'Rank: {self.random_anime["rank"]}',bg='white')
			self.label3.config(text=f'Score: {self.random_anime["score"]}',bg='white')
			seperator = "\n"
			result_string = seperator.join(self.random_anime["genres"])
			self.label4.config(text=f'Genres: \n{result_string}',bg='white')

			image_url = self.random_anime['image link']
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
	
			self.current_anime = self.random_anime
		else:
			self.label.config(text='Anime with this Genre and Score does not exist',bg='white')
			self.label2.config(text='',bg='grey')
			self.label3.config(text='',bg='grey')
			self.label4.config(text='',bg='grey')
			if self.image_label:
				self.image_label.config(image='')
			else:
				pass
		
		colored_text = colored('Current Anime','blue',attrs=['bold'])
		print(colored_text)
		print(self.current_anime['title'])

		colored_text = colored('Previous Animes','blue',attrs=['bold'])
		print(colored_text)
		for info in self.history_stack_backward:
			print(info["title"])

		colored_text = colored('Next Animes','blue',attrs=['bold'])
		print(colored_text)
		for info in self.history_stack_forward:
			print(info['title'])

		colored_text = colored('-' * 40,'red',attrs=['bold'])
		print(colored_text)

	def confirm_exit(self):
		result = messagebox.askyesno("Confirmation", "Are you sure you want to exit?")
		if result:
			self.root.destroy()

	def preferences_click(self):
		sub_window = Toplevel(root)
		sub_window.title('Preferences')
		sub_window.geometry('320x240+125+125')

	def previous_anime(self):
		if len(self.history_stack_backward) <= 0 and len(self.history_stack_forward) == 0:
			pass
		elif len(self.history_stack_backward) > 0:
			self.history_stack_forward.append(self.current_anime)
			popped_anime = self.history_stack_backward.pop()
			self.label.config(text=popped_anime["title"])
			self.label2.config(text=f'Rank: {popped_anime["rank"]}')
			self.label3.config(text=f'Score: {popped_anime["score"]}')
			seperator = "\n"
			result_string = seperator.join(popped_anime["genres"])
			self.label4.config(text=f'Genres: \n{result_string}')

			image_url = popped_anime['image link']
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

			self.current_anime = popped_anime

			colored_text = colored('Current Anime','blue',attrs=['bold'])
			print(colored_text)
			print(self.current_anime['title'])

			colored_text = colored('Previous Animes','blue',attrs=['bold'])
			print(colored_text)
			for info in self.history_stack_backward:
				print(info["title"])

			colored_text = colored('Next Animes','blue',attrs=['bold'])
			print(colored_text)
			for info in self.history_stack_forward:
				print(info['title'])

			colored_text = colored('-' * 40,'red',attrs=['bold'])
			print(colored_text)

	def next_anime(self):

		if len(self.history_stack_forward) == 0:
			pass
		else:
			self.history_stack_backward.append(self.current_anime)
			popped_anime = self.history_stack_forward.pop()

			self.label.config(text=popped_anime["title"])
			self.label2.config(text=f'Rank: {popped_anime["rank"]}')
			self.label3.config(text=f'Score: {popped_anime["score"]}')
			seperator = "\n"
			result_string = seperator.join(popped_anime["genres"])
			self.label4.config(text=f'Genres: \n{result_string}')

			image_url = popped_anime['image link']
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

			self.current_anime = popped_anime

			colored_text = colored('Current Anime','blue',attrs=['bold'])
			print(colored_text)
			print(self.current_anime['title'])

			colored_text = colored('Previous Animes','blue',attrs=['bold'])
			print(colored_text)
			for info in self.history_stack_backward:
				print(info["title"])
				
			colored_text = colored('Next Animes','blue',attrs=['bold'])
			print(colored_text)
			for info in self.history_stack_forward:
				print(info['title'])

			colored_text = colored('-' * 40,'red',attrs=['bold'])
			print(colored_text)

	def tooltip(self):
		sub_window = Toplevel(root)
		sub_window.title('How To Use')
		sub_window.geometry('1200x750+125+125')
		label5 = Label(sub_window,text='Generating Random Animes\n\n'
									   'Generate Completely Random Anime:\n' 
									   'Leave both genre and score dropdown boxes empty and click generate.\n\n'
									   'Generate Random Anime with a Given Genre:\n'
									   'Leave score box empty and select a desired genre, then click generate.\n\n'
									   'Generate Random Anime with a Given Score:\n'
									   'Leave genre box empty and select a desired score, then click generate.\n\n'
									   'Generate Random Anime with Given Genre and Score:\n'
									   'Select desired genre and score and then click generate.\n\n'
									   'How to Use Back and Next Buttons\n\n'
									   '*Animes will be cleared after every opening of app, so after you close your window,\n' 
									   'previously generated animes will be lost.*\n\n'
									   'Back Button:\n'
									   'Click back button to see previous anime generated\n\n'
									   'Next Button:\n'
									   'Click next button to see animes in front of your previous ones.',font=('Arial',10))
		label5.pack()
		# if not self.label5['text'].strip():
		# 	self.label5.config(text='testing')
		# else:
		# 	self.label5.config(text='')




if __name__ == '__main__':
	root = tk.Tk()
	app = AnimeChooserApp(root)
	root.protocol('WM_DELETE_WINDOW', app.confirm_exit)
	root.mainloop()