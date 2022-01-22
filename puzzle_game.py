"""
    J.R. Cribbs
    CS5001 - Fall 2021
    Final Project

    Sliding Puzzle Game
    From Wikipedia: "A sliding puzzle challenges a player to slide
    pieces along certain routes to establish a certain end-configuration."
    This program uses Python Turtle Graphics to created an interactive sliding
    puzzle game
"""

import turtle
import puzzle_classes
import time
import random
import glob
import datetime


def set_screen() -> tuple:
    """
    sets up initial screen and draws the game board, returns user choices
    from first two dialogue boxes.
    parameters: none
    returns: user's name, number of moves (tuple)
    """
    # creating screen and turtle
    screen = turtle.Screen()
    tr = turtle.Turtle()
    tr.hideturtle()
    turtle.hideturtle()
    tr.speed(0)

    # setting screen size
    WIDTH, HEIGHT = 800, 800
    screen.setup(WIDTH, HEIGHT)

    # splash screen
    splash = puzzle_classes.Message("Resources/splash_screen.gif")
    time.sleep(3)
    splash.turtle.hideturtle()

    # dialog boxes, not allowed to enter "blank" or hit cancel button
    name = ""
    while name == "" or name == None:
        name = screen.textinput("Slide Puzzle 5001", "Please enter your name")

    moves = ""
    while moves == "" or moves == None:
        moves = screen.numinput("Slide Puzzle 5001", "Please enter the number of "
                                                     "moves you want (5 - 200)",
                                minval=5, maxval=200)

    # making game board
    make_game_boxes(tr)

    # making buttons
    make_buttons()

    # display leaderboard
    leader_board(tr)

    return name, moves


def make_game_boxes(turtle):
    """
    makes the individual game boxes on the screen
    parameters: turtle instance
    returns: none
    """
    # moving turtle and drawing puzzle box
    turtle.up()
    turtle.goto(-375, -200)
    turtle.down()

    turtle.color("black")
    turtle.width(4)
    draw_rectangle(500, 550, turtle)

    # moving and drawing leaderboard box
    turtle.up()
    turtle.goto(150, -200)
    turtle.down()

    turtle.seth(0)
    turtle.color("blue")
    draw_rectangle(230, 550, turtle)

    # moving and drawing status box
    turtle.up()
    turtle.goto(-375, -350)
    turtle.down()

    turtle.seth(0)
    turtle.color("black")
    draw_rectangle(750, 120, turtle)

def draw_rectangle(length, height, turtle):
    """
    draws a rectangle with inputted length and height
    parameters: two ints, and turtle instance
    returns: none
    """
    for i in range(2):
        turtle.forward(length)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)

def make_buttons():
    """
    makes buttons and tracks when quit button is clicked
    Parameters: none
    Returns: none
    """
    # creating buttons as new turtles using Buttons class
    quit_button = puzzle_classes.Buttons("Resources/quitbutton.gif", 300, -285)
    puzzle_classes.Buttons("Resources/loadbutton.gif", 200, -285)
    puzzle_classes.Buttons("Resources/resetbutton.gif", 100, -285)

    # capturing quit button clicks
    quit_button.turtle.onclick(quit_clicked)

def quit_clicked(x, y):
    """
    quits the game if 'quit' button is clicked
    parameters: x, y coordinates of click (not used in this function)
    returns: none
    """
    puzzle_classes.Message("Resources/quitmsg.gif")
    time.sleep(3)
    puzzle_classes.Message("Resources/credits.gif")
    time.sleep(4)
    quit()

def leader_board(turtle):
    """
    loads leaderboard file and displays on screen
    parameters: turtle instance
    returns: none
    """
    # setting starting position for leaderboard entries
    x_pos = 170
    y_pos = 300
    turtle.penup()
    turtle.goto(x_pos, y_pos)
    turtle.pendown()

    try:
        # reading from file and writing to leaderboard space
        style = ("Cambria", 20, "bold")
        with open("leaderboard.txt", mode="r") as infile:
            for line in infile:
                line = line.strip("\n")
                turtle.write(line, font=style)
                # moving turtle down on screen between leaders
                y_pos = y_pos - 50
                turtle.penup()
                turtle.goto(x_pos, y_pos)
                turtle.pendown()

    except FileNotFoundError:
        no_leader_board("leader_board()")

