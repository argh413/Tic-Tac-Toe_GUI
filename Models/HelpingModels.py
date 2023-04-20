from enum import Enum


class PlayerMarker(Enum):
    """
    Determines all valid markers in game.
    This class created for reducing redundancy and increasing readability of the code.
    Values of each item specifies char of player marker.
    """
    Cross = "X"
    Circle = "O"
    Unspecified = None


class GameStatus(Enum):
    """
    Determines all cases of Game.
    This class created for reducing redundancy and increasing readability of the code.
    Values of each item are not worthwhile.
    """
    Starting = 0  # Used for the situation that user marker is not determined.
    InProgress = 1  # Used for the situation that the game is in progress and has not finished yet.
    UserWon = 2
    ComputerWon = 3
    Tie = 4
