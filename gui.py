import random
from multiprocessing import Process
from threading import Thread
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
            self.addr = (self.host, self.port)

    def set_port(self, port):
        print(f'Port set to : {port}')
        if port:
            self.port = port
            self.addr = (self.host, self.port)
 
    @staticmethod
    def validate_host(host):
        L=host.split('.')
        if len(L)!=4:
            return None
        for i in L:
            if not i.isdigit():return None
            
            if not 0<=int(i)<=225:return None
        
        return host

    @staticmethod
    def validate_port(port):
        if port.isdigit:
            port=int(port)
            if 5000<=port<=25000:
                return port 
        else:return None


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
        self.geometry('450x650')
        self.resizable(0, 0)
        self.transfer_object=None # This is the object that is
                                  # going to be transferred to the next frame
                                  # This object can be Sender/ ReceiverConnection object

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

        ttk.Label(self, text='First Page', font='"Product Sans" 28 bold').pack(side=TOP)

        self.choice = StringVar()
        # input('Pause..')
        ttk.Radiobutton(self, text='Sender', variable=self.choice, value='sender').pack()
        ttk.Radiobutton(self, text='Receiver', variable=self.choice, value='receiver').pack()

        ttk.Button(self, text='Quit', command=self.master.quit).pack(side=BOTTOM)
        ttk.Button(self, text='Submit', command=self.submit).pack()

    def submit(self):
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
        ttk.Label(self, text='SenderPage', font='"Product Sans" 22 bold').pack(side=TOP)

        self.host_label=Label(self, text="Enter IP address in the box below: ")
        self.host_label.pack()
        self.host_entry = ttk.Entry(self, font='"Fira Code" 14', cursor='ibeam')
        self.host_entry.bind("<Return>", self.set_host)
        self.host_entry.pack()

        ttk.Separator(self).pack(fill=X)

        self.port_label=Label(self, text="Enter port address in the box below: ")
        self.port_label.pack()
        self.port_entry = ttk.Entry(self, font='"Fira Code" 14', cursor='ibeam')
        self.port_entry.bind("<Return>", self.set_port)
        self.port_entry.pack()

        self.show_host=Label(self, text="")
        self.show_port=Label(self, text="")
        self.show_host.pack()
        self.show_port.pack()

        self.next_page=ttk.Button(self, text='Next', state='disable' ,command=self.next)
        self.next_page.pack(side=BOTTOM)
        ttk.Button(self, text='Quit', command=self.master.quit).pack(side=BOTTOM)

    def set_host(self, temp):
        temp = self.host_entry.get()
        host=self.Sender.validate_host(temp)

        if host:
            self.Sender.set_host(host)
            self.host_entry.delete(0, END)
            self.host_label['fg']='black'
            self.host_label['text']=f'Target IP address is set to: {host}'
        else:
            self.host_label['fg']='red'
            if self.Sender.host:
                msg=f'IP address INVALID, still set to {self.Sender.host}'
            else:
                msg='IP address INVALID, enter again!'
            
            self.host_label['text']=msg
        self.enable_next()


    def set_port(self, temp):
        temp = self.port_entry.get()
        port= self.Sender.validate_port(temp)

        if port:
            self.Sender.set_port(port)
            self.port_entry.delete(0, END)
            self.port_label['fg']='black'
            self.port_label['text']=f'Port address set to: {port}'
        
        else:
            self.port_label['fg']='red'
            if self.Sender.port:
                msg=f'Port number INVALID, port is still set to {self.Sender.port}!'
            else:
                msg='Port number INVALID, enter again!'

            self.port_label['text']=msg
        self.enable_next()
        
    
    def enable_next(self):
        if self.Sender.host and self.Sender.port:
            self.next_page['state']='enable'
        
    def next(self):
        self.master.transfer_object=self.Sender # Transfer the object to the next frame
        print('Going to the next page')
        self.master.switch_to_page(SenderPage2)


class SenderPage2(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.Sender = self.master.transfer_object # Sender is now with this Frame

        # Add Widgets
        ttk.Label(self, text='Message Sender Page', font='"Product Sans" 20 bold').pack(side=TOP)
        ttk.Label(self, text=self.Sender.port, font='"Product Sans" 12 bold').pack(side=TOP)
        ttk.Label(self, text=self.Sender.host, font='"Product Sans" 12 bold').pack(side=TOP)



class ReceiverPage(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.Receiver = ReceiverConnection()
        self.thread_run = True  # If set false, all running threads will close

        # Add widgets
        ttk.Label(self, text='Receiver Page', font='"Product Sans" 22 underline').pack(side=TOP)

        ttk.Label(self, text=f'Your IP address is: {self.Receiver.get_host()}',
                  font='"Fira Code" 9').pack()
        ttk.Label(self, text=f'Your port number is: {self.Receiver.get_port()}',
                  font='"Fira Code" 9').pack()

        self.data_label = Label(self, text='', font='"Product Sans" 8 underline')

        ttk.Button(self, text='Quit', command=self.close).pack(side=BOTTOM)
        self.check_new_messages()  # A function that checks for new messages in a thread
        # t = Thread(target=self.Receiver.sock.recvfrom, args=(self.Receiver.buffer,))
        # t.start()

    def check_new_messages(self):
        task = Thread(target=self.check_messages_helper())
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
