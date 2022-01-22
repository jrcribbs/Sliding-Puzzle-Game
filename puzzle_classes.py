"""
    J.R. Cribbs
    CS5001 - Fall 2021
    Final Project

    classes to be used with puzzle_game.py
"""
import turtle
import puzzle_game

class Message(turtle.Turtle):
    """
    main screen messages for user
    attributes: turtle, picture (message to be displayed), current screen
    methods: __init__
    """
    def __init__(self, picture):
        """
        creates messages using a new turtle instance.
        Parameters: picture to be used as message, position (x,y) of button
        Returns: none
        """
        self.turtle = turtle.Turtle()
        self.picture = picture
        self.screen = turtle.getscreen()

        self.screen.addshape(picture)
        self.turtle.shape(picture)


class Buttons(turtle.Turtle):
    """
    creates buttons instances in correct location
    attributes: turtle, picture (message to be displayed), current screen
    methods: __init__
    """

    def __init__(self, picture, x_pos, y_pos):
        """
        creates buttons that are new turtle instances.
        Parameters: picture to be used as button, position (x,y) of button
        Returns: none
        """
        self.turtle = turtle.Turtle()
        self.picture = picture
        self.screen = turtle.getscreen()

        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(x_pos, y_pos)
        self.turtle.pendown()

        self.screen.addshape(picture)
        self.turtle.shape(picture)

