# This file uses the following encoding: utf-8
# Bouncy! - A multihop ssh client and config generator. Version 1.0.
# (C) 2021. Made by Rey.
# Compile with pyinstaller bouncy.py --onefile

import os, tkinter, sys, subprocess, re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox, Scrollbar
import tkinter.scrolledtext as scrolledtext

global system_font
system_font = "Arial, 10"

global previous_user
global homepath

homepath = os.path.expanduser('~/.ssh/')

class view_edit():
    
    def start(self):
        
        editor_window = Tk()
        
        def exit_editor():
            
            content = editor_box.get(1.0, END)
            flag = int(len(content))
            
            if (flag == 1):
                               
                editor_window.destroy()
                
            else:
                
                editor_window.focus_force()
                
                MsgBox = messagebox.askquestion ('File not Saved','Are you sure you want to exit?', icon = 'warning', parent = editor_window)
                    
                if MsgBox == 'yes':
                        
                    editor_window.destroy()
                        
                else:
                        
                    return
        
        def open_file():
            
            input_file_name = filedialog.askopenfilename(initialdir = homepath, parent = editor_window)
            
            if input_file_name:
                
                file_name = input_file_name
                editor_box.delete(1.0, END)
                
                with open(file_name) as file:
                    content = file.read()
                    content = content.rstrip()
                    editor_box.insert(1.0, content)
                    
            editor_window.title("SSH Configuration Editor - "+input_file_name)
        
        def export():
            
            input_file_name = filedialog.asksaveasfilename(initialdir = homepath, parent = editor_window)
            
            if input_file_name:
 
                file_name = input_file_name
                write_to_file(file_name)
                
            editor_window.title("SSH Configuration Editor - "+input_file_name)
                
            return "break"
        
        def write_to_file(file_name):
            
            try:
                content = editor_box.get(1.0, END)
                content = content.rstrip()
                with open(file_name, 'w') as the_file:
                    the_file.write(str(content))
            except IOError:
                tkinter.messagebox.showwarning("Save", "File could not be saved.")        
        
        editor_window.title("SSH Configuration Editor")
        editor_window.iconbitmap('@bouncy.xbm')
        editor_window.geometry("940x680")
        editor_window.resizable(height = 0, width = 0)
        editor_box = scrolledtext.ScrolledText(editor_window, width = 115, height = 39, undo = True)
        editor_box.grid(row = 0, column = 0, padx = 0, ipadx = 0, sticky = W + E + N + S)
        
        menubar = Menu(editor_window)
        
        #File Menu
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", font = system_font, command = open_file)
        filemenu.add_command(label="Export", font = system_font, command = export)
        filemenu.add_command(label="Exit", font = system_font, command = exit_editor)
        menubar.add_cascade(label="File", menu = filemenu)     
        
        #Help Menu

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", font = system_font, command = bouncy().about)
        menubar.add_cascade(label="Help", menu = help_menu)     
        
        editor_window.config(menu = menubar)
        editor_window.focus_force()
        editor_window.protocol('WM_DELETE_WINDOW', exit_editor)
        bouncy().center(editor_window)
        editor_window.mainloop()

