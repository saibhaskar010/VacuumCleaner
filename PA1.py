import numpy as np
import random
import matplotlib.pyplot as plt

class VacuumCleaner:
    def __init__(self, env, agent_program = 1):
        #Percept variables
        self.wall_sensor = 0
        self.dirt_sensor = 0
        self.home_sensor = 1

        self.state = {}

        self.position = (9,0)
        self.agent_program = agent_program
        self.action_count = 0

        #private variables
        self.__orientation = "U"
        self.__env = env

    def move_forward(self):
        if(self.wall_sensor == 0):
            update = self.__orintation_mapping()
            self.position = (self.position[0] + update[0], self.position[1] + update[1])
        else:
            print("Failed to move forward")


        self.percept()



    def turn_left(self):
        if self.__orientation == "U": self.__orientation = "L"
        elif self.__orientation == "D": self.__orientation = "R"
        elif self.__orientation == "L": self.__orientation = "D"
        else: self.__orientation = "U"

        self.percept()
    
    def turn_right(self):
        if self.__orientation == "U": self.__orientation = "R"
        elif self.__orientation == "D": self.__orientation = "L"
        elif self.__orientation == "L": self.__orientation = "U"
        else: self.__orientation = "D"

        self.percept()

    def suck(self):
        self.__env.clean_tile(self.position)

        self.percept()



    def turn_off(self):
        print(f"Turning off after performing {self.action_count} actions")
        return "off"

    def __orintation_mapping(self):
        mapping = {"U": (-1, 0), "D" : (1, 0), "L": (0, -1), "R": (0, 1)}
        return mapping[self.__orientation]

    def percept(self):
        update = self.__orintation_mapping()
        next_position = (self.position[0] + update[0], self.position[1] + update[1]) 
        if(self.__env.is_wall_ahead(next_position)):
            self.wall_sensor = 1
        else: 
            self.wall_sensor = 0
        
        if(self.__env.is_tile_dirty(self.position)):
            self.dirt_sensor = 1
        else:
            self.dirt_sensor = 0
        
        if(self.position == (9,0)):
            self.home_sensor = 1
        else:
            self.home_sensor = 0

    def random_choice(self, funcs, weights):
        return random.choices(funcs, weights = weights, k = 1)[0]

    
        

    def perf(self):
        return (self.action_count, self.__env.number_of_clean_tiles(),)

    def run(self):
        self.percept()
        performance_log = []
        count=0
        while True:
            count+=1
            if count%100==0:
                print(self.__env.print_env(self.position))
            if(self.agent_program == 1):   
                action = self.__agent_program_1()

            elif(self.agent_program == 2): 
                action = self.__agent_program_2()

            else:                          
                action = self.__agent_program_3()

            self.action_count += 1
            performance_log.append(self.perf())

            if(action() == "off"): 
                return performance_log


    def __agent_program_1(self):
        if self.dirt_sensor == 1:
            return self.suck
        elif self.home_sensor == 1 and self.wall_sensor == 1:
            return self.turn_off
        elif self.wall_sensor == 1 and self.home_sensor == 0:
            return self.turn_right
        else: 
            return self.move_forward


    def __agent_program_2(self):
        funcs= [self.turn_right,self.turn_left,self.move_forward,self.suck,self.turn_off]
        if self.__env.all_clear() == False:
            if self.dirt_sensor == 1 and self.wall_sensor == 1:
                weights = [0,0,0,100,0]

            elif self.wall_sensor == 1  and self.dirt_sensor == 0:
                weights = [50,50,0,0,0]

            elif self.wall_sensor == 0 and self.dirt_sensor == 0: 
                weights = [30,10,60,0,0]
            
            else:
                weights = [0,0,0,100,0]
        else:
             weights = [0,0,0,0,100]
                
        return self.random_choice(funcs=funcs,weights=weights)

    def __agent_program_2_backup(self):
        funcs= [self.turn_right,self.turn_left,self.move_forward,self.suck,self.turn_off]
        if self.dirt_sensor == 1 and self.wall_sensor == 1:
            weights = [0,0,0,100,0]

        elif self.wall_sensor == 1  and self.dirt_sensor == 0:
            weights = [50,48,0,0,2]

        elif self.wall_sensor == 0 and self.dirt_sensor == 0: 
            weights = [30,10,59,0,1]
        else:
            weights = [0,0,0,100,0]
                
        return self.random_choice(funcs=funcs,weights=weights)

    def __agent_program_3(self):
        pass