class Tiles(turtle.Turtle):
    """
    creates tile objects and places them on the board
    attributes: turtle object, tile size, picture, current screen, x position
                of tile, y position of tile, index position of tile in master
                nested list, bool flag if clicked, bool flag if "blank" tile
                or not
    methods: __init__, check_click, swap_tiles, __str__
    """

    def __init__(self, tile_size, picture, x_pos, y_pos):
        self.turtle = turtle.Turtle()
        self.tile_size = tile_size
        self.picture = picture
        self.screen = turtle.Screen()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.row_index = 0
        self.index = 0
        self.clicked = False

        if "blank" in self.picture:
            self.is_blank = True
        else:
            self.is_blank = False

        # telling tiles where to go
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.goto(self.x_pos, self.y_pos)
        self.turtle.pendown()

        # adding tile picture
        self.screen.addshape(self.picture)
        self.turtle.shape(self.picture)

    def check_click(self, x, y):
        """
        checking if user is clicking on tile
        parameters: x, y
        returns: none
        """
        if x in range((self.x_pos - (self.tile_size // 2)),
                      (self.x_pos + (self.tile_size // 2))) and \
            y in range((self.y_pos - (self.tile_size // 2)),
                       (self.y_pos + (self.tile_size // 2))):
            self.clicked = True

            return self.clicked

    def swap_tiles(self, other):
        """
        moves tile to other tile's position. reassigns attributes accordingly
        parameters: two tile objects, self and other
        returns: none
        """

        # picking up pen and moving turtle
        self.turtle.penup()
        other.turtle.penup()

        self.turtle.goto(other.x_pos, other.y_pos)
        other.turtle.goto(self.x_pos, self.y_pos)
        
        self.turtle.pendown()
        other.turtle.pendown()

        # updating x, y for both tile objects
        self.x_pos, self.y_pos = self.turtle.pos()
        other.x_pos, other.y_pos = other.turtle.pos()

    def __str__(self):
        return f"Tile Object: {self.x_pos, self.y_pos}"

class GameBoard(turtle.Turtle):
    """
    controller for main game board. this class handles most of the game
    functionality including keeping track of player's move count, current
    positions of tiles, if win/lose condition was met, and tells Tiles when
    to move
    attributes: two turtles, nested list of tile objects, list of pictures in
                correct order, file name of current puzzle, player's name,
                total moves allowed, total moves so far (click_count), current
                screen
    methods: __init__, draw_boxes, display_moves, check_click, swap_tiles,
            check_outcome, check_win
    """

    def __init__(self, turtle_list, win_list, file_name, player_name,
                 total_moves, click_count):
        """
        constructor for GameBoard.
        parameters: list of tiles (turtle objects), list of picture file
                    locations in proper order, file name of current
                    puzzle (str), total player moves allowed (int),
                    total player moves so far (int)
        returns: none
        """
        self.turtle = turtle.Turtle() # boxes around tiles & makes thumbnail
        self.writing_turtle = turtle.Turtle() # writes player moves
        self.turtle_list = turtle_list
        self.win_list = win_list
        self.file_name = file_name
        self.player_name = player_name
        self.total_moves = int(total_moves)
        self.click_count = int(click_count)
        self.screen = turtle.getscreen()

        self.turtle.hideturtle()
        self.writing_turtle.hideturtle()

    def draw_boxes(self, reset_flag: bool, thumbnail: str):
        """
        drawing boxes around each of the tiles on the board, if first time
        placing them. then becomes thumbnail image
        parameters: bool, whether reset button has been clicked
        returns: none
        """
        THUMBNAIL_LOCATION = 335, 320

        if reset_flag == False:
            for each in self.turtle_list:
                for tile in each:
                    # moving turtle to starting position
                    self.turtle.speed(0)
                    self.turtle.penup()
                    self.turtle.goto(tile.x_pos - (tile.tile_size / 2),
                                     tile.y_pos + (tile.tile_size / 2))
                    self.turtle.pendown()
                    self.turtle.width(2)

                    # making squares around each tile
                    for i in range(4):
                        self.turtle.forward(tile.tile_size + 2)
                        self.turtle.right(90)

            # moving to position and displaying thumbnail
            self.turtle.penup()
            self.turtle.goto(THUMBNAIL_LOCATION)
            self.turtle.pendown()

            self.screen.addshape(thumbnail)
            self.turtle.shape(thumbnail)
            self.turtle.showturtle()

    def display_moves(self):
        """
        displays player move count on the board
        """

        # setting starting position for player count
        x_pos = -330
        y_pos = -300
        self.writing_turtle.penup()
        self.writing_turtle.goto(x_pos, y_pos)
        self.writing_turtle.pendown()

        # reading from file and writing to leaderboard space
        style = ("Cambria", 20, "bold")

        if self.click_count > 0:
            self.writing_turtle.clear()
            self.writing_turtle.write(f"Player Moves: {self.click_count}",
                                      font=style)

    def check_click(self, x, y):
        """
        checking user clicks and updating tiles as necessary
        parameters: two floats - x, y (user clicks)
        returns: none
        """
        # setting default index positions of blank and clicked tiles
        blank_row_index = 0
        blank_index = 0
        clicked_row_index = 0
        clicked_index = 0

        # looping through list and checking clicks
        for each in self.turtle_list:
            for tile in each:
                # capturing blank tile position
                if tile.is_blank == True:
                    blank_row_index = self.turtle_list.index(each)
                    blank_index = each.index(tile)
                    tile.row_index = blank_row_index
                    tile.index = blank_index

                # capturing clicked tile position
                if tile.check_click(x, y) == True and tile.is_blank == False:
                    clicked_row_index = self.turtle_list.index(each)
                    clicked_index = each.index(tile)
                    tile.row_index = clicked_row_index
                    tile.index = clicked_index

    # checking if clicked tile is a neighbor of blank and swapping if True

        # if clicked is to the left of blank tile
        if clicked_row_index == blank_row_index and clicked_index == \
                (blank_index - 1):

            # swapping tiles
            self.swap_tiles(blank_row_index, blank_index, clicked_row_index,
                            clicked_index)

            # incrementing click counter and displaying for user
            self.click_count += 1
            self.display_moves()

            # checking if game won or lost
            self.check_outcome()

        # if clicked is to the right of blank tile
        elif clicked_row_index == blank_row_index and clicked_index == \
                (blank_index + 1):

            # swapping tiles
            self.swap_tiles(blank_row_index, blank_index, clicked_row_index,
                            clicked_index)

            # incrementing click counter and displaying for user
            self.click_count += 1
            self.display_moves()

            # checking if game won or lost
            self.check_outcome()

        # if clicked is directly below blank tile
        elif clicked_row_index == blank_row_index - 1 and clicked_index == \
                blank_index:

            self.swap_tiles(blank_row_index, blank_index, clicked_row_index,
                            clicked_index)

            # incrementing click counter and displaying for user
            self.click_count += 1
            self.display_moves()

            # checking if game won or lost
            self.check_outcome()

        # if clicked is directly above blank tile
        elif clicked_row_index == blank_row_index + 1 and clicked_index == \
                blank_index:

            # swapping tiles
            self.swap_tiles(blank_row_index, blank_index, clicked_row_index,
                            clicked_index)

            # incrementing click counter and displaying for user
            self.click_count += 1
            self.display_moves()

            # checking if game won or lost
            self.check_outcome()

        # checking if reset button was clicked
        elif x in range(60, 140) and y in range(-320, -245):
            # setting bool flag
            reset_clicked = True

            # rebuilding game
            puzzle_game.play_game(self.file_name, reset_clicked,
                                  self.player_name, self.total_moves,
                                  self.click_count)

            self.writing_turtle.clear()
            self.screen.listen()

        # checking if load button was clicked
        elif x in range(160, 240) and y in range(-325, -250):
            choice, bool = puzzle_game.load_file()

            # if user hits cancel
            if choice is None:
                return

            # if user load choice is valid
            if bool == True:
                # clearing player moves and thumbnail
                self.writing_turtle.clear()
                self.turtle.shape("blank")

                # covering tile area in white box
                self.turtle.penup()
                self.turtle.goto(-360, 340)
                self.turtle.pendown()
                self.turtle.color("white")
                self.turtle.begin_fill()

                for i in range(2):
                    self.turtle.forward(480)
                    self.turtle.right(90)
                    self.turtle.forward(520)
                    self.turtle.right(90)
                self.turtle.end_fill()

                # re-running play_game function with new choice
                puzzle_game.play_game(choice, False, self.player_name,
                                      self.total_moves, 0)
            else:
                return

        else:
            print(x, y)

    def swap_tiles(self, blank_row_index, blank_index, clicked_row_index,
                   clicked_index):
        """
        swaps tiles if valid tile is clicked. changes both tile location and
        position within master_list
        parameters: index position of blank and clicked tiles
        returns: none
        """

        # getting blank and clicked tile locations within master list
        temp_blank = self.turtle_list[blank_row_index][blank_index]
        temp_target = self.turtle_list[clicked_row_index][clicked_index]

        # moving tiles on board
        temp_blank.swap_tiles(temp_target)

        # swapping tiles within master list
        self.turtle_list[blank_row_index].insert(blank_index,
                                                 temp_target)
        self.turtle_list[blank_row_index].pop(blank_index + 1)
        self.turtle_list[clicked_row_index].insert(clicked_index,
                                                   temp_blank)
        self.turtle_list[clicked_row_index].pop(clicked_index + 1)

    def check_outcome(self):
        """
        checking game outcome after each vaild click
        parameters: none
        returns: none
        """
        # checking if user lost
        if self.click_count == self.total_moves + 1:
            # disabling clicks
            self.screen.onscreenclick(print(""))
            # displaying lose message & credits, then quitting
            puzzle_game.game_lost()

        # checking if user won
        elif self.check_win() == True:
            # disabling clicks
            self.screen.onscreenclick(print(""))
            # running game_won function
            puzzle_game.game_won(self.player_name, self.click_count)

        else:
            return

    def check_win(self):
        """
        checks if tiles are in winning order
        parameters: none
        returns: bool - True if tiles are in winning order
        """
        current_list = []

        # grabbing picture list of current board
        for each in self.turtle_list:
            for tile in each:
                current_list.append(tile.picture)

        # comparing current board with winning list order
        if current_list == self.win_list:
            return True