def load_file():
    """
    prompts for input if 'load' button clicked. returns user's choice.
    parameters: x, y coordinates of click (not used in this function)
    returns: play_game function with user's choice
    """
    screen = turtle.getscreen()
    files = [" "]

    # grabbing all .puz files from directory
    for puz in glob.glob("*.puz"):
        files.append(puz)

    # cleaning up text display
    files = "\n".join(files)

    # prompting for user input
    choice = ""
    while choice == "":
        choice = screen.textinput("Slide Puzzle 5000",
                                  "Please enter the name of the puzzle you"
                                  f" would like to load. Choices are: {files}")

    # if valid entry is given
    if choice == None:
        return choice, False

    elif choice in files:
        return choice, True

    else:
        # displaying error and logging incident
        invalid_file(choice, "load_file()")

        # return invalid entry
        return choice, False

def invalid_file(file_name: str, function_name: str):
    """
    notifies user if file does not exist, adds incident to error log
    parameters: incorrect file name, function that tried to access file
    returns: none
    """
    # display error message
    x = puzzle_classes.Message("Resources/file_error.gif")
    time.sleep(2)
    x.turtle.hideturtle()

    # log error
    date = datetime.datetime.now()
    date = date.strftime("%c")
    error_log = f"{date}: Error: File {file_name} does not exist or" \
                f" has bad puzzle size. Location: " \
                f"{function_name}"
    with open("5001_puzzle.err", mode="a") as outfile:
        outfile.write(error_log)
        outfile.write("\n")

def no_leader_board(function_name: str):
    """
    notifies user if leader board file does not exist, adds to error log
    parameters: function that tried to access leaderboard
    returns: none
    """
    x_pos = 170
    y_pos = 300
    tut = turtle.Turtle()
    style = ("Cambria", 15, "bold")

    # display no leader board message
    x = puzzle_classes.Message("Resources/leaderboard_error.gif")
    time.sleep(3)
    x.turtle.hideturtle()

    # log error
    date = datetime.datetime.now()
    date = date.strftime("%c")
    error_log = f"{date}: Error: Leaderboard not found. Location: " \
                f"{function_name}"
    with open("5001_puzzle.err", mode="a") as outfile:
        outfile.write(error_log)
        outfile.write("\n")

    # writing "no leaders" in leaderbox, allows game to continue
    tut.hideturtle()
    tut.penup()
    tut.goto(x_pos, y_pos)
    tut.pendown()

    tut.write("No Leaders", font=style)


def get_metadata(file_name: str) -> dict:
    """
    pulls metadata out of file, returns dictionary
    parameters: one file name - string
    returns: metadata dictionary
    """
    puzzle_data = []
    metadata = {}

    # reading file and putting all data into one list
    try:
        with open(file_name, mode="r") as puzzle_file:
            for each in puzzle_file:
                puzzle_data.append(each)
        # slicing list and cleaning up data
        for each in puzzle_data[0:4]:
            meta, value = each.split(":")
            value = value.strip("\n")
            value = value.strip(" ")
            if meta == "number" or meta == "size":
                metadata[meta] = int(value)
            else:
                metadata[meta] = value

    # calling file error logger, game continues
    except FileNotFoundError:
        return invalid_file(file_name, "get_metadata()")

    return metadata

def get_puzzle_list(file_name: str) -> list:
    """
    pulls puzzle image locations out of file. returns list
    parameters: one file name - string
    returns: list
    """
    puzzle_data = []
    picture_list = []

    # reading file and putting all data into one list
    try:
        with open(file_name, mode="r") as puzzle_file:
            for each in puzzle_file:
                puzzle_data.append(each)

        # slicing out metadata and cleaning up list data
        for each in puzzle_data[4::]:
            meta, picture = each.split(":")
            picture = picture.strip("\n")
            picture = picture.strip(" ")
            picture_list.append(picture)

    except FileNotFoundError:
        return invalid_file(file_name, "get_puzzle_list()")

    return picture_list