class Environment:
    '''
    Defines an environment for the vacuum cleaner to operate in
    '''

    def __init__(self, walls = False):
        if(walls):
            self.grid = [[1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
                         [2, 2, 1, 2, 2, 2, 1, 2, 2, 2],
                         [1, 1, 1, 1, 2, 1, 1, 1, 1, 1], 
                         [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 2, 1, 1, 1, 1, 1]]
        else:
            self.grid = [[1  for y in range(10)] for x in range(10)]
    

    def all_clear(self):
        for row in self.grid:
            if(1 in row):
                return False
        return True

    def clean_tile(self, position = (0,0)):
        '''
        Cleans the tile at given position

        '''
        self.grid[position[0]][position[1]] = 0


    def is_tile_dirty(self, position):
        '''
        Checks if tile is dirty
        '''

        return True if self.grid[position[0]][position[1]] == 1 else False

    def is_wall_ahead(self, position):
        '''
        Checks if a wall is in front of the agent
        '''

        if(position[0] == -1 or position[1] == -1 or position[0] == 10 or position[1] == 10 or (self.grid[position[0]][position[1]] == 2)):
            return True
        return False
        

    def print_env(self, position = None):
        ''' 
        This method is used to print the environment in its most current state. The x marks where the agent is. 
        2 represents a wall block
        1 represents a dirty tile
        0 represents a clean tile 
        '''

        for i in range(10):
            for j in range(10):
                if((i,j) == position and position):
                    print(f"x{self.grid[i][j]}", end = " ")
                else:
                    print(self.grid[i][j], end = " ")
            print()
        print()

    def number_of_clean_tiles(self):
        count = 0
        for row in self.grid:
            count += row.count(0)
        return count

def plot_perf(perf_log, title = None):
    X = [log[0] for log in perf_log]
    Y = [log[1] for log in perf_log]
    plt.xlabel("Number of actions")
    plt.ylabel("Number of clean tiles")
    if(title):
        plt.title(title)
    plt.plot(X,Y)
    plt.show()
    


#---------------------Agent Program 1-Without walls-------------------------


# env1 = Environment()
# vc = VacuumCleaner(env = env1, agent_program = 1)
# env1.print_env(vc.position)
# perf_log = vc.run()
# print(perf_log)
# env1.print_env(vc.position)
# plot_perf(perf_log, title = "Agent Program 1 (Without walls)")


#------------------------Agent Program 1-With walls--------------------------

# env2 = Environment(walls = True)
# vc = VacuumCleaner(env = env2, agent_program = 1)
# env2.print_env(vc.position)
# perf_log = vc.run()
# print(perf_log)
# env2.print_env(vc.position)
# plot_perf(perf_log, title = "Agent Program 2 (With walls)")


#---------------------Agent Program 2-Without walls-------------------------

list_of_end_log=[]
list_of_90= []
for i in range(50):
    env2 = Environment(walls = False)
    vc = VacuumCleaner(env = env2, agent_program = 2)
    env2.print_env(vc.position)
    p_log=vc.run()
    env2.print_env(vc.position)
    list_of_end_log.append(p_log[-1][0])
    for i in p_log:
        if i[1]==90:
            list_of_90.append(i[0])
            break


print(list_of_end_log)
y_cords= list_of_end_log
x_cords= range(len(list_of_end_log))
plt.bar(x_cords, y_cords)
plt.show()
print(list_of_90)

plt.bar(range(len(list_of_90)),list_of_90)
plt.show()

#---------------------Agent Program 2-With walls-------------------------
list_of_end_log=[]
list_of_90= []
for i in range(50):
    env2 = Environment(walls = True)
    vc = VacuumCleaner(env = env2, agent_program = 2)
    env2.print_env(vc.position)
    p_log=vc.run()
    print(p_log)
    env2.print_env(vc.position)
    list_of_end_log.append(p_log[-1][0])
    for i in p_log:
        if i[1]==76:
            list_of_90.append(i[0])
            break

print(list_of_end_log)
y_cords= list_of_end_log
x_cords= range(len(list_of_end_log))
plt.bar(x_cords, y_cords)
plt.show()

plt.bar(range(len(list_of_90)),list_of_90)
plt.show()


#---------------Agent Program 3--------------------------------
