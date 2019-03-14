import random
from multiprocessing import Process
from socket import *
from tkinter import *
from tkinter import ttk

print(sys.version)


class SenderConnection:
    def __init__(self):
        self.host = None
        self.port = None
        self.addr = (self.host, self.port)
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def send_data(self, data):
        self.sock.sendto(data, self.addr)

    def close(self):
        self.close()

    def set_host(self, host):
        print(f'Host set to : {host}')
        if host:
            self.host = host

    def set_port(self, port):
        print(f'Port set to : {port}')
        if port:
            self.port = port


class ReceiverConnection:
    def __init__(self):
        self.host = gethostbyname(gethostname())
        self.port = random.randint(5000, 25000)
        self.addr = (self.host, self.port)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(self.addr)
        self.buffer = 8 * 1024

        self.results = None

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.current_page = None
        self.title('File Transfer')
        self.size = (350, 550)
        self.switch_to_page(FirstPage)
        self.geometry('350x550')
        self.resizable(0, 0)

    def switch_to_page(self, page):
        new_page = page(self)
        if self.current_page:
            self.current_page.destroy()

        self.current_page = new_page
        self.current_page.pack(side=TOP, fill=X, expand=True)


class FirstPage(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        ttk.Label(self, text='First Page', font='"Product Sans" 56 bold').pack(side=TOP)

        self.choice = StringVar()
        # input('Pause..')
        ttk.Radiobutton(self, text='Sender', variable=self.choice, value='sender').pack()
        ttk.Radiobutton(self, text='Receiver', variable=self.choice, value='receiver').pack()

        ttk.Button(self, text='Quit', command=self.master.quit).pack(side=BOTTOM)
        ttk.Button(self, text='Submit', command=self.submit).pack()

    def submit(self):
        print(self.choice.get())
        if self.choice.get() == 'sender':
            self.master.switch_to_page(SenderPage)
        elif self.choice.get() == 'receiver':
            self.master.switch_to_page(ReceiverPage)


class SenderPage(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.Sender = SenderConnection()

        # Add widgets
        ttk.Label(self, text='SenderPage', font='"Product Sans" 40 bold').pack(side=TOP)

        Label(self, text="Enter IP address in the box below: ").pack()
        self.host_entry = ttk.Entry(self, font='"Fira Code" 14', cursor='ibeam')
        self.host_entry.bind("<Return>", self.set_host)
        self.host_entry.pack()

        ttk.Separator(self).pack(fill=X)

        Label(self, text="Enter port address in the box below: ").pack()
        self.port_entry = ttk.Entry(self, font='"Fira Code" 14', cursor='ibeam')
        self.port_entry.bind("<Return>", self.set_port)
        self.port_entry.pack()

        ttk.Button(self, text='Quit', command=self.master.quit).pack(side=BOTTOM)

    def set_host(self, temp):
        host = self.host_entry.get()
        self.Sender.set_host(host)
        self.host_entry.delete(0, END)

    def set_port(self, temp):
        port = self.port_entry.get()
        self.Sender.set_port(port)
        self.port_entry.delete(0, END)


class ReceiverPage(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.Receiver = ReceiverConnection()
        self.thread_run = True  # If set false, all running threads will close

        # Add widgets
        ttk.Label(self, text='ReceiverPage', font='"Product Sans" 40 bold').pack(side=TOP)

        ttk.Label(self, text=f'Your IP address is: {self.Receiver.get_host()}',
                  font='"Product Sans" 22').pack()
        ttk.Label(self, text=f'Your port number is: {self.Receiver.get_port()}',
                  font='"Product Sans" 22').pack()

        self.data_label = Label(self, text='', font='"Product Sans" 12 underline')

        ttk.Button(self, text='Quit', command=self.close).pack(side=BOTTOM)
        self.check_new_messages()  # A function that checks for new messages in a thread
        # t = Thread(target=self.Receiver.sock.recvfrom, args=(self.Receiver.buffer,))
        # t.start()

    def check_new_messages(self):
        task = Process(target=self.check_messages_helper())
        task.start()

    def check_messages_helper(self):
        while True:
            if self.thread_run:
                break
            data, addr = self.Receiver.sock.recvfrom(self.Receiver.buffer)
            other = gethostbyname(addr)
            data = data.decode()
            self.data_label['text'] = f'{other}: {data}'

    def close(self):
        self.thread_run = False
        sys.exit()


m = MainWindow()
m.mainloop()
