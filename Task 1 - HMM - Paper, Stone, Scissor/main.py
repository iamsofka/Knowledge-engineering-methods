import numpy as np
import matplotlib.pyplot as plot
from game import Game

def main():
    rps = Game()

    last_move = None
    iterations = 20

    variants = [Game.STONE, Game.SCISSORS, Game.PAPER]
    verbal = ['stone', 'scissors', 'paper']

    transition_matrix = [
        [1, 1, 1], # stone
        [1, 1, 1], # scissors
        [1, 1, 1]  # paper
    ]

    performance = 0
    performance_history = [0]
    x_axis_labels = [0]

    for i in range(0, iterations):
        move = input('Your move (0 - stone, 1 - scissors, 2 - paper): ')
        rps.move(int(move))

        if (last_move == None):
            ai_move = np.random.choice(variants)
        else:
            predicted = np.random.choice(variants, p = normalize_probabilities(transition_matrix[last_move]))
            ai_move = Game.rules[predicted].index(Game.LOSS)
            transition_matrix[last_move][int(move)] += 1

        last_move = int(move)
        result = rps.move(ai_move)

        performance -= result
        performance_history.append(performance)
        x_axis_labels.append(i + 1)

        if (result < 0): result_verbal = 'you lost'
        elif (result > 0): result_verbal = 'won'
        else: result_verbal = 'in a draw'

        print("Computer's move is: " + verbal[ai_move])
        print("You " + result_verbal)
    
    print("Performance: " + str(performance))
    print("Transition matrix: " + str(normalize_probabilities_matrix(transition_matrix)))

    plot.plot(x_axis_labels, performance_history, '-c')
    plot.xlabel('games')
    plot.ylabel('performance')
    plot.show()

def normalize_probabilities(values):

    probabilities = values.copy()

    sum_values = np.sum(probabilities)
    for i in range(0, len(probabilities)):
        probabilities[i] /= sum_values
    
    return probabilities

def normalize_probabilities_matrix(values):

    probabilities = values.copy()

    for i in range(0, len(probabilities)):
        probabilities[i] = normalize_probabilities(values[i])
    
    return probabilities

if __name__ == '__main__':
    main()