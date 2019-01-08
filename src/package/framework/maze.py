from abc import ABCMeta, abstractmethod


class Maze:

    @abstractmethod
    def get_maze(self):
        pass

    @abstractmethod
    def get_goal_positions(self):
        pass

    @abstractmethod
    def get_start_positions(self):
        pass

    @abstractmethod
    def get_size(self):
        pass
