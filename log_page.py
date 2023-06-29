import tkinter as tk
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from API import api
import globals
import json
import csv
import os
from conversion import Convert
from tkinter import filedialog
import pandas as pd
from datetime import datetime
from datetime import timedelta

class LogPage(tk.Frame):

    def __init__(self, parent, controller):

        def confirm_popup():
            confirmed = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
            if confirmed:
                controller.navigate("LoginPage")
            else:
                pass

        def export_popup():
            messagebox.showerror("No graph", "Please navigate to the graph page to create a graph.")

        def import_popup():
            messagebox.showerror("Nowhere to import", "Please navigate to the graph page to import a file.")

        screen_width = controller.screen_width
        screen_height = controller.screen_height        

        tk.Frame.__init__(self, parent)
        self.config(width=screen_width, height=screen_height) 
        self.controller = controller
        
        # save entry button image to use in each selection
        save_image = Image.open(globals.root_dir + "images/data_entry_page/save.png")
        resized_save_image = save_image.resize((int(screen_width*0.06), int(screen_height*0.04)))
        self.save_button_image = ImageTk.PhotoImage(resized_save_image)

        # create log page canvas
        log_page_canvas = tk.Canvas(self, bg="#ffffff", width=screen_width, height=screen_height, 
                                 bd=0, highlightthickness=0, relief="ridge")
        log_page_canvas.place(x=0, y=0)

        button_size = int(screen_width*0.05)
        distance_between = int(screen_width*0.005)
        section_width = int(2 * button_size + 3 * distance_between)
        section_y_offset = screen_height*0.01
        button_y_offset = screen_height*0.032
        
        # ~~~ create toolbar ~~~

        # toolbar background
        toolbar_background_image = Image.open(globals.root_dir + "images/home_page/toolbar/toolbar_background.png")
        resized_toolbar_background = toolbar_background_image.resize((int(screen_width), int(screen_height*0.14)))
        self.toolbar_background = ImageTk.PhotoImage(resized_toolbar_background)
        log_page_canvas.create_image(0, 0, image=self.toolbar_background, anchor=tk.NW)        
        
        # profile picture
        profile_image = Image.open(globals.root_dir + "images/home_page/toolbar/signout.png")
        resized_profile_image = profile_image.resize((int(screen_height*0.12), int(screen_height*0.12)))
        self.profile_picture_image = ImageTk.PhotoImage(resized_profile_image)
        self.profile_button = tk.Button(self, image=self.profile_picture_image, borderwidth=0, 
                                        bg= "#D9D9D9", activebackground="#D9D9D9", command=lambda: confirm_popup())
        self.profile_button.place(x=screen_width*0.99, y=screen_height*0.01, anchor=tk.NE)

        # Import buttons section
        import_section_image = Image.open(globals.root_dir + "images/home_page/toolbar/import_section.png")
        resized_import_section = import_section_image.resize((section_width, int(screen_height*0.12)))
        self.import_section = ImageTk.PhotoImage(resized_import_section)
        log_page_canvas.create_image(.1*distance_between + .1*section_width, section_y_offset, image=self.import_section, anchor=tk.NW)
        # import from file button
        from_file_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/from_file_button.png")
        resized_from_file_image = from_file_button_image.resize((button_size, button_size))
        self.from_file_image = ImageTk.PhotoImage(resized_from_file_image)
        self.from_file_button = tk.Button(self, image=self.from_file_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", command=lambda: import_popup())
        self.from_file_button.place(x=.13*distance_between + .13*section_width, y=button_y_offset, anchor=tk.NW)
        # sync data button
        sync_data_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/sync_data_button.png")
        resized_sync_data_image = sync_data_button_image.resize((button_size, button_size))
        self.sync_data_image = ImageTk.PhotoImage(resized_sync_data_image)
        self.sync_data_button = tk.Button(self, image=self.sync_data_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", 
                                         command=lambda: self.sync_data())
        self.sync_data_button.place(x=.18*distance_between + .18*section_width + button_size, y=button_y_offset, anchor=tk.NW)
        
        # Export buttons section
        export_section_image = Image.open(globals.root_dir + "images/home_page/toolbar/export_section.png")
        resized_export_section = export_section_image.resize((section_width, int(screen_height*0.12)))
        self.export_section = ImageTk.PhotoImage(resized_export_section)
        log_page_canvas.create_image(1.15*distance_between + 1.15*section_width, section_y_offset, image=self.export_section, anchor=tk.NW)
        # export graph button
        export_graph_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/export_graph_button.png")
        resized_export_graph_image = export_graph_button_image.resize((button_size, button_size))
        self.export_graph_image = ImageTk.PhotoImage(resized_export_graph_image)
        self.export_graph_button = tk.Button(self, image=self.export_graph_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", command=lambda: export_popup())
        self.export_graph_button.place(x=1.18*distance_between + 1.18*section_width, y=button_y_offset, anchor=tk.NW)
        # export data button
        export_data_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/data_button.png")
        resized_export_data_image = export_data_button_image.resize((button_size, button_size))
        self.export_data_image = ImageTk.PhotoImage(resized_export_data_image)
        self.export_data_button = tk.Button(self, image=self.export_data_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", 
                                         command=lambda: self.export_data())
        self.export_data_button.place(x=1.23*distance_between + 1.23*section_width + button_size, y=button_y_offset, anchor=tk.NW)
    
        # New buttons section
        new_section_image = Image.open(globals.root_dir + "images/home_page/toolbar/new_section.png")
        resized_new_section = new_section_image.resize((section_width, int(screen_height*0.12)))
        self.new_section = ImageTk.PhotoImage(resized_new_section)
        log_page_canvas.create_image(2.2*distance_between + 2.2*section_width, section_y_offset, image=self.new_section, anchor=tk.NW)
        # new graph button
        new_graph_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/new_graph_button.png")
        resized_new_graph_image = new_graph_button_image.resize((button_size, button_size))
        self.new_graph_image = ImageTk.PhotoImage(resized_new_graph_image)
        self.new_graph_button = tk.Button(self, image=self.new_graph_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", 
                                         command=lambda: controller.navigate("HomePage"))
        self.new_graph_button.place(x=2.25*distance_between + 2.25*section_width, y=button_y_offset, anchor=tk.NW)
        # new record button
        new_record_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/new_record_button.png")
        resized_new_record_image = new_record_button_image.resize((button_size, button_size))
        self.new_record_image = ImageTk.PhotoImage(resized_new_record_image)
        self.new_record_button = tk.Button(self, image=self.new_record_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9",
                                         command=lambda: controller.navigate("DataEntryPage"))
        self.new_record_button.place(x=2.28*distance_between + 2.28*section_width + button_size, y=button_y_offset, anchor=tk.NW)
         #***************************
        # log buttons section
        log_section_image = Image.open(globals.root_dir + "images/home_page/toolbar/view_section.png")
        resized_log_section = log_section_image.resize((section_width, int(screen_height*0.12)))
        self.log_section = ImageTk.PhotoImage(resized_log_section)
        log_page_canvas.create_image(3.3*distance_between + 3.3*section_width, section_y_offset, image=self.log_section, anchor=tk.NW)
        
        # log button section
        new_log_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/extra_charting_button.png")
        resized_new_log_image = new_log_button_image.resize((button_size, button_size))
        self.new_log_image = ImageTk.PhotoImage(resized_new_log_image)
        self.new_log_button = tk.Button(self, image=self.new_log_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", 
                                         command=lambda: (controller.navigate("LogPage"), self.charts.close()))
        self.new_log_button.place(x=2.9*distance_between + 2.9*section_width + button_size, y=button_y_offset, anchor=tk.NW)
        
        #statistics button section
        new_statistics_button_image = Image.open(globals.root_dir + "images/home_page/toolbar/statistics_button.png")
        resized_new_statistics_image = new_statistics_button_image.resize((button_size, button_size))
        self.new_statistics_image = ImageTk.PhotoImage(resized_new_statistics_image)
        self.new_statistics_button = tk.Button(self, image=self.new_statistics_image, borderwidth=0,
                                         bg="#D9D9D9", activebackground="#D9D9D9", 
                                         command=lambda: (controller.navigate("StatisticsPage"), self.charts.close()))
        self.new_statistics_button.place(x=3.35*distance_between + 3.35*section_width + button_size, y=button_y_offset, anchor=tk.NW)


        font_size = int(screen_width*0.008)
        
        #Creating borders of sections
        #filterBox = tk.LabelFrame(self, bg='#FFFFFF', width=1000, height=100)
        filterBox = tk.LabelFrame(self, bg='#FFFFFF', width=screen_width*0.65, height=screen_height*0.115)
        filterBox.place(x=screen_width*0.1, y=screen_height*0.18, anchor=tk.NW)

        #resultBox = tk.LabelFrame(self, width=480, height=480)
        resultBox = tk.LabelFrame(self, width=screen_width*0.312, height=screen_height*0.55)
        resultBox.place(x=screen_width*0.1, y=screen_height*0.31, anchor=tk.NW)

        #displayBox = tk.LabelFrame(self, bg='#FFFFFF', width=500, height=480)
        displayBox = tk.LabelFrame(self, bg='#FFFFFF', width=screen_width*0.324, height=screen_height*0.55)
        displayBox.place(x=screen_width*0.426, y=screen_height*0.31, anchor=tk.NW)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Filter Box Code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #Initializing variables
        filterBox.filename = ""
        filterBox.data = {}
        filterBox.browseButtonText = tk.StringVar()
        filterBox.browseButtonText.set("Browse Files")

        filterBox.grid_propagate(False)

        # Select dataset to load
        select_dataset_label = tk.Label(filterBox, text="Select Dataset", font=((f"Helvetica, {font_size}")), bg="#ffffff")
        select_dataset_label.grid(row=0, column=0, sticky='W', padx=15)

        #creating the browse file button
        browseButton = tk.Button(filterBox, text="Browse Files", width=15, height=1, command=lambda: loadFile())
        browseButton.grid(row=1, column=0, sticky='W', padx=15)

        #Initializing the text box that displays the currently selected data file
        selectedFileBox = tk.Text(filterBox, height=1, width=18)
        selectedFileBox.grid(row=2, column=0, sticky='W')
        selectedFileBox.insert(tk.INSERT, "No File Selected")
        selectedFileBox.config(state="disabled")

        #Select event to filter
        select_event_label = tk.Label(filterBox, text='Select Event', font=((f"Helvetica, {font_size}")), bg="#ffffff")
        select_event_label.grid(row=0, column=1, sticky='W', padx=15)

        #Event drop down menu
        eventOptions = ["Medication", "Therapy", "Feeding", "Homecare", "No Filter"]
        selectedEventFilter = tk.StringVar()
        selectedEventFilter.set("No Filter")

        filterBox.event_dropdown = tk.OptionMenu(filterBox, selectedEventFilter, *eventOptions)
        filterBox.event_dropdown.config(width=10, height=1, borderwidth=0)
        filterBox.event_dropdown.grid(row=1, column=1, sticky='W', padx=15)

        #Date Range Radio Buttons label
        date_range_label = tk.Label(filterBox, text='Date Range', font=((f"Helvetica, {font_size}")), bg="#ffffff")
        date_range_label.grid(row=0, column=2, sticky='W', padx=15)
        
        #Date Range Radio Variable
        filterBox.dateRangeRadio = tk.IntVar()
        filterBox.dateRangeRadio.set(1)
        
        #Creating the custom date range
        startDateLabel = tk.Label(filterBox, text="Start Date:", font=((f"Helvetica, {font_size}")), bg="#ffffff")
        startDateLabel.grid(row=1, column=4, sticky='W', padx=15)
        startDate = DateEntry(filterBox, width=10, weekendbackground="#ffffff", weekendforeground="#000000", othermonthwebackground="gray93", othermonthweforeground="gray45")
        startDate.grid(row=1, column=5, sticky='W', padx=15)
        startDate.configure(state="disabled")

        endDateLabel = tk.Label(filterBox, text="End Date:", font=((f"Helvetica, {font_size}")), bg="#ffffff")
        endDateLabel.grid(row=2, column=4, sticky='W', padx=15)
        endDate = DateEntry(filterBox, width=10, weekendbackground="#ffffff", weekendforeground="#000000", othermonthwebackground="gray93", othermonthweforeground="gray45")
        endDate.grid(row=2, column=5, sticky='W', padx=15)
        endDate.configure(state="disabled")

        #functions to enable and disable the start/end date fields depending on if custom is selected
        def updateStateOff():
            startDate.configure(state="disabled")
            endDate.configure(state="disabled")

        def updateStateOn():
            startDate.configure(state="normal")
            endDate.configure(state="normal")

        #Creating the Radio Buttons
        filterBox.radio1 = tk.Radiobutton(filterBox, bg="#ffffff", text="Last 24 Hours", variable=filterBox.dateRangeRadio, value=1, command=updateStateOff)
        filterBox.radio2 = tk.Radiobutton(filterBox, bg="#ffffff", text="Last 7 Days", variable=filterBox.dateRangeRadio, value=2, command=updateStateOff)
        filterBox.radio3 = tk.Radiobutton(filterBox, bg="#ffffff", text="Last 30 Days", variable=filterBox.dateRangeRadio, value=3, command=updateStateOff)
        filterBox.radio4 = tk.Radiobutton(filterBox, bg="#ffffff", text="Custom", variable=filterBox.dateRangeRadio, value=4, command=updateStateOn)

        #placing the radio buttons with grid
        filterBox.radio1.grid(row=1, column=2, sticky='W', padx=15)
        filterBox.radio2.grid(row=2, column=2, sticky='W', padx=15)
        filterBox.radio3.grid(row=1, column=3, sticky='W', padx=15)
        filterBox.radio4.grid(row=2, column=3, sticky='W', padx=15)

        #creating the load button
        filterBox.loadButton = tk.Button(filterBox, text='Load', height=1, width=10, command=lambda: loadList())
        filterBox.loadButton.grid(row=1, column=6, sticky='W', padx=(120, 15))

        #Function to load a json dataset into the application
        def loadFile():
            filterBox.filename = filedialog.askopenfilename(initialdir="/", title="Select a Dataset File", filetypes=[("JSON files", "*.json")])
            with open(filterBox.filename) as file:
                filterBox.data = json.load(file)
            
            #grabbing the filename from the path
            name = os.path.split(filterBox.filename)[1]
            
            #clearing filename textbox and inserting the new filename
            selectedFileBox.config(state='normal')
            selectedFileBox.delete('1.0', tk.END)
            selectedFileBox.insert(tk.INSERT, name)
            selectedFileBox.config(state='disabled')


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Result Box Code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #keeping the label frame at it's set size
        resultBox.pack_propagate(False)

        #initializing the filtered list
        resultBox.filteredList = []

        #creating the canvas for the results box
        resultCanvas = tk.Canvas(resultBox, bg='#BBBBBB', height=480, width=450)
        resultCanvas.pack(side="left", fill='both', expand=1)

        #creating the scrollbar for the results box
        resultScroll = ttk.Scrollbar(resultBox, orient='vertical', command=resultCanvas.yview)
        resultScroll.pack(side='right', fill='y')

        #function to dynamically adjust the scroll region when the load button is pressed
        def adjustScrollRegion(event):
            resultCanvas.configure(scrollregion=resultCanvas.bbox('all'))

        #configuring the canvas
        resultCanvas.configure(yscrollcommand=resultScroll.set)
        resultCanvas.bind('<Configure>', lambda e: resultCanvas.configure(scrollregion=resultCanvas.bbox("all")))

        #creating the frame to store the canvas
        resultFrame = tk.Frame(resultCanvas)
        resultFrame.bind("<Configure>", adjustScrollRegion)
        resultCanvas.create_window((0,0), window=resultFrame, anchor='nw')

        #creating the export button
        exportButton = tk.Button(self, height=2, width=52, text="Export Filtered Data", font=((f"Helvetica, {font_size}")), command=lambda: exportFilteredData())
        exportButton.place(x=screen_width*0.1, y=(screen_height*0.31)+resultBox.winfo_height(), anchor=tk.NW)

        #function to load the event list into the results box
        def loadList():
            #checking if a dataset has been selected
            if len(filterBox.data) == 0:
                messagebox.showerror("No Dataset Selected", "Please click Browse Files and select a dataset file")
                return 0
            
            #clearing the dictionary on new load and reseting the event counter
            counter = 0
            tempList = {}
            resultBox.filteredList.clear()

            #clearing the frame
            for widget in resultFrame.winfo_children():
                widget.destroy()
           
            
            #creating the filtered event list
            for i in range(len(filterBox.data)):
                #grabbing the event type
                eventType = filterBox.data[i]['Type']

                #grabbing the date and time from the string
                date = (filterBox.data[i]['time'])[:10]
                time = (filterBox.data[i]['time'])[11:19]
                
                #converting the date and time into a datetime object
                dateFormat = "%Y-%m-%d %H:%M:%S"
                eventDateObject = "{0} {1}".format(date, time)
                eventDate = datetime.strptime(eventDateObject, dateFormat)

                #checking if event is within date range
                if filterBox.dateRangeRadio.get() == 1:
                    rangeEnd = datetime.now() - timedelta(days=1)
                    if eventDate < rangeEnd:
                        continue
                elif filterBox.dateRangeRadio.get() == 2:
                    rangeEnd = datetime.now() - timedelta(days=7)
                    if eventDate < rangeEnd:
                        continue
                elif filterBox.dateRangeRadio.get() == 3:
                    rangeEnd = datetime.now() - timedelta(days=30)
                    if eventDate < rangeEnd:
                        continue
                elif filterBox.dateRangeRadio.get() == 4:
                    start = startDate.get_date()
                    end = endDate.get_date()
                    tempDate = datetime.date(eventDate)
                    if tempDate > end or tempDate < start:
                        continue
                
                #checking if event type matches selected filter
                if selectedEventFilter.get() == "Medication" and eventType != "Medicine":
                    continue
                elif selectedEventFilter.get() == "Feeding" and eventType != "Food":
                    continue
                elif selectedEventFilter.get() == "Therapy" and eventType != "Therapy":
                    continue
                elif selectedEventFilter.get() == "Homecare" and (eventType == "Medicine" or eventType == "Food" or eventType == "Therapy"):
                    continue

                #storing the event index and time in templist
                tempList[i] = eventDateObject

            #sorting the tempList
            tempList = sorted(tempList.items(), key=lambda kv: kv[1])

            #creating the sorted filtered event list and its buttons
            for j in tempList:
                #storing the sorted event from data in the filteredList
                resultBox.filteredList.append(filterBox.data[j[0]])
                
                #grabbing the event type and date for the button labels
                eventType = resultBox.filteredList[counter]['Type']
                date = (resultBox.filteredList[counter]['time'])[:10]
                
                #formatting the label for each button
                label = "Event Type: {0}\nDate Logged: {1}".format(eventType, date)

                #creating the buttons
                e=tk.Button(resultFrame, justify="left", wraplength=200, anchor='w', font=((f"Helvetica, {font_size}")), text=label, height=3, width=30, command=lambda a=counter: displayInfo(a))
                e.grid(row=counter, column=0, pady=2)
                counter = counter + 1
            
        #function to export the filtered list into a json file
        def exportFilteredData():
            filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

            #checking if JSON
            if filename:
                extension = filename.split('.')[-1]
                if extension == "json":
                    with open(filename, 'w') as file:
                        json.dump(resultBox.filteredList, file)
                # elif extension == "csv":     #For future developers, add in a CSV export to this function


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Display Box Code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #creating the textbox to display information
        filler = 'No Event Has Been Selected Yet'
        infoBox = tk.Text(displayBox, height=20, width=40, font=((f"Helvetica, {font_size}")))
        infoBox.insert(tk.INSERT, filler)
        displayBox.pack_propagate(False)
        infoBox.pack(fill='both', expand=1)

        #function to load the specific data of a selected event into the display box
        def displayInfo(index):
            #clearing the display
            infoBox.config(state=tk.NORMAL)
            infoBox.delete('1.0', tk.END)

            #grabbing the info to be displayed
            date = (resultBox.filteredList[index]['time'])[:10]
            time = (resultBox.filteredList[index]['time'])[11:19]
            info = "Event ID: {0}\n\nUUID: {1}\n\nType: {2}\n\nTime: {3} at {4}\n\nAttributes:\n".format(resultBox.filteredList[index]['EventID'], resultBox.filteredList[index]['UUID'], resultBox.filteredList[index]['Type'], date, time)

            #adding the event attributes to the info being displayed
            attributeNum = len(resultBox.filteredList[index]['Attribute'])
            for i in range(attributeNum):
                if resultBox.filteredList[index]['Attribute'][i]['Type'] == "Text":
                    attrType = "Text"
                elif resultBox.filteredList[index]['Attribute'][i]['Type'] == "Int":
                    attrType = "Num"
                elif resultBox.filteredList[index]['Attribute'][i]['Type'] == "Length":
                    attrType = "Length"
                elif resultBox.filteredList[index]['Attribute'][i]['Type'] == "Rating":
                    attrType = "Rating"
                elif resultBox.filteredList[index]['Attribute'][i]['Type'] == "Time":
                    attrType = "Time"
                

                if "Time" in resultBox.filteredList[index]['Attribute'][i]:
                    continue
                else:
                    #creating the attribute string and appending it to the info
                    attribute = "\t{0}: {1}\n\n".format(resultBox.filteredList[index]['Attribute'][i]['Title'], resultBox.filteredList[index]['Attribute'][i][attrType])
                    info += attribute

            #inserting the info into the display and making it read only
            infoBox.insert(tk.INSERT, info)
            infoBox.config(state=tk.DISABLED)

    