def make_tiles(metadata: dict, picture_list: list, reset_flag: bool):
    """
    takes in file data and places tiles. scrambles them if this is the first
    time puzzle has been loaded (reset button was not clicked)
    parameters: metadata dictionary, list of picture locations, reset flag
                (bool) that tells make_tiles if list needs to be
                scrambled (False = scrambled)
    returns: nested list of Tile objects, corresponding to position on board
    """

    # sqrt of total tiles = row length
    row_size = int((metadata["number"] ** 0.5))
    count = row_size
    x_pos = -300
    y_pos = 250
    turtle_list = []

    # scrambling tiles before placing
    if reset_flag == False:
        random.shuffle(picture_list)

    # building nested list
    for i in range(0, row_size):
        turtle_list.append([])
        # traversing picture_list and calling Tiles class for each image path
        for j in range(0, row_size):
            turtle_list[i].append(puzzle_classes.Tiles(metadata["size"],
                                                    picture_list.pop(0),
                                                    x_pos, y_pos))
            # moving next tile over to the right
            x_pos = x_pos + (metadata["size"] + 10)
            count -= 1

            # ending row and moving down
            if count == 0:
                x_pos = -300
                y_pos = y_pos - (metadata["size"] + 10)
                count = row_size

    return turtle_list

def play_game(file_name: str, reset_flag: bool, name: str, moves: int,
              click_count: int):
    """
    main game driver - builds tiles and sends them to game board, along with
    other critical data.
    parameters: file name of puzzle to be played (string), boolean flag if
                the reset button has been clicked (bool), name of player (str),
                number of moves (int), clicks so far (used if "reset" has been
                clicked)
    returns: none if good data, play_game() with new choice if bad data in file
    """
    # grabbing metadata and image data from file, checking if reset is clicked
    metadata = get_metadata(file_name)
    puzzle_list = get_puzzle_list(file_name)
    win_list = get_puzzle_list(file_name)
    thumbnail = metadata["thumbnail"]

    # checking good data/puzzle size
    check_size = metadata["number"] ** 0.5
    if not check_size.is_integer():
        file_name = metadata["name"]
        invalid_file(file_name, "play_game()")
        choice, bool = load_file()
        return play_game(choice, False, name, moves, 0)

    # making & placing tiles
    tile_list = make_tiles(metadata, puzzle_list, reset_flag)

    # creating game board
    game_board = puzzle_classes.GameBoard(tile_list, win_list, file_name, name,
                                          moves, click_count)

    # drawing tile boxes/thumbnail on board and checking for user clicks
    game_board.draw_boxes(reset_flag, thumbnail)
    game_board.screen.onclick(game_board.check_click)

def game_lost():
    """
    displays loss message and quits game if player loses
    parameters: none
    returns: none
    """

    puzzle_classes.Message("Resources/Lose.gif")
    time.sleep(3)
    puzzle_classes.Message("Resources/credits.gif")
    time.sleep(4)
    quit()

def game_won(player_name: str, move_count: int):
    """
    displays win message and updates leaderboard file if necessary
    parameters: player's name (str), move count (int)
    returns: none
    """
    winner_list = []

    # if moves are greater than/== 10, don't add to leaderboard
    if move_count >= 10:
        puzzle_classes.Message("Resources/winner.gif")
        time.sleep(3)
        puzzle_classes.Message("Resources/credits.gif")
        time.sleep(4)
        quit()
    else:
        # reading from file and writing to leaderboard space
        with open("leaderboard.txt", mode="r") as infile:
            for line in infile:
                winner_list.append(line)

        # slicing out metadata
        winner_list = winner_list[1::]

        # checking scores and changing list as necessary
        for i in range(len(winner_list)):
            score = int(winner_list[i][0])

            if score >= move_count:
                index = winner_list.index(winner_list[i])
                winner_list.insert(index, f"{move_count}: {player_name}\n")

        winner_list.insert(0, "Leaders:\n")

        # converting list to dict then back to list to remove duplicate entries
        winner_list = list(dict.fromkeys(winner_list))

        # overwriting leaderboard file with new data
        with open("leaderboard.txt", mode="w") as outfile:
            for item in winner_list:
                outfile.write(item)

        # displaying win message/credits and quitting game
        puzzle_classes.Message("Resources/winner.gif")
        time.sleep(3)
        puzzle_classes.Message("Resources/credits.gif")
        time.sleep(4)
        quit()

def main():

    name, moves = set_screen()
    play_game("mario.puz", False, name, moves, 0)

if __name__ == "__main__":
    main()
