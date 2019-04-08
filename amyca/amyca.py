import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage

import sys

from user import User
from todo import ToDo
from project import Project


class MainScreen:

	def __init__(self):
		"""Initialize GUI main window"""
		self.project = Project('p1')

		self.current_time = 0
		self.nus_orange = '#EF7C00'
		self.nus_blue = '#003D7C'

		self.main_window = Tk()
		self.main_window.geometry('1600x700')  # set window size
		#self.window.attributes('-fullscreen', True) # create full screen
		self.main_window.title('AMYCA - Project Management Assistance')  # set window title
		#self.window.configure(background=self.nus_blue)
		self.main_window.iconphoto(self.main_window, PhotoImage(file='title_image.png'))

		# Create Frame
		self.header = Frame(self.main_window, height=40)
		self.content= Frame(self.main_window)
		self.footer = Frame(self.main_window, height=20)

		self.header.pack(fill='both')
		self.content.pack(fill='both', expand=True)
		self.footer.pack(fill='both')


		# create menu
		self.menu_bar = Menu(self.main_window)
		self.file_menu = Menu(self.menu_bar, tearoff=0) # add file menu
		self.file_menu.add_command(label='Logout', command=self.logout)
		self.file_menu.add_command(label='Exit', command=self.main_window.destroy)
		self.help_menu = Menu(self.menu_bar, tearoff=0)
		self.help_menu.add_command(label='Help', command=self.help)

		self.menu_bar.add_cascade(label='File', menu=self.file_menu)
		self.menu_bar.add_cascade(label='Help', menu=self.help_menu)
		self.main_window.config(menu=self.menu_bar)

		# create default font
		self.output_font = ('Courier New', 12)
		self.header_font = ('Courier New', 30)
		self.footer_font = ('Courier New', 10)

		# add Label as header box
		self.header_box = Label(self.header, text='AMYCA - Project Management Assistance',
		                        font=self.header_font) # ('Helvetica', 30)
		self.header_box.pack()

		# add Label as footer box
		self.footer_box = Label(self.footer, text='Copyright © 2019 Amyca | Develop By: Md Kamruzzaman (A0107851),'
		 + ' Abdullah-al-mamun Khan (A0147365Y) and Chia Xiao Hui (A0147375X) | Project: TE3201-Software Engineering | NUS', font=self.footer_font)
		self.footer_box.pack()

		# add a Entry as input_box to enter command
		self.input_box = Entry(self.content)  # create input box
		self.input_box.pack(padx=5, pady=5, fill='x')
		self.input_box.bind('<Return>', self.command_entered)  # bind the command_entered function to the Enter key
		self.input_box.focus()

		# add a Text area to show chat history
		self.history_area = Text(self.content, width='50')
		self.history_area.pack(padx=5, pady=5, side=LEFT, fill='y')
		self.history_area.tag_configure('normal_format', font=self.output_font)
		self.history_area.tag_configure('success_format', foreground='green', font=self.output_font)
		self.history_area.tag_configure('error_format', foreground='red', font=self.output_font)

		# add a Text area to show list of tasks
		self.list_area = Text(self.content, width='50')
		self.list_area.pack(padx=5, pady=5, side=LEFT, fill='y')
		self.list_area.tag_configure('normal_format', font=self.output_font)
		self.list_area.tag_configure('pending_format', foreground='red', font=self.output_font)
		self.list_area.tag_configure('done_format', foreground='green', font=self.output_font)

		# add a Text area to show all resources
		self.resource_area = Text(self.content, width='50')
		self.resource_area.pack(padx=5, pady=5, side=LEFT, fill='y')
		self.resource_area.tag_configure('normal_format', font=self.output_font)

		# add a Text area to show all cost
		self.cost_area = Text(self.content, width='50')
		self.cost_area.pack(padx=5, pady=5, side=LEFT, fill='both')
		self.cost_area.tag_configure('normal_format', font=self.output_font)
		self.cost_area.tag_configure('total_cost_format', foreground='red', font=self.output_font)

		# show the welcome message and the list of tasks
		self.update_chat_history('start', 'Welcome to AMYCA ! Your project management assistance.', 'success_format')

		self.update_task_list(self.project.tasks)
		self.update_resource_list(self.project.resources)
		self.update_cost_list(self.project.cost)

	def start(self):
		"""This function is for call main loop for starting GUI"""
		self.main_window.mainloop()

	def clear_input_box(self):
		"""This function is for clear input box"""
		self.input_box.delete(0, END)

	def get_current_time(self):
		self.current_time = datetime.datetime.now().strftime('%H:%M:%S')
		return self.current_time

	def update_chat_history(self, command, response, status_format):
		"""

		:param command:
		:param response:
		:param status_format: indicates which color to use for the status message. eg 'normal_format', 'error_format' or 'success_format'
		:return:
		"""
		current_time = datetime.datetime.now().strftime('%H:%M:%S')
		self.history_area.insert(1.0, '-'*40 + '\n', 'normal_format')
		self.history_area.insert(1.0, '>>> ' + response + '\n', status_format)
		self.history_area.insert(1.0, 'You said: ' + command + '\n', 'normal_format')
		self.history_area.insert(1.0, current_time + '\n', 'normal_format')

	def update_task_list(self, tasks):
		self.list_area.delete('1.0', END)  # Clear the list area

		for i, task in enumerate(tasks):
			if task.get_status():
				output_format = 'done_format'
			else:
				output_format = 'pending_format'
			self.list_area.insert(END, task.get_status_as_icon() + ' ' + str(i+1) + '. ' + task.get_as_string() + '\n', output_format)

	def update_resource_list(self, resources):
		self.resource_area.delete('1.0', END)
		for i, resource in enumerate(resources):
			self.resource_area.insert(END, str(i+1) + '. ' + resource[0] + ' = ' + str(resource[1]) + ' pcs' + '\n', 'normal_format')
			# Todo: Need to update as per project resource

	def update_cost_list(self, cost_list):
		self.cost_area.delete('1.0', END) # Todo: Need to ask prof what is mean by '1.0' and END
		total_cost = 0
		for i, cost in enumerate(cost_list):
			total_cost = total_cost + cost[1]
			self.cost_area.insert(END, str(i+1) + '. ' + cost[0] + ' = $' + str(cost[1]) + '\n', 'normal_format')
		self.cost_area.insert(END, '-'*25 + '\n', 'normal_format')
		self.cost_area.insert(END, 'Total cost = $' + str(total_cost) + '\n', 'total_cost_format')

	def command_entered(self, event):
		command = None

		try:
			command = self.input_box.get()
			command.strip().lower()

			output = self.execute_command(command)
			print(output)
			self.update_chat_history(command, output, 'success_format')
			self.update_task_list(self.project.tasks)
			self.update_resource_list(self.project.resources)
			self.update_cost_list(self.project.cost)
			self.clear_input_box()

		except Exception as e:
			self.update_chat_history(command, str(e) + '\n', 'error_format')
			messagebox.showerror('Error...!!!', str(e))

	def execute_command(self, command):
		if command == 'exit':
			sys.exit()
		elif command.startswith('todo '):
			description = command.split(' ', 1)[1]
			return self.project.add_task(ToDo(description, False))
		elif command.startswith('done '):
			user_index = command.split(' ', 1)[1]
			index = int(user_index) - 1
			if index < 0:
				raise Exception('Index must be grater then 0')
			else:
				try:
					self.project.tasks[index].mark_as_done()
					return 'Congrats on completing a task ! :-)'
				except:
					raise Exception('No item at index ' + str(index + 1))
		else:
			raise Exception('Command not recognized')


	def help(self):
		messagebox.showinfo('Help', 'I am amyca to help you')  # Todo: Need to impliment help function

	def logout(self):
		self.main_window.destroy()
		LoginScreen(User).start()


