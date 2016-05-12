def get_next_position(self):
    if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
            self.x = self.x - 1
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
            self.y = self.y + 1
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
            self.x = self.x + 1
        elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
            self.y = self.y - 1
    elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
            self.x = self.x + 1
        elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
            self.y = self.y - 1
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
            self.x = self.x - 1
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
            self.y = self.y + 1
    elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
            self.y = self.y + 1
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
            self.x = self.x + 1
        elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
            self.y = self.y - 1
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
            self.x = self.x - 1
    elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
            self.y = self.y - 1
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
            self.x = self.x - 1
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
            self.y = self.y + 1
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
            self.x = self.x + 1

# not traveled by me
def get_next_position_nvbm(self):
    if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.traveled_map[self.y,self.x-1] == 0:
            self.x = self.x - 1
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
            self.y = self.y + 1
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
            self.x = self.x + 1
        elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
            self.y = self.y - 1
    elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
            self.x = self.x + 1
        elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
            self.y = self.y - 1
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.traveled_map[self.y,self.x-1] == 0:
            self.x = self.x - 1
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
            self.y = self.y + 1
    elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
            self.y = self.y + 1
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
            self.x = self.x + 1
        elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
            self.y = self.y - 1
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.traveled_map[self.y,self.x-1] == 0:
            self.x = self.x - 1
    elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
            self.y = self.y - 1
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-2,2] == self.traveled_map[self.y,self.x-1] == 0:
            self.x = self.x - 1
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
            self.y = self.y + 1
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
            self.x = self.x + 1

def get_next_position_nv(self):
    # coming from TOP
    if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y,self.x-1,0]  == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
            self.x = self.x - 1
            return True
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
            self.y = self.y + 1
            return True
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2]== self.maze[self.y,self.x+1,1] == 0:
            self.x = self.x + 1
            return True
        elif self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
            self.y = self.y - 1
            return True
    # coming from DOWN
    elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.maze[self.y,self.x+1,1] == 0:
            self.x = self.x + 1
            return True
        elif self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
            self.y = self.y - 1
            return True
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
            self.x = self.x - 1
            return True
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
            self.y = self.y + 1
            return True
    # coming from LEFT
    elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
            self.y = self.y + 1
            return True
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.maze[self.y,self.x+1,1] == 0:
            self.x = self.x + 1
            return True
        elif self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
            self.y = self.y - 1
            return True
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
            self.x = self.x - 1
            return True
    # coming from RIGHT
    elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
        if self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
            self.y = self.y - 1
            return True
        elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
            self.x = self.x - 1
            return True
        elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
            self.y = self.y + 1
            return True
        elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.maze[self.y,self.x+1,1] == 0:
            self.x = self.x + 1
            return True
    return False