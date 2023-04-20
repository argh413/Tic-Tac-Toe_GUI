from Models.TkinterModels import *
import random


class Board:
    """
    Determines Board model.
    """
    wining_cases = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal cases
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical cases
                    [0, 4, 8], [2, 4, 6]]  # Diagonal cases

    def __init__(self):
        # Create Default Board
        self.__board = {}
        for a in range(0, 9):
            self.__board[a] = str(a)

    def update_board(self, x=None, o=None) -> None:
        """
        Makes changes on board dictionary according to values of x and o params.
        :param x: Position of X on board
        :param o: Position of O on board
        :return: None
        """
        if x is not None:
            self.__board[x] = "X"
        if o is not None:
            self.__board[o] = "O"

    def check_winner(self, player_marker: PlayerMarker) -> bool:
        """
        Due to player's moves, checks that if player can win or not.
        :param player_marker: A Player object.
        :return: Return True if player won the game.
        """
        selected = self.get_selected_places(player_marker)
        # Check that if player can win the game.
        for case in Board.wining_cases:
            if set(case).intersection(set(selected)) == set(case):
                return True
        return False

    def get_selected_places(self, player_marker: PlayerMarker) -> list:
        """
        Gets the places that player selected.
        :param player_marker: A Player object
        :return: List of player's selected places
        """
        selected = []
        # Fetch position numbers that player selected so far in the game and then put them into selected list.
        for i in self.__board:
            if self.__board[i] == player_marker.value:
                selected.append(i)
        return selected

    def check_unoccupied_places(self, *places) -> list:
        """
        Checks if places are occupied or not then return those one that are unoccupied.
        This function returns [] when there is no empty place among places param on board.
        :param places: Positions of board that are wanted to check.
        :return: List of unoccupied places
        """
        unoccupied_places = []
        for c in places:
            if self.__board[c] == str(c):
                unoccupied_places.append(c)
        return unoccupied_places

    def get_winning_move(self, player_marker: PlayerMarker) -> int | None:
        """
        Gets a move that can make player (Computer or User) winner
        :param player_marker: Determines player (X or O).
        :return: Position number that can make player winner of game.
        It returns None when there is no way to win.
        """
        winning_moves = []
        selected = self.get_selected_places(player_marker)
        lt = []  # List of every two elements (as tuple) of selected list.
        # Find cases of every two elements of selected list.
        # Ex) selected = [1,2,3] => lt = [(1,2),(1,3),(2,3)]
        for j in selected:
            k = 1
            while selected.index(j) + k <= len(selected) - 1:
                lt.append((j, selected[selected.index(j) + k]))
                k += 1
        # Get winning move due to all win cases.
        for case in Board.wining_cases:
            for i in lt:
                if set(case).intersection(set(i)) == set(i):
                    winning_moves.append(list(set(case).difference(set(i)))[0])
        for i in winning_moves:
            if self.check_unoccupied_places(i):
                return i
        return None


class Player:
    """
    Determines Player model and its common properties.
    """

    def __init__(self, marker: PlayerMarker = PlayerMarker.Unspecified):
        self.__marker = marker

    # Determines the marker that Player uses in the process of Game.
    @property
    def marker(self):
        return self.__marker

    @marker.setter
    def marker(self, marker: PlayerMarker):
        self.__marker = marker


class UserPlayer(Player):
    """
    Determines User Player model.
    This class inherits from Player class.
    """
    pass


class ComputerPlayer(Player):
    """
    Determines Computer Player model.
    This class inherits from Player class.
    """

    def make_a_move(self, board: Board) -> int | None:
        """
        Makes a move for computer due to scenario of the game.
        :return: selected position on board by computer
        """
        position = None
        if self.marker == PlayerMarker.Circle:
            if board.get_winning_move(PlayerMarker.Circle) is not None and board.check_unoccupied_places(
                    board.get_winning_move(PlayerMarker.Circle)):
                position = board.get_winning_move(PlayerMarker.Circle)
                board.update_board(o=position)
            elif board.get_winning_move(PlayerMarker.Cross) is not None and board.check_unoccupied_places(
                    board.get_winning_move(PlayerMarker.Cross)):
                position = board.get_winning_move(PlayerMarker.Cross)
                board.update_board(o=position)
            elif board.check_unoccupied_places(0, 2, 6, 8):
                position = random.choice(board.check_unoccupied_places(0, 2, 6, 8))
                board.update_board(o=position)
            elif board.check_unoccupied_places(4):
                position = random.choice(board.check_unoccupied_places(4))
                board.update_board(o=position)
            elif board.check_unoccupied_places(1, 3, 5, 7):
                position = random.choice(board.check_unoccupied_places(1, 3, 5, 7))
                board.update_board(o=position)
        elif self.marker == PlayerMarker.Cross:
            if board.get_winning_move(PlayerMarker.Cross) is not None and board.check_unoccupied_places(
                    board.get_winning_move(PlayerMarker.Cross)):
                position = board.get_winning_move(PlayerMarker.Cross)
                board.update_board(x=position)
            elif board.get_winning_move(PlayerMarker.Circle) is not None and board.check_unoccupied_places(
                    board.get_winning_move(PlayerMarker.Circle)):
                position = board.get_winning_move(PlayerMarker.Circle)
                board.update_board(x=position)
            elif board.check_unoccupied_places(0, 2, 6, 8):
                position = random.choice(board.check_unoccupied_places(0, 2, 6, 8))
                board.update_board(x=position)
            elif board.check_unoccupied_places(4):
                position = random.choice(board.check_unoccupied_places(4))
                board.update_board(x=position)
            elif board.check_unoccupied_places(1, 3, 5, 7):
                position = random.choice(board.check_unoccupied_places(1, 3, 5, 7))
                board.update_board(x=position)

        return position


