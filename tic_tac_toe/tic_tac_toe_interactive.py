# coding: utf-8

"""
Board format:

+----+----+----+
| 11 | 12 | 13 |
+----+----+----+
| 21 | 22 | 23 |
+----+----+----+
| 31 | 32 | 33 |
+----+----+----+
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
import logging

# Logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                    filename="./logs/tic_tac_toe_interactive.log",
                    filemode="w")
logger = logging.getLogger("tic_tac_toe.tic_tac_toe_interactive")

# Functions
def board(fig, L):
    """
    Draws the board
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object
        
    L : float
        Length of the board
        
    Returns
    -------
    None
    """

    tabx = np.linspace(0, L, 4)
    taby = tabx*1.
    X, Y = np.meshgrid(tabx, taby)

    fig.plot(X, Y,"k-")
    fig.plot(Y, X,"k-")
    fig.axis("equal")

	
def cross(fig, L, player, posx=0, posy=0):
    """
    Draws a cross
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object
        
    L : float
        Length of the board
        
    player : str
        Player's name
        
    posx : float
        Optional, x coordinate of the center of the cross
    
    posy : float
        Optional, y coordinate of the center of the cross
        
    Returns
    -------
    None
    """

    x = np.arange(-1, 2)*L/12.
    y = np.arange(-1, 2)*L/12.
    
    fig.plot(x + posx, y + posy, "r-")
    fig.plot(-x + posx, y + posy, "r-")
    fig.axis("equal")
    plt.title(f"{player}'s turn", fontsize = "x-large")
    plt.draw()

	
def circle(fig, L, player, posx=0, posy=0):
    """
    Draws a circle

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object

    L : float
        Length of the board

    player : str
        Player's name

    posx : float
        Optional, x coordinate of the center of the circle

    posy : float
        Optional, y coordinate of the center of the circle

    Returns
    -------
    None
    """

    R = 1.5*L/12
    theta = np.arange(0, 2*np.pi, 0.0001)
    
    fig.plot(R*np.cos(theta) + posx, R*np.sin(theta) + posy, "b-")
    fig.axis("equal")
    plt.title(f"{player}'s turn", fontsize="x-large")
    plt.draw()


def quadrant(coord, L):
    """
    Returns the quadrant of the board where the player has clicked

    Parameters
    ----------
    coord : numpy.ndarray
        Array of coordinates of the click

    L : float
        Length of the board

    Returns
    -------
    ix1 : int
        Index of the lower x coordinate of the quadrant

    ix2 : int
        Index of the upper x coordinate of the quadrant

    iy1 : int
        Index of the lower y coordinate of the quadrant

    iy2 : int
        Index of the upper y coordinate of the quadrant

    Lvec : numpy.ndarray
        Array of the coordinates of the board
    """

    x = coord[0,0]
    y = coord[0,1]
    
    Lvec = np.array([0, L/3., 2*L/3., L])
    
    ix1 = np.max(np.where(Lvec <= x))
    ix2 = np.min(np.where(Lvec >= x)) # Once we have ix1, ix2 = ix1 + 1
    
    iy1 = np.max(np.where(Lvec <= y))
    iy2 = np.min(np.where(Lvec >= y))

    return ix1, ix2, iy1, iy2, Lvec


def play(coord, L, play_num, starts, players, dicc, matrix, ax):
    """
    Places a cross or a circle in the board
    
    Parameters
    ----------
    coord : numpy.ndarray
        Array of coordinates of the click
        
    L : float
        Length of the board
        
    play_num : int
        Number of the play
        
    starts : int
        Number of the player who starts
        
    players : list
        List of the players' names
        
    dicc : dict
        Dictionary of the players' names and their symbols
        
    matrix : list
        List of the board
        
    ax : matplotlib.axes._subplots.AxesSubplot
        Axes object
        
    Returns
    -------
    None
    """

    ix1, ix2, iy1, iy2, Lvec = quadrant(coord, L)
    player = players[((starts + 1) % 2)*(play_num % 2 != 0) 
                       + starts*(play_num % 2 == 0)]
    
    if ((play_num % 2 == 0 and starts == 0) or 
        (play_num % 2 != 0 and starts == 1)):
        assert type(matrix[ix1][iy1]) !=  str,\
        "You can only choose empty spaces"
        
        matrix[ix1][iy1] = dicc[players[1]] # In the if statement, we have avoided the circle case
        cross(ax, L, player,
              posx=(Lvec[ix1] + Lvec[ix2])/2.,
              posy=(Lvec[iy1] + Lvec[iy2])/2.)
        
    elif ((play_num % 2 == 0 and starts == 1) or 
          (play_num % 2 != 0 and starts == 0)):
        assert type(matrix[ix1][iy1]) !=  str,\
        "You can only choose empty spaces"

        matrix[ix1][iy1] = dicc[players[0]]
        circle(ax, L, player,
                posx=(Lvec[ix1] + Lvec[ix2])/2.,
                posy=(Lvec[iy1] + Lvec[iy2])/2.)
        

def winner_position(matrix, piece):
    """
    Checks if there is a winner
    
    Parameters
    ----------
    matrix : list
        List of the board
        
    piece : str
        Symbol of the player
        
    Returns
    -------
    True if there is a winner, None otherwise
    """

    matrix = np.asarray(matrix)

    # In order to check if there is a winner, we have to exchange the first
    # row with the last one because we have assigned the bottom part of the
    # board to be the first row of the matrix
    matrix[[0,-1]] = matrix[[-1,0]]

    piece = np.asarray([piece for i in range(len(matrix[:,0]))])
    anti_matrix = np.fliplr(matrix)
    
    if ((np.diagonal(matrix) == piece).all() or
        (np.diagonal(anti_matrix) == piece).all()):
        return True
    
    for i in range(len(matrix[:,0])):
        if (matrix[:,i] == piece).all() or (matrix[i,:] == piece).all():
            return True


def check_winner(matrix, player, piece):
    """
    Checks if there is a winner and prints the winner's name

    Parameters
    ----------
    matrix : list
        List of the board

    player : str
        Player's name

    piece : str
        Symbol of the player

    Returns
    -------
    True if there is a winner, None otherwise
    """

    if winner_position(matrix, piece):
        plt.title(f"{player} wins", fontsize="x-large")
        return True
    

def main():
    # Board length
    L = 12

    # Players' names
    player1 = input(u"Player 1: ")
    player2 = input(u"Player 2: ")

    logger.info(f"{player1} plays with O and {player2} plays with X")

    dicc = {player1: "O", player2: "X"}
    players = [player1, player2]

    # Randomly choose who starts
    starts = np.random.randint(0, 2)
    logger.info(f"{player1*(starts == 0) + player2*(starts == 1)} starts\n")

    # Create the board
    matrix = [[0,0,0] for i in range(3)]

    # Create the figure
    fig = plt.figure(figsize = (5, 5))
    ax = fig.add_subplot(111)

    board(ax, L)
    logger.info("Board created")

    plt.title(f"{player1*(starts == 0) + player2*(starts == 1)}'s turn", 
              fontsize="x-large")

    # Play
    play_num = 1
    while True:
        while True:
            try:
                coord = fig.ginput() # Get the coordinates of the click
                coord = np.asarray(coord)
                
                plt.draw()

                play(coord, L, play_num, starts,
                     players, dicc, matrix, ax)
                break

            except AssertionError as error:
                logger.error(error)
                continue
        
        # Check if there is a winner
        if check_winner(matrix, player1, dicc[player1]):
            logger.warning(f"{player1} wins")
            break

        elif check_winner(matrix, player2, dicc[player2]):
            logger.warning(f"{player2} wins")
            break
        
        play_num += 1
        if play_num == 10:
            plt.title("Draw", fontsize="x-large")
            logger.warning("Draw")
            break
        
    plt.show()

if __name__ == "__main__":
    main()