class LoginScreen:
	def __init__(self, user):
		self.user = user
		self.login = False

		self.login_window = Tk()
		self.login_window.geometry('300x250')
		self.login_window.title('Login to Amyca')
		self.login_window.iconphoto(self.login_window, PhotoImage(file='title_image.png'))

		# Create a Form label
		self.label = Label(text='Please enter details below to login')
		self.label.pack(padx=10, pady=10)

		self.label_user_name = Label(self.login_window, text='Username *')
		self.label_user_name.pack(padx=5, pady=5)

		self.username_login_entry = Entry(self.login_window)
		self.username_login_entry.pack(padx=5, pady=5)

		self.label_password = Label(self.login_window, text='Password *')
		self.label_password.pack(padx=5, pady=5)

		self.password_login_entry = Entry(self.login_window, show='*')
		self.password_login_entry.pack(padx=5, pady=5)

		self.login_button = Button(self.login_window, text='Login', command=self.verify_user_login)
		self.login_button.pack(padx=5, pady=5)

	def start(self):
		return self.login_window.mainloop()

	def verify_user_login(self):
		user_name = self.username_login_entry.get()
		user_password = self.password_login_entry.get()
		access_login = self.user.verify(user_name, user_password)
		if access_login:
			self.login_success()
		else:
			messagebox.showerror('Login', 'Login not successful')

	def login_success(self):
		self.login_window.destroy()
		MainScreen().start()


if __name__ == '__main__':
	try:
		#User('admin', 'admin123', 4)
		#LoginScreen(User).start()
		MainScreen().start()
	except Exception as e:
		print('Problem: ', e)
		messagebox.showerror('Error...!!!', str(e))


