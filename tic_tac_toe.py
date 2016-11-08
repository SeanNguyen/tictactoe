class TicTacToe(object):
    # Game Constants
    PLAYER_SYMBOLS = ['X', 'O']
    PLAYER_SIZE = len(PLAYER_SYMBOLS)
    WINNING_LENGTH = 3

    DIRECTION_NORTH = 0
    DIRECTION_EAST  = 1
    DIRECTION_WEST  = 2
    DIRECTION_SOUTH = 3
    DIRECTION_NE    = 4
    DIRECTION_NW    = 5
    DIRECTION_SE    = 6
    DIRECTION_SW    = 7

    # Private Attributes
    __board = None
    __players = []
    __current_player = None
    __winner = None
    __move_count = 0

    # Public methods
    def start_game(self):
        self.__init_game()
        self.__draw_board()

        while not self.__winner and self.__move_count < len(self.__board) ** 2:
            input_cell_number = -1
            while not self.__is_valid_move_input(input_cell_number):
                input_cell_number = raw_input("{}, choose a box to place an '{}' into: ".format(self.__current_player["name"],
                                                                                            self.__current_player["symbol"]))

            input_row, input_col = self.__convert_user_input_to_position(input_cell_number)
            self.__board[input_row][input_col] = self.__current_player['symbol']

            if self.__check_current_player_winning_status(input_row, input_col):
                self.__winner = self.__current_player

            self.__current_player = self.__get_next_player()
            self.__move_count += 1
            self.__draw_board()


        self.display_winner()

    # Private Methods
    def __init_game(self):
        # Init board
        board_size = None
        while not board_size or not board_size.isdigit():
            board_size = raw_input("Board size: ")
        board_size = int(board_size)
        self.__board = [[None for col in xrange(board_size)] for row in xrange(board_size)]
        # Init players
        for i in xrange(TicTacToe.PLAYER_SIZE):
            self.__players.append({
                "name": raw_input("Enter name for Player %s: " % (i + 1)),
                "symbol": TicTacToe.PLAYER_SYMBOLS[i]
            })
        self.__current_player = self.__players[0]

    def __convert_user_input_to_position(self, input_cell_number):
        input_cell_number = int(input_cell_number)
        input_row = (input_cell_number - 1) // len(self.__board)
        input_col = input_cell_number % len(self.__board) - 1
        return input_row, input_col

    def __get_next_player(self):
        current_player_position = self.__players.index(self.__current_player)
        next_player_position = (current_player_position + 1) % TicTacToe.PLAYER_SIZE
        return self.__players[next_player_position]

    def __check_current_player_winning_status(self, last_move_row, last_move_col):
        # Horizontal
        row_streak = self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_WEST) + \
                     self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_EAST) + 1
        if row_streak >= TicTacToe.WINNING_LENGTH:
            return True

        # Vertical
        row_streak = self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_NORTH) + \
                     self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_SOUTH) + 1
        if row_streak >= TicTacToe.WINNING_LENGTH:
            return True

        # Diagonal
        row_streak = self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_NE) + \
                     self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_SW) + 1
        if row_streak >= TicTacToe.WINNING_LENGTH:
            return True
        row_streak = self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_NW) + \
                     self.__count_symbol_in_direction(self.__current_player["symbol"], last_move_row, last_move_col,
                                                      TicTacToe.DIRECTION_SE) + 1
        if row_streak >= TicTacToe.WINNING_LENGTH:
            return True

    def __count_symbol_in_direction(self, symbol, last_row, last_col, direction):
        if direction == TicTacToe.DIRECTION_NORTH:
            last_row += 1
        if direction == TicTacToe.DIRECTION_EAST:
            last_col += 1
        if direction == TicTacToe.DIRECTION_WEST:
            last_col -= 1
        if direction == TicTacToe.DIRECTION_SOUTH:
            last_row -= 1
        if direction == TicTacToe.DIRECTION_NE:
            last_row += 1
            last_col += 1
        if direction == TicTacToe.DIRECTION_NW:
            last_row += 1
            last_col -= 1
        if direction == TicTacToe.DIRECTION_SE:
            last_row -= 1
            last_col += 1
        if direction == TicTacToe.DIRECTION_SW:
            last_row -= 1
            last_col -= 1

        if not 0 <= last_row < len(self.__board) or not 0 <= last_col < len(self.__board):
            return 0
        if self.__board[last_row][last_col] != symbol:
            return 0
        return 1 + self.__count_symbol_in_direction(symbol, last_row, last_col, direction)


    def __is_valid_move_input(self, input_cell_number):
        try:
            input_cell_number = int(input_cell_number)
        except:
            return False
        # Check in range
        if not 0 < input_cell_number <= len(self.__board) ** 2:
            return False
        # Check empty
        row, col = self.__convert_user_input_to_position(input_cell_number)
        if self.__board[row][col]:
            return False
        return True

    def __check_winner(self):
        pass

    def display_winner(self):
        if self.__winner:
            print('Congratulations %s! You have won.' % (self.__winner['name']))
        else:
            print("Tie")

    def __draw_board(self):
        print('----' * (len(self.__board) - 1) + "---")
        for row_num, row in enumerate(self.__board):
            printed_row = []
            for col_num, cell in enumerate(row):
                printed_row.append("{:^3}".format(cell or str(len(self.__board) * row_num + col_num + 1)))
            print("|".join(printed_row))
            print('----' * (len(self.__board) - 1) + "---")


if __name__ == '__main__':
    tic_tac_toe = TicTacToe()
    tic_tac_toe.start_game()