class Game:
    """
    Composition of main entities and handles the logic of Game.
    """

    def __init__(self, main_layout: MainLayout):
        # Determines randomly whether the computer or the player goes first.
        self.__starter_player = random.choice([0, 1])  # 0 => User, 1 => Computer
        self.__board = Board()
        self.__user_player = UserPlayer()
        self.__computer_player = ComputerPlayer()
        self.__main_layout = main_layout
        self.__game_board_frame = GameBoardFrame(self.__main_layout)
        self.__marker_determiner_frame = MarkerDeterminerFrame(self.__main_layout)
        self.__game_status_frame = GameStatusFrame(self.__main_layout)
        self.__identifier_of_infinite_loop = None

    # Determines status of the game.
    @property
    def status(self):
        if self.__user_player.marker != PlayerMarker.Unspecified:
            if self.__board.check_winner(self.__user_player.marker):
                self.__game_status_frame.status = GameStatus.UserWon
                self.__game_board_frame.status = GameStatus.UserWon
                return GameStatus.UserWon
            elif self.__board.check_winner(self.__computer_player.marker):
                self.__game_status_frame.status = GameStatus.ComputerWon
                self.__game_board_frame.status = GameStatus.ComputerWon
                return GameStatus.ComputerWon
            # if check_unoccupied_places return [] for all positions on board, the game ends in tie
            elif not self.__board.check_unoccupied_places(0, 1, 2, 3, 4, 5, 6, 7, 8):

                self.__game_status_frame.status = GameStatus.Tie
                self.__game_board_frame.status = GameStatus.Tie
                return GameStatus.Tie
            else:
                self.__game_status_frame.status = GameStatus.InProgress
                self.__game_board_frame.status = GameStatus.InProgress
                return GameStatus.InProgress
        else:
            self.__game_status_frame.status = GameStatus.Starting
            self.__game_board_frame.status = GameStatus.Starting
            return GameStatus.Starting

    def play(self) -> None:
        if self.status == GameStatus.Starting:
            self.__specify_selected_marker()
            self.__identifier_of_infinite_loop = self.__game_board_frame.after(1, self.play)
        elif self.status == GameStatus.InProgress:
            self.__game_board_frame.after_cancel(self.__identifier_of_infinite_loop)
            if self.__starter_player == 1:
                position = self.__computer_player.make_a_move(self.__board)
                if position is not None:
                    self.__game_board_frame.insert_marker(position, self.__computer_player.marker)
                    MainLayout.show_info("Computer did it's move. Now it's your turn.")
            else:
                MainLayout.show_info("It's your turn!")
            self.__make_next_move()

    def __specify_selected_marker(self) -> None:
        # Defines an infinite loop to check if user marker is chosen or not.
        # Infinite loop will be canceled when user chose its marker.
        self.__identifier_of_infinite_loop = self.__marker_determiner_frame.after(1, self.__specify_selected_marker)
        if self.__marker_determiner_frame.selected_marker is not None and self.__user_player.marker == PlayerMarker.Unspecified:
            self.__game_board_frame.marker = self.__marker_determiner_frame.selected_marker
            if self.__marker_determiner_frame.selected_marker == PlayerMarker.Cross:
                self.__user_player.marker = PlayerMarker.Cross
                self.__computer_player.marker = PlayerMarker.Circle
            else:
                self.__user_player.marker = PlayerMarker.Circle
                self.__computer_player.marker = PlayerMarker.Cross
            self.__game_status_frame.user_marker = self.__user_player.marker
            self.__game_status_frame.computer_marker = self.__computer_player.marker
            # Cancels the infinite loop.
            self.__marker_determiner_frame.after_cancel(self.__identifier_of_infinite_loop)
            self.__marker_determiner_frame.destroy()

    def __make_next_move(self) -> None:
        # Defines an infinite loop to make a move for computer, just after that user made a move (make next move for computer).
        # Infinite loop will be canceled when game is finished.
        self.__identifier_of_infinite_loop = self.__game_board_frame.after(1, self.__make_next_move)
        if self.status == GameStatus.InProgress:
            if self.__game_board_frame.last_clicked_button is not None:
                if self.__user_player.marker == PlayerMarker.Cross:
                    # Updates board dictionary according to the position which user selected. 
                    self.__board.update_board(x=self.__game_board_frame.last_clicked_button)
                else:
                    # Updates board dictionary according to the position which user selected. 
                    self.__board.update_board(o=self.__game_board_frame.last_clicked_button)
                if not self.__board.check_winner(self.__user_player.marker):
                    position = self.__computer_player.make_a_move(self.__board)
                    self.__game_board_frame.insert_marker(position, self.__computer_player.marker)
                    self.__game_board_frame.last_clicked_button = None
        else:
            # Cancels the infinite loop.
            self.__game_board_frame.after_cancel(self.__identifier_of_infinite_loop)
            if self.status == GameStatus.UserWon:
                MainLayout.show_info("You won!")
            elif self.status == GameStatus.ComputerWon:
                MainLayout.show_info("Computer won!")
            elif self.status == GameStatus.Tie:
                MainLayout.show_info("Tie!")
