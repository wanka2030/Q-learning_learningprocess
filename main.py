import numpy as np
import tkinter as tk
import random
import time
import matplotlib.pyplot as plt  # 新增

# 建立迷宮地圖
# -1 為起始點、0 為可行走的路、1 為牆、 2 為終點 
maze = np.array([
    [0, 0, -1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 2, 0]
])

class MazeWindow:
    def __init__(self, maze):
        self.root = tk.Tk()
        self.root.title('Maze Q-learning')
        self.maze = maze
        self.labels = np.zeros(self.maze.shape).tolist()
        self.plotBackground()
    def plotBackground(self):
        for i, row in enumerate(self.maze.tolist()):
            for j, element in enumerate(row):
                bg = 'black' if element == 1 else 'red' if element == 2 else 'green' if element == -1 else 'white'
                self.labels[i][j] = tk.Label(self.root, foreground='blue', background=bg, width=2, height=1, relief='ridge', font='? 40 bold')
                self.labels[i][j].grid(row=i, column=j)
    def mainloop(self, func):
        self.root.after(1000, func)
        self.root.mainloop()
    def target(self, indexes):
        for label in [item for row in self.labels for item in row]:
            label.config(text='')
        self.labels[indexes[0]][indexes[1]].config(text = 'o')
        self.root.update()

class Agent:
    def __init__(self, maze, initState):
        self.state = initState
        self.maze = maze
        self.initQTable()
        self.actionList = ['up', 'down', 'left', 'right']
        self.actionDict = {element : index for index, element in enumerate(self.actionList)}
    def initQTable(self):
        #建立Qtable
        Q = np.zeros(self.maze.shape).tolist()
        for i, row in enumerate(Q):
            for j, _ in enumerate(row):
                Q[i][j] = [0, 0, 0, 0] # up, down, left, right
        self.QTable = np.array(Q, dtype='f')
    def showQTable(self):
        for i, row in enumerate(self.QTable):
            for j, element in enumerate(row):
                print(f'({i}, {j}){element}')
    def showBestAction(self):
        for i, row in enumerate(self.QTable):
            for j, element in enumerate(row):
                Qa = element.tolist()
                action = self.actionList[Qa.index(max(Qa))] if max(Qa) != 0 else '??'
                print(f'({i}, {j}){action}', end=" ")
            print()
    def getAction(self, eGreddy=0.8):
        if random.random() > eGreddy:
            return random.choice(self.actionList)
        else:
            Qsa = self.QTable[self.state].tolist()
            return self.actionList[Qsa.index(max(Qsa))]
    def getNextMaxQ(self, state):
        return max(np.array(self.QTable[state]))
    def updateQTable(self, action, nextState, reward, lr=0.7, gamma=0.9):
        Qs = self.QTable[self.state]
        Qsa = Qs[self.actionDict[action]]
        Qs[self.actionDict[action]] = (1 - lr) * Qsa + lr * (reward + gamma *(self.getNextMaxQ(nextState)))

class Environment:
    def __init__(self):
        pass
    # 建立動作up、down、left、right 分別代表上、下、左、
    def getNextState(self, state, action):
        row = state[0]
        column = state[1]
        if action == 'up':
            row -= 1
        elif action == 'down':
            row += 1
        elif action == 'left':
            column -= 1
        elif action == 'right':
            column += 1
        nextState = (row, column)
        #判斷其他的狀況
        try:
            # 超出地圖範圍/撞牆
            if row < 0 or column < 0 or maze[row, column] == 1:
                return [state, False]
            # 抵達終點
            elif maze[row, column] == 2:
                return [nextState, True]
            # 還沒抵達
            else:
                return [nextState, False]
        except IndexError as e:
            # 撞牆
            return [state, False]
    # 根據行為進行獎懲機制
    def doAction(self, state, action):
        nextState, result = self.getNextState(state, action)
        # 碰到牆或是邊界，即執行完動作還停在原地，回饋 -10 分。
        if nextState == state:
            reward = -10
        # 到達終點，回饋 100 分。
        elif result:
            reward = 100
        # 可以移動，但沒有到達終點，回饋 -1 分
        else:
            reward = -1
        return [reward, nextState, result]
    
def main():    
    initState = (np.where(maze==-1)[0][0], np.where(maze==-1)[1][0])
    # Create an Agent
    agent = Agent(maze, initState)
    # Create a game Environment
    environment = Environment()
    step_history = []  # 新增：記錄每輪步數
    for j in range(0, 30):
        agent.state = initState
        m.target(agent.state)
        time.sleep(0.1)
        i = 0
        while True:
            i += 1
            # Get the next step from the Agent
            action = agent.getAction(0.9)
            # Give the action to the Environment to execute
            reward, nextState, result = environment.doAction(agent.state, action)
            # Update Q Table based on Environmnet's response
            agent.updateQTable(action, nextState, reward)
            # Agent's state changes
            agent.state = nextState
            m.target(agent.state)
            if result:
                print(f' {j+1:2d} : {i} steps to the goal.')
                step_history.append(i)  # 記錄步數
                break
    agent.showQTable()
    agent.showBestAction()
    # 顯示圖表
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(step_history)+1), step_history, marker='o')
    plt.title('Steps to reach the goal in each episode')
    plt.xlabel('Episode')
    plt.ylabel('Steps')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
m = MazeWindow(maze)
m.mainloop(main)
  
