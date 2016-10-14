def explore(self, mode):
    if mode == 0:
        action_list = []
        for action in range(4):
            action_list.append(action)
        numpy.random.shuffle(action_list)
        for action in action_list:
            next_pos = self.get_next_pos(action)
            if self.check_action(action):
                if next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                    self.update_q(action,next_pos,self.reward_goal)
                else:
                    self.update_q(action,next_pos,self.reward_step)
                return next_pos
            else:
                is_robot = False
                for robot in self.robot_list:  # check if robot
                    if next_pos[0] == robot.c_p[0] and next_pos[1] == robot.c_p[1]:
                        is_robot = True
                        break
                if is_robot:
                    self.update_q(action,next_pos,self.reward_robot)
                else:
                    self.update_q(action,next_pos,self.reward_wall)
        return self.c_p
    elif mode == 1:
        action_list = []
        # get actions to not visited places
        for action in range(4):
            pos_tmp = self.get_next_pos(action)
            if self.traveled_map[pos_tmp[0],pos_tmp[1],0] == 0:
                action_list.append(action)
        #numpy.random.shuffle(action_list)
        action_list.sort()
        for action in action_list:
            next_pos = self.get_next_pos(action)
            if self.check_action(action):
                if next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                    self.update_q(action,next_pos,self.reward_goal)
                else:
                    self.update_q(action,next_pos,self.reward_step)
                return next_pos
            else:
                self.update_q(action,next_pos,self.reward_wall)
        # get remaining actions
        action_list_2 = []
        for action in xrange(4):
            if action not in action_list:
                action_list_2.append(action)
        # numpy.random.shuffle(action_list_2)
        action_list.sort()
        for action in action_list_2:
            next_pos = self.get_next_pos(action)
            if self.check_action(action):
                if next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                    self.update_q(action,next_pos,self.reward_goal)
                else:
                    self.update_q(action,next_pos,self.reward_step)
                return next_pos
            else:
                self.update_q(action,next_pos,self.reward_wall)
        # stay
        return self.c_p