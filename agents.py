import random
import time



def count_set_bits(number):
    count = 0
    while number:
        number &= number - 1
        count += 1
    return count


def heuristic(state):
    player=state.get_next_on_move()
    opponent = (player + 1) % 2
    if state.get_state_status() == player:
        return 1000000
    elif state.get_state_status() == opponent:
        return -1000000
    elif state.get_state_status() ==2:
        return 0#potencijalno ako je draw onda 0
    else:
        val=get_win_checkers_positions(state, player) - get_win_checkers_positions(state, opponent)
        if player ==1:
            val*=-1
        return val



def get_win_checkers_positions(state, player):
    if player == 0:
        opp = state.checkers_yellow
    else:
        opp = state.checkers_red
    val = 0
    for mask in state.win_masks:
        newVal = opp & mask
        if newVal ==0:
            val += 1
    return val


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_column(self, state, max_depth):
        pass



class Human(Agent):
    pass


class ExampleAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        time.sleep(random.random())
        columns = state.get_possible_columns()
        return columns[random.randint(0, len(columns) - 1)]

class MinMaxABAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        alpha=-float("inf")
        beta=float("inf")
        score = self.minmax([state,0,0],0,max_depth,alpha,beta)

        return score[2]

    def minmax(self, state, depth, max_depth, alpha, beta):
        state_data,heur,column = state
        if (max_depth != 0 and depth == max_depth) or state_data.get_state_status() is not None:
            if state_data.get_state_status() is not None:
                #heur *= (42 - depth)
                heur-=depth
                return [state_data, heur, column] #ako je pobednik return neki broj - depth, ako je ybog dubine vvrati heuristiku
            else:
                #heur*=(42-depth)
                return state
        player = state_data.get_next_on_move()
        columns = state_data.get_possible_columns()
        if player == 0:
            score = [state_data,-float("inf"),column]
            states = []
            for col in columns:
                new_state = state_data.generate_successor_state(col)
                states.append([new_state, heuristic(new_state),col])
            states.sort(key=lambda x: (-x[1], (3,2,4,1,5,0,6).index(x[2])))
            for state in states:
                #da li proveravati da li je kraj - ne treba
                score = max(score, self.minmax(state,depth+1,max_depth,alpha,beta), key=lambda x: x[1])
                alpha=max(alpha,score[1])
                if alpha>=beta:
                    break
            return score
        else:
            score = [state_data,float("inf"),column]
            states = []
            for col in columns:
                new_state = state_data.generate_successor_state(col)
                states.append((new_state, heuristic(new_state), col))
            states.sort(key=lambda x: (-x[1], (3, 2, 4, 1, 5, 0,6).index(x[2])))
            for state in states:
                score = min(score, self.minmax(state,depth+1,max_depth,alpha,beta), key=lambda x: x[1])
                beta = min(beta,score[1])
                if alpha>=beta:
                    break
            return score


class NegascoutAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        alpha = -float("inf")
        beta = float("inf")
        score = self.negascout([state, 0, 0], 0, max_depth, alpha, beta)

        return score[2]
    def negascout(self, state, depth, max_depth, alpha, beta):
        state_data,heur,column = state
        player = state_data.get_next_on_move()
        if (max_depth != 0 and depth == max_depth) or state_data.get_state_status() is not None:
            if state_data.get_state_status() is not None:
                #heur *= (42 - depth)
                heur-=depth
                if player == 1:
                    heur*=-1
                return [state_data, heur, column] #ako je pobednik return neki broj - depth, ako je ybog dubine vvrati heuristiku
            else:
                if player == 1:
                    heur*=-1
                #heur*=(42-depth)
                return [state_data, heur, column]
        columns = state_data.get_possible_columns()

        score = [state_data,-float("inf"),column]
        states = []
        for col in columns:
            new_state = state_data.generate_successor_state(col)
            states.append([new_state, heuristic(new_state),col])
        states.sort(key=lambda x: (-x[1], (3,2,4,1,5,0,6).index(x[2])))
        for i in range(0,len(states)):
            if i == 0:
                val = self.negascout(states[i], depth + 1, max_depth, -beta, -alpha)
                val[1]*=-1
            else:
                val = self.negascout(states[i],depth+1,max_depth,-alpha -1, -alpha)
                val[1]*=-1
                if alpha < val[1] and val[1] < beta:
                    val = self.negascout(states[i],depth+1,max_depth,-beta,-alpha)
                    val[1]*=-1
            #da li proveravati da li je kraj - ne treba
            score = max(score, val, key=lambda x: x[1])
            alpha=max(alpha,score[1])
            if alpha>=beta:
                break
        return score