class bouncy():  
    
    def get_hosts(self):
        
        wd = 'Host'
        host_names = []
        
        with open(homepath+"config", "r") as config:
            
            cfg = config.readlines()
                           
        for x in cfg:
            
            if re.search(r'\bHost\b', x):
                        
                host_names.append(x.strip().replace('Host ',''))
                                                   
            else:
                            
                continue
                    
        if len(host_names) <= 0:
                
            tkinter.messagebox.showinfo(title = "Warning", message = "No configuation found.")
            
            bouncy().wizard()
        else:
                
            bouncy().connect(host_names)
        
    def clear_current_config(self):
        
        cmd = "echo   > "+homepath+"/config"
                
        os.system(cmd)
        
        tkinter.messagebox.showinfo(title = "Done!", message = "SSH configuration file Cleared!")
        
    def connect(self, host_names):
                           
        def execute():
            
            cmd = "ssh "+variable.get()
            
            exec_cmd = "gnome-terminal -x sh -c \""+cmd+"; bash\""
                   
            connect_screen.destroy()
            
            os.system("rm -rf ufile.tmp")
            
            os.system(exec_cmd)
            
        hostname = StringVar()
        
        connect_screen = Tk()
        connect_screen.title("Start SSH Session")
        connect_screen.geometry("300x125")
        connect_screen.iconbitmap('@bouncy.xbm')
        connect_screen.resizable(height = 0, width = 0)
        Label(connect_screen, text="Connect").pack()
        
        #connect window
        variable = StringVar(connect_screen)
        variable.set(host_names[0])        
        Label(connect_screen, text="Select Hostname").pack()
        host_ip_entry = OptionMenu(connect_screen, variable, *host_names)
        host_ip_entry.pack()
        
        Label(connect_screen, text="").pack()
        
        Button(connect_screen, text="Execute", width=10, height=1, command = execute).pack()
        bouncy().center(connect_screen)
        connect_screen.mainloop()  
    
    def help(self):

        help_window = Tk()
        help_window.iconbitmap('@bouncy.xbm')
        help_window.resizable(height = 0, width = 0)
        help_window.title("Help")
        txt_box = Text(help_window, height = 39, width = 128)
        txt_box.pack(side = LEFT)
        txt_box.insert(END, "\n Bouncy! - A multihop ssh client and config generator. Version 1.0.\n\n")
        txt_box.insert(END, " This tool makes it easier to create a multihop ssh tunnel.\n\n")
        txt_box.insert(END, " File Menu:\n\n")
        txt_box.insert(END, " Configuration Editor: Opens a configuration editor\n")
        txt_box.insert(END, " Clear Current SSH config: Clear the current ssh configuration file\n")
        txt_box.insert(END, " Wizard: Starts the ssh configuration wizard for multihopping\n")
        txt_box.insert(END, " Exit: Quits the program\n\n")
        txt_box.insert(END, " Session Menu:\n\n")
        txt_box.insert(END, " Start SSH Tunnel: Establishes a conneciton using the current configuration or by loading a new configuration file\n\n")
        txt_box.insert(END, " Help Menu:\n\n")
        txt_box.insert(END, " Help Contents: Displays this Help\n")
        txt_box.insert(END, " About: Displays the About Section\n\n")
        txt_box.insert(END, " Configuration editor:\n\n")
        txt_box.insert(END, " File Menu:\n\n")
        txt_box.insert(END, " Open: Loads a configuration file\n")
        txt_box.insert(END, " Export: Saves the configuration file\n")
        txt_box.insert(END, " Wizard: Starts the ssh configuration wizard for multihopping\n")
        txt_box.insert(END, " Exit: Quits the Editor\n\n")
        txt_box.insert(END, " Help Menu:\n\n")
        txt_box.insert(END, " About: Displays the About Section\n\n\n")        
        txt_box.insert(END, " Please direct any support or general questions to escambray@outlook.com\n\n")
        txt_box.insert(END, " (C) 2021. Made by Rey.\n")
        
        txt_box.config(font = system_font)
        txt_box.config(state=DISABLED)
        
        scrollb = Scrollbar(help_window, command=txt_box.yview)
        scrollb.pack(side=RIGHT, fill=Y)
        txt_box['yscrollcommand'] = scrollb.set
        bouncy().center(help_window)
        help_window.mainloop()
    
    def terminate(self):
 
        sys.exit()
    
    def center(self, win):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()     
    
    def about(self):
        
        about_board = Tk()
        about_board.geometry("450x125")
        about_board.title('About')
        about_board.iconbitmap('@bouncy.xbm')
        about_board.resizable(height = 0, width = 0)
        about_label = ttk.Label(about_board, font = system_font, text="\nBouncy! - A multihop SSH client and config generator. Version 1.0.\r")
        about_label1 = ttk.Label(about_board, font = system_font, text = "\n(C) 2021. Made by Rey.\n")
        about_button = ttk.Button(about_board, text ="Close", command = about_board.destroy)
        
        for item in [about_label, about_label1]:
            item.pack()
            item.configure(anchor = "center")
            
        about_button.pack()
        bouncy().center(about_board)
        about_board.mainloop()   
        
    def wizard(self):
        
        def get_ProxyJumps():
            
            def write_Proxies(*args):
                
                host_IP = host_ip_entry.get()
                c_port = port_entry.get()
                user = user_entry.get()
                cert = cert_entry.get()
                
                host_ip_entry.delete(0, END)
                user_entry.delete(0, END)
                cert_entry.delete(0, END)
                                
                with open("ufile.tmp", "r") as ufile:
                    
                    previous_user = ufile.read().strip()
                    
                with open(homepath+"config", "a") as temp:
                    
                    temp.write("Host "+user+"\r"+"User "+user+"\r"+"HostName "+host_IP+"\r"+"Port "+c_port+"\r"+"IdentityFile "+cert+"\r"+"ProxyJump "+previous_user+"\r\n\n")
                
                with open("ufile.tmp", "w") as ufl:
                   
                   ufl.write(user)
                    
            def get_cert_pj():
                
                cert_pj = filedialog.askopenfilename(initialdir = ".", defaultextension=".pem", filetypes=[("Identity Certificate", "*.*pem")], parent = wizard_screen_pj)
                
                if cert_pj:
                    
                    cert_entry.insert(END, cert_pj)            
            
            host_IP = StringVar()
            c_port = StringVar()
            user = StringVar()
            pwd = StringVar()
            cert_pj = StringVar()        
            
            wizard_screen_pj = Tk()
            wizard_screen_pj.title("Configuration Wizard")
            wizard_screen_pj.geometry("300x375")
            wizard_screen_pj.iconbitmap('@bouncy.xbm')
            wizard_screen_pj.resizable(height = 0, width = 0)
            Label(wizard_screen_pj, text="Proxy Information").pack()
            Label(wizard_screen_pj, text="").pack()
            
            #host portion
            Label(wizard_screen_pj, text="Host IP").pack()
            host_ip_entry = Entry(wizard_screen_pj, textvariable=host_IP)
            host_ip_entry.pack()
            
            # port portion
            Label(wizard_screen_pj, text="").pack()
            Label(wizard_screen_pj, text="Port - Leave Blank if using default").pack()
            port_entry = Entry(wizard_screen_pj, textvariable = c_port)
            port_entry.pack()
            port_entry.insert(END, "22")
            
            # username portion
            Label(wizard_screen_pj, text="").pack()
            Label(wizard_screen_pj, text="Username").pack()
            user_entry = Entry(wizard_screen_pj, textvariable=user)
            user_entry.pack()
            
            # cert portion
            Label(wizard_screen_pj, text="").pack()
            Label(wizard_screen_pj, text="Key file").pack()
            cert_entry = Entry(wizard_screen_pj, textvariable = cert_pj)
            cert_entry.pack()
            Process_bttn = Button(wizard_screen_pj, text="Fetch Fle", width=10, height=1, command = get_cert_pj)
            Process_bttn.pack()
    
            Label(wizard_screen_pj, text="").pack()
            
            Button(wizard_screen_pj, text="Next", width=10, height=1, command = write_Proxies).pack()
            bouncy().center(wizard_screen_pj)
            wizard_screen_pj.mainloop            
        
        def write_lz(*args):
            
            host_IP = host_ip_entry.get()
            c_port = port_entry.get()
            user = user_entry.get()
            cert = cert_entry.get()
            
            with open(homepath+"config", "w") as temp:
                
                temp.write("Host "+user+"\r"+"User "+user+"\r"+"HostName "+host_IP+"\r"+"Port "+c_port+"\r"+"IdentityFile "+cert+"\r\n\n")
                
            wizard_screen.destroy()
            
            with open("ufile.tmp", "w") as ufl:
                
                ufl.write(user)
                
            get_ProxyJumps()
                
        def get_cert():
            
            cert = filedialog.askopenfilename(initialdir = ".", defaultextension=".pem", filetypes=[("Identity Certificate", "*.*pem")], parent = wizard_screen)
            
            if cert:
                
                cert_entry.insert(END, cert)
            
        global wizard_screen
        global host_IP
        global c_port
        global user
        global cert 
        global host_ip_entry
        global port_entry
        global user_entry
        global password_entry
        global cert_entry 


        host_IP = StringVar()
        c_port = StringVar()
        user = StringVar()
        pwd = StringVar()
        cert = StringVar()        
        
        wizard_screen = Tk()
        wizard_screen.title("Configuration Wizard")
        wizard_screen.geometry("300x375")
        wizard_screen.resizable(height = 0, width = 0)
        wizard_screen.iconbitmap('@bouncy.xbm')
        Label(wizard_screen, text="First Jump Point").pack()
        Label(wizard_screen, text="").pack()
        
        #host portion
        Label(wizard_screen, text="Host IP").pack()
        host_ip_entry = Entry(wizard_screen, textvariable=host_IP)
        host_ip_entry.pack()
        
        # port portion
        Label(wizard_screen, text="").pack()
        Label(wizard_screen, text="Port - Leave Blank if using default").pack()
        port_entry = Entry(wizard_screen, textvariable = c_port)
        port_entry.pack()
        port_entry.insert(END, "22")
        
        # username portion
        Label(wizard_screen, text="").pack()
        Label(wizard_screen, text="Username").pack()
        user_entry = Entry(wizard_screen, textvariable=user)
        user_entry.pack()
        
        # cert portion
        Label(wizard_screen, text="").pack()
        Label(wizard_screen, text="Key file").pack()
        cert_entry = Entry(wizard_screen, textvariable = cert)
        cert_entry.pack()
        Process_bttn = Button(wizard_screen, text="Fetch Fle", width=10, height=1, command = get_cert)
        Process_bttn.pack()

        Label(wizard_screen, text="").pack()
        
        Button(wizard_screen, text="Next", width=10, height=1, command = write_lz).pack()
        bouncy().center(wizard_screen)
        wizard_screen.mainloop        
            
    def main(self):
        
        bouncy_main = Tk()
                
        menubar = Menu(bouncy_main)

        # create pulldown menues, and add them to the menu bar

        #File Menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Configuration Editor", font = system_font, command=view_edit().start)
        filemenu.add_command(label="Clear Current SSH config", font = system_font, command=self.clear_current_config)
        filemenu.add_command(label="Wizard", font = system_font, command=self.wizard)      
        filemenu.add_command(label="Exit", font = system_font, command=self.terminate)
        menubar.add_cascade(label="File", font = system_font, menu=filemenu)

        #Connection Menu
        connectmenu = Menu(menubar, tearoff=0)
        connectmenu.add_command(label="Start SSH tunnel", font = system_font, command=self.get_hosts)
        menubar.add_cascade(label="Session", font = system_font, menu=connectmenu)

        # Help Menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Contents", font = system_font, command=self.help)
        helpmenu.add_command(label="About", font = system_font, command=self.about)
        menubar.add_cascade(label="Help", font = system_font, menu=helpmenu)
        bouncy_main.config(menu=menubar)

        bouncy_main.title('Bouncy!')
        bouncy_main.configure(background='white')
        bouncy_main.geometry("250x10")
        bouncy_main.resizable(height = 0, width = 0)
        bouncy_main.iconbitmap('@bouncy.xbm')
        bouncy_main.protocol('WM_DELETE_WINDOW', self.terminate)
        bouncy().center(bouncy_main)
        bouncy_main.mainloop() 
        

if __name__ == '__main__': 
    
    bouncy().main()
