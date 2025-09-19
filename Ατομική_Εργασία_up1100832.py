import tkinter as tk
import random
import winsound

class GameOfLife:

    def __init__(self, rows, cols, cell_size=15, speed=1, mode=0, world=1):    #init function
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.speed = speed
        self.running=1        #this parameter decides if the game is running or not
        self.mode=mode        #this parameter decides the mode(1=user or 0=random generated)
        self.world=world      #this parameter decides if the world is spherical or flat
        winsound.PlaySound('start', winsound.SND_FILENAME)
        if self.mode==0:
            self.grid = self.create_grid()
            self.start_drawing()
        elif self.mode==1:
            self.grid = self.default_grid()
            self.change(1)
        


    def create_buttons(self):    
        font1='Arial 10'
        #Create a start button
        self.start_button = tk.Button(self.window, text='Start', font=font1, bg='#40514E', fg='#11999E', activebackground = "#30E3CA",command=self.run)
        #Create a stop button
        self.stop_button = tk.Button(self.window, text='Pause', font=font1, bg='#40514E', fg='#11999E', activebackground = "#30E3CA", command=self.stop)
        #Create a change configuration button
        self.change_conf = tk.Button(self.window, text='Change configuration', font=font1, bg='#40514E', fg='#11999E', activebackground = "#30E3CA", command=self.change)
        #Create a reset button
        self.reset_rand_button = tk.Button(self.window, text='Reset Random', font=font1, bg='#40514E', fg='#11999E', activebackground = "#30E3CA", command=self.reset)
        #Create a new reset button
        self.reset_button = tk.Button(self.window, text='Wipe', font=font1, bg='#40514E', fg='#11999E', activebackground = "#30E3CA", command=self.wipe)
        #Create a close button
        self.close_button =tk.Button(self.window, text='Close', font=font1, bg='#40514E', fg='#11999E', activebackground = "#30E3CA", command=self.window.destroy)
        #Create a speed slider
        self.speed_slider = tk.Scale(self.window, from_=1, to=100, orient=tk.HORIZONTAL, font=font1,bg='#40514E',fg='#11999E', activebackground = "#30E3CA",label='Speed', command=self.change_speed)
        self.speed_slider.set(self.speed)
        #Pack buttons
        self.start_button.pack() 
        self.stop_button.pack()
        self.reset_rand_button.pack()
        self.reset_button.pack()
        self.change_conf.pack()
        self.close_button.pack()
        self.speed_slider.pack()

    def create_label(self):    #Creates labels of generation,population,births and deaths
        self.generation = 0
        self.births = 0
        self.deaths = 0
        self.calc_population()
        self.label1 = tk.Label(self.window, text=f'Generation: {self.generation}',bg='#40514E',fg='#11999E')
        self.label2 = tk.Label(self.window, text=f'Population: {self.population}',bg='#40514E',fg='#11999E')
        self.label3 = tk.Label(self.window, text=f'Births: {self.births}',bg='#40514E',fg='#11999E')
        self.label4 = tk.Label(self.window, text=f'Deaths: {self.deaths}',bg='#40514E',fg='#11999E')
        self.label1.pack()
        self.label2.pack()
        self.label3.pack()
        self.label4.pack()

    def update_generation_population(self):     #Update generation,population,births and deaths
        self.label1.config(text=f'Generation: {self.generation}')
        self.label2.config(text=f'Population: {self.population}')
        self.label3.config(text=f'Births: {self.births}')
        self.label4.config(text=f'Deaths: {self.deaths}')

    def create_grid(self):         #Creates random grid 
        grid = []               #Create new grid and loop through it
        for row in range(self.rows):
            grid.append([])
            for col in range(self.cols):  
                grid[row].append(random.randint(0, 1))        # Append a random number to the grid
        return grid

    def draw_grid(self):    #Draws grid of cells
        for row in range(self.rows):  #Loop through the grid
            for col in range(self.cols):  
                x1 = col * self.cell_size    #Get position
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.grid[row][col] == 1:   #If the cell is alive
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill='#30E3CA', outline='black')
                else:                           #If the cell is dead
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill='white', outline='black')

    def update(self):    #Update grid
        if self.running==1:       #If self.running=1 repeat yourself
            self.births = 0    #Reset births and deaths
            self.deaths = 0
            new_grid = []   
            for row in range(self.rows): #Create new grid
                new_grid.append([])
                for col in range(self.cols):
                    new_grid[row].append(self.get_new_cell_state(row, col))       #Append the new cell state to the grid
            #Update the grid
            self.grid = new_grid
            #Delete all the items on the canvas
            self.canvas.delete('all')
            #Draw the new grid
            self.draw_grid()
            self.window.after(500//self.speed, self.update)
            #Update the generation and population and births and deaths
            self.generation += 1
            self.calc_population()
            self.update_generation_population()

    def get_num_neighbours1(self, row, col):
        num_neighbours = 0        #Loop through the neighbours
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:     #If the cell is itself skip itt
                    continue
                neighbour_row = (row + i) % self.rows  #Apply modulo to wrap around the rows
                neighbour_col = (col + j) % self.cols  #Apply modulo to wrap around the columns
                num_neighbours += self.grid[neighbour_row][neighbour_col]    #Add the neighbour to the number of neighbours
        return num_neighbours

    def get_new_cell_state(self, row, col):
        if self.world==1 :       #If we have sheical world
            num_neighbours = self.get_num_neighbours1(row, col)           #Calculate neighbours
            current_state = self.grid[row][col]
        elif self.world==0 :      #If we have flat world 
            num_neighbours = self.get_num_neighbours0(row, col)           #Calculate neighbours
            current_state = self.grid[row][col]
    
        if current_state == 1 and (num_neighbours < 2 or num_neighbours > 3):       #If live cell and meet conditions return changed state state
            self.deaths+=1       #Add death
            return 0
        elif current_state == 0 and num_neighbours == 3:      #If dead cell and meet conditions return changed state
            self.births+=1     #Add birth
            return 1
        else:                         #Else return current state 
            return current_state

    def get_num_neighbours0(self, row, col):    #Calculates live neighbours of cell
        num_neighbours = 0
        for i in range(-1, 2):  #Loop through the neighbours
            for j in range(-1, 2): 
                if i == 0 and j == 0:    #If the cell is itself skip it
                    continue                 
                neighbour_row = row + i   #Calculate the neighbour row
                neighbour_col = col + j   #Calculate the neighbour column
                if neighbour_row < 0 or neighbour_row >= self.rows or neighbour_col < 0 or neighbour_col >= self.cols:    #If the neighbour is out of bounds skip it
                    continue                
                num_neighbours += self.grid[neighbour_row][neighbour_col]        #Add the neighbour to the number of neighbours
        return num_neighbours


    def run(self):    #Function to start running of the game
        self.running=1
        self.update()

    def reset(self):        #Reset grid function
        self.stop()      #Stop running
        self.grid = self.create_grid()     #Create new random grid
        self.canvas.delete('all')      #Delete old grid
        self.draw_grid()          #Call function to draw new greid
        self.generation = 0      #Reset genetration
        self.births=0           #Reset births
        self.deaths=0            #Reset deaths
        self.calc_population()     #Call function calculate new population
        self.update_generation_population()    #Call function to update generation and population

    def wipe(self):
        self.stop()      #Stop running
        self.grid = self.default_grid()     #Create new clear grid
        self.canvas.delete('all')      #Delete old grid
        self.draw_grid()          #Call function to draw new greid
        self.generation = 0      #Reset genetration
        self.births=0            #Reset births
        self.deaths=0            #Reset deaths
        self.calc_population()     #Call function calculate new population
        self.update_generation_population()    #Call function to update generation and population


    def change_speed(self, speed):      #Changes speed of game
        self.speed = int(speed)

    def calc_population(self):    #Calculate population
        self.population = 0     #Reset population
        for i in range(self.rows):
            for j in range(self.cols):     #Loop grid,if cell is live add one to self.population
                if self.grid[i][j]==1:
                    self.population+=1

    def start_drawing(self):      #Creates window of the game
        self.window = tk.Tk()
        self.window.configure(bg='#E4F9F5')
        self.canvas = tk.Canvas(self.window, width=self.cols*self.cell_size,height=self.rows*self.cell_size,bg='white')      #Canvas of cells
        self.canvas.pack()
        self.window.resizable(False, False)
        self.window.title('Game of Life')
        self.draw_grid()          #Call functions to finish the window  
        self.create_buttons()
        self.create_label()
        self.window.mainloop()

    def default_grid(self):       #Create grid with only dead cells
        grid = []
        for row in range(self.rows):  #Loop through the rows
            grid.append([])
            for col in range(self.cols):  #Loop through the columns
                grid[row].append(0)    #Append dead cell
        return grid


    def stop(self):    #stop running
        self.running=0


    def change(self,start=0):    #Creates window for the user to change the grid
        self.running=0
        self.new_window=tk.Tk()
        self.new_window.title('Game of Life Configuration')
        self.f=tk.Frame(self.new_window,bg='#E4F9F5')
        self.f.pack()
        for i in range(self.rows):     #Reads grid and creates the buttons accordingly 
            for j in range(self.cols):
                if self.grid[i][j]==1:   #If cell is alive create colored button
                    tk.Button(self.f,bg='#30E3CA',height=1,width=1).grid(row=i,column=j)
                elif self.grid[i][j]==0:   #If the cell is dead create white button
                    tk.Button(self.f,bg='white',height=1,width=1).grid(row=i,column=j)
        #Create finish button
        finish_b=tk.Button(self.f,text='Finished',font='Arial 15',bg='#40514E',fg='#11999E', activebackground = "#30E3CA",command=lambda: self.finished(start)).grid(row=self.rows+1,column=int(self.cols/3),columnspan=6)

        self.new_window.bind('<Button-1>',self.clicked)    #Activates functions when user clicks
        self.new_window.bind('<Button-3>',self.clicked1)
        self.new_window.mainloop()


    def clicked(self,event):       #Right click,creates live cell
        x = event.x_root - self.f.winfo_rootx()    #Identify clicks
        y = event.y_root - self.f.winfo_rooty() 

        z=self.f.grid_location(x,y)  #Get coordinates of click 
        if z[1]!=self.rows+1:       #If button different from finished button
            x1=z[0]
            y1=z[1]
            self.grid[y1][x1]=1     #Change grid item 
            event.widget['bg']='#30E3CA'     #Change bg of button

    def clicked1(self,event):   #Left click,creates dead cell
        x = event.x_root - self.f.winfo_rootx()   #Identify clicks
        y = event.y_root - self.f.winfo_rooty()

        z=self.f.grid_location(x,y)    #Get coordinates of click
        if z[1]!=self.rows+1:     #If button different from finished button
            x1=z[0]
            y1=z[1]
            self.grid[y1][x1]=0   #Change grid item
            event.widget['bg']='white'      #Change bg of button
            


    def finished(self,start=0):
        if start==0:                 #If 0 (random generated mode),start game
            self.calc_population()
            self.update_generation_population()
            self.draw_grid()
            self.new_window.destroy()   #Close window
        elif start==1:             #If 1 (user generated mode),start game
            self.new_window.destroy()
            self.start_drawing()

class Dimentions:               #Window to get dimentions
    def __init__(self,i):    
        self.new_root = tk.Tk()
        self.i=i               #i difines the mode,if i=0 random generated mode,if i=1 user generated mode
        self.new_root.configure(bg='#E4F9F5')
        self.new_root.title("Conway's Game of Life Dimensions")
        self.labelx = tk.Label(self.new_root,text='Enter x dimension (between 6 to 28)',font='Arial 15',bg='#E4F9F5')   #Label and entry for x dimension
        self.labelx.pack()
        self.entryx = tk.Entry(self.new_root,font='Arial 15',bg='#40514E',fg='#11999E')
        self.entryx.pack()
        self.labely = tk.Label(self.new_root,text='Enter y dimension (between 6 to 28)',font='Arial 15',bg='#E4F9F5')   #Label and entry for y dimension
        self.labely.pack()
        self.entryy = tk.Entry(self.new_root,font='Arial 15',bg='#40514E',fg='#11999E')
        self.entryy.pack()
        self.labelc = tk.Label(self.new_root,text='Enter cell size (between 6 to 16)',font='Arial 15',bg='#E4F9F5')   #Labeel and entry for cell size
        self.labelc.pack()
        self.entryc = tk.Entry(self.new_root,font='Arial 15',bg='#40514E',fg='#11999E')
        self.entryc.pack()
        self.button = tk.Button(self.new_root,text ='Finished',font='Arial 15',bg='#40514E',fg='#11999E',activebackground='#30E3CA',command=lambda: self.pushed_dimensions(self.i))   #finished button
        self.button.pack()
        self.new_root.mainloop()

    def pushed_dimensions(self,i):
        try:
            x=int(self.entryx.get())             #Get dimensions and cell size
            y=int(self.entryy.get())
            cell_size=int(self.entryc.get())
            if (x>=6 and x<=28 and y>=6 and y<=28 and cell_size>=6 and cell_size<=16):   #If dimensions valid call window to choose world type
                self.new_root.destroy()
                self.world(i,x,y,cell_size)
                
            else:
                new_window=tk.Tk()                  #Window for wrong inputs
                new_window.configure(bg='#E4F9F5')
                new_window.title("Conway's Game of Life dimensions")
                label=tk.Label(new_window,text='Please enter valid dimensions',font='Arial 20',bg='#E4F9F5')
                label.pack()
                buttondes=tk.Button(new_window,text='OK',font='Arial 20',bg='#40514E',fg='#11999E',activebackground='#30E3CA',command=new_window.destroy)
                buttondes.pack()
                new_window.mainloop()
        except:
            new_window=tk.Tk()                  #Window for wrong inputs
            new_window.configure(bg='#E4F9F5')
            new_window.title("Conway's Game of Life dimensions")
            label=tk.Label(new_window,text='Please enter valid dimensions',font='Arial 20',bg='#E4F9F5')
            label.pack()
            buttondes=tk.Button(new_window,text='OK',font='Arial 20',bg='#40514E',fg='#11999E',activebackground='#30E3CA',command=new_window.destroy)
            buttondes.pack()
            new_window.mainloop()


    def world(self,i,x,y,cell_size):
        self.new_window=tk.Tk()                  #Window for choosing world type
        self.new_window.configure(bg='#E4F9F5')
        self.new_window.title("Conway's Game of Life World")
        label=tk.Label(self.new_window,text='Please choose world',font='Arial 20',bg='#E4F9F5')
        label.pack()
        button1=tk.Button(self.new_window,text='Spherical World',font='Arial 15',bg='#40514E',fg='#11999E',activebackground='#30E3CA',command=lambda: self.start(i,1,x,y,cell_size))
        button2=tk.Button(self.new_window,text='Flat World',font='Arial 15',bg='#40514E',fg='#11999E',activebackground='#30E3CA',command=lambda: self.start(i,0,x,y,cell_size))
        button1.pack()
        button2.pack()
        self.new_window.mainloop()
    
    def start(self,i,world,x,y,cell_size): #start game with right parameters and destroy previous window
        self.new_window.destroy()
        GameOfLife(y, x, cell_size, 1,i,world)





            

    
                
        
                
        


if __name__ == '__main__':
    root = tk.Tk()                 #Main window
    root.configure(bg='#E4F9F5')
    root.title("Conway's Game of Life")
    root.iconbitmap(True,'ghost-chase.ico')    #Window icon
    canvas = tk.Canvas(root, width=950, height=364)          #Canvas to put image to
    root.resizable(False, False)
    frame = tk.Frame(root, relief='raised', borderwidth=2)   
    canvas.pack()

#bg_img
    background_image = tk.PhotoImage(file='finalbackround.png')
    canvas.create_image((0,0),anchor='nw',image=background_image)

#btn1
    button1=tk.Button(root,text='RANDOM GENERATED GAME',font='Arial 10 bold',
                   bg='#40514E',fg='#11999E', activebackground='#30E3CA',
                   command=lambda: Dimentions(0))
    button1_window=canvas.create_window(350,200,width=220, height=40,anchor='nw', window=button1)

#btn2
    button2=tk.Button(root,text='USER GENERATED GAME',font='Arial 10 bold',
                  bg='#40514E',fg='#11999E', activebackground = "#30E3CA",
                  command=lambda: Dimentions(1))
    button2_window=canvas.create_window(350,240, width=220, height=40,anchor='nw', window=button2)



#btn3
    button3=tk.Button(root,text='ΕΧΙΤ',font='Arial 10 bold',
                  bg='#40514E',fg='#11999E',activebackground = "#30E3CA",
                  command=root.destroy)
    button3_window=canvas.create_window(350,280, width=220, height=40,anchor='nw', window=button3)

    root.mainloop()
