from basicRobot import BasicRobot

# Shared Q matrix: No
# Expertness: None
# Weighting: None


class Artemis(BasicRobot):
    def __init__(self,id,maze,name):
        BasicRobot.__init__(self, id, maze, name)