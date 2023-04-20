import tkinter as tk
from tkinter import messagebox
from Models.HelpingModels import *


class MainLayout(tk.Tk):
    """
    Creates master(root) window for tkinter.
    """

    def __init__(self, starter_method):
        """
        Initializes MainLayout class.
        Configures root window for having suitable appearance.
        """
        super().__init__()
        self.__starter_method = starter_method  # Creates private attribute for starter_method property.
        self.title("Tic Tac Toe")  # Sets title for root window.
        self.resizable(False, False)  # Restricts root windows to change it's size.
        self.eval('tk::PlaceWindow . center')  # Sets root window to center of monitor.

    @staticmethod
    def show_info(text: str) -> None:
        """
        Shows an info messagebox using tkinter.messagebox
        Used for reduce dependency of other models to tkinter.messagebox
        :param text: text of messagebox
        :return: None
        """
        messagebox.showinfo("Tic Tac Toe", text)

    @staticmethod
    def show_warning(text: str) -> None:
        """
        Shows a warning messagebox using tkinter.messagebox
        Used for reduce dependency of other models to tkinter.messagebox
        :param text: text of messagebox
        :return: None
        """
        messagebox.showwarning("Tic Tac Toe", text)

    # Determines method which is starter of program.
    # Used for PlayAgain button.
    @property
    def starter_method(self):
        return self.__starter_method


class GameBoardFrame(tk.Frame):
    """
    Tkinter Frame for Game Board.
    """

    def __init__(self, main_layout: MainLayout):
        """
        Initializes GameBoardFrame class.
        Creates needed widgets for GameBoard.
        :param master: tkinter root window.
        :param marker: marker that should be shown in place of clicked button.
        """
        super().__init__(main_layout)
        self.pack()  # Packs frame to root windows.
        self.__marker = PlayerMarker.Unspecified  # Creates private attribute for marker property.
        self.__last_clicked_button = None  # Creates private attribute for last_clicked_button property.
        self.__status = GameStatus.Starting
        # Creates text variables for buttons.
        self.__string_vars = {}
        for i in range(0, 9):
            self.__string_vars[f"b{i}_string"] = tk.StringVar()
            self.__string_vars[f"b{i}_string"].set("")
        # Creates 9 buttons and configures their properties.
        self.__buttons = {}
        for i in range(0, 9):
            self.__buttons[f"b{i}"] = tk.Button(self, textvariable=self.__string_vars[f"b{i}_string"],
                                                command=lambda n=i: self.__on_click(n), height=4,
                                                width=8, font="Helvetica 20", state="normal")
        # Configures geometry of buttons.
        self.__buttons["b0"].grid(row=1, column=0)
        self.__buttons["b1"].grid(row=1, column=1)
        self.__buttons["b2"].grid(row=1, column=2)
        self.__buttons["b3"].grid(row=2, column=0)
        self.__buttons["b4"].grid(row=2, column=1)
        self.__buttons["b5"].grid(row=2, column=2)
        self.__buttons["b6"].grid(row=3, column=0)
        self.__buttons["b7"].grid(row=3, column=1)
        self.__buttons["b8"].grid(row=3, column=2)

    # Determines number of last button that user clicked on.
    @property
    def last_clicked_button(self):
        return self.__last_clicked_button

    @last_clicked_button.setter
    def last_clicked_button(self, button_number: int | None):
        self.__last_clicked_button = button_number

    # Determines the marker that should be shown in place of clicked button.
    @property
    def marker(self):
        return self.__marker

    @marker.setter
    def marker(self, marker: PlayerMarker):
        self.__marker = marker

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: GameStatus):
        if status != GameStatus.InProgress and status != GameStatus.Starting:
            # Changes state of all buttons to disable.
            # Used for the situation that game is finished
            for i in self.__buttons:
                self.__buttons[i]['state'] = 'disabled'
        self.__status = status

    def insert_marker(self, button_number: int | None, marker: PlayerMarker) -> None:
        """
        Sets marker to text variable of clicked button.
        :param button_number: Number of button that its text variable should be changed to marker.
        :param marker: Determines the marker that should be shown in place of clicked button.
        :return: None
        """
        if button_number is not None:
            self.__string_vars[f"b{button_number}_string"].set(marker.value)
            # Disables a button that its text variable changed to marker. (Prevents double-clicking on button)
            self.__buttons[f"b{button_number}"]["state"] = "disabled"
            if marker == PlayerMarker.Cross:
                self.__buttons[f"b{button_number}"]['disabledforeground'] = 'red'
            elif marker == PlayerMarker.Circle:
                self.__buttons[f"b{button_number}"]['disabledforeground'] = 'blue'

    def __on_click(self, button_number: int) -> None:
        """
        Callback method for click event.
        This method is private and cannot be accessed from outer.
        :param button_number: Number of button that user clicked on.
        :return: None
        """
        if self.status == GameStatus.InProgress:
            self.insert_marker(button_number, self.marker)
            self.last_clicked_button = button_number
        elif self.status == GameStatus.Starting:
            MainLayout.show_warning("First choose your marker!")


class MarkerDeterminerFrame(tk.Frame):
    """
    Tkinter Frame for specifying User marker in Game.
    """

    def __init__(self, main_layout: MainLayout):
        """
        Initializes MarkerDeterminerFrame class.
        Creates needed widgets for MarkerDeterminer frame.
        :param master: tkinter root window.
        """
        super().__init__(main_layout)

        self.__selected_marker = None  # Creates private attribute for selected_marker property.

        self.pack(padx=10, pady=10)  # Packs the frame to root window.

        self.__question_label = tk.Label(self, text="X or O ?")
        self.__question_label.pack(side="top", padx=5, pady=5)
        self.__x_button = tk.Button(self, text="X", width=10, fg="red",
                                    command=lambda m=PlayerMarker.Cross: self.__on_click(m))
        self.__x_button.pack(side='left', padx=5, pady=5)
        self.__o_button = tk.Button(self, text="O", width=10, fg="blue",
                                    command=lambda m=PlayerMarker.Circle: self.__on_click(m))
        self.__o_button.pack(side='right', padx=5, pady=5)

    # Determines the marker that user selected.
    @property
    def selected_marker(self):
        return self.__selected_marker

    def __on_click(self, marker: PlayerMarker) -> None:
        """
        Callback method for click event.
        This method is private and cannot be accessed from outer.
        :param marker: the marker that user selected
        :return: None
        """
        self.__selected_marker = marker


class GameStatusFrame(tk.Frame):
    """
    Tkinter Frame for showing status of Game.
    """

    def __init__(self, main_layout: MainLayout):
        """
        Initializes GameStatusFrame class.
        Creates needed widgets for GameStatus frame.
        :param master: Tkinter root window
        """
        super().__init__(main_layout)
        self.__status = GameStatus.Starting  # Creates private attribute for status property.
        self.__user_marker = tk.StringVar()  # Creates private attribute for user_marker property.
        self.__user_marker.set(f"User : {PlayerMarker.Unspecified.value}")
        self.__computer_marker = tk.StringVar()  # Creates private attribute for computer_marker property.
        self.__computer_marker.set(f"Computer : {PlayerMarker.Unspecified.value}")
        self.__l1 = tk.Label(self, textvariable=self.user_marker)
        self.__l1.pack(side="top", padx=5, pady=5)
        self.__l2 = tk.Label(self, textvariable=self.computer_marker)
        self.__l2.pack(side='top', padx=5, pady=5)
        self.__quit_button = tk.Button(self, text="Quit", width=10, command=exit, fg="red")
        self.__quit_button.pack(side="left", padx=5, pady=5)
        self.__play_again_button = tk.Button(self, text="PlayAgain", width=10,
                                             command=lambda: [main_layout.destroy(), main_layout.starter_method()],
                                             fg="green")

    # Determines User marker in the game. 
    @property
    def user_marker(self):
        return self.__user_marker

    @user_marker.setter
    def user_marker(self, user_marker: PlayerMarker):
        self.__user_marker.set(f"User : {user_marker.value}")

    # Determines Computer marker in the game. 
    @property
    def computer_marker(self):
        return self.__computer_marker

    @computer_marker.setter
    def computer_marker(self, computer_marker: PlayerMarker):
        self.__computer_marker.set(f"Computer : {computer_marker.value}")

    # Determines status of the game.
    @property
    def status(self):
        return self.__status

    # Used to make visible or invisible widgets when status changes.
    @status.setter
    def status(self, status: GameStatus):
        if status == GameStatus.InProgress:
            # Shows GameStatusFrame when game started.
            self.pack(padx=10, pady=10)
        elif status != GameStatus.InProgress and status != GameStatus.Starting:
            # Shows PlayAgain button when game was finished.
            self.__play_again_button.pack(side="right", padx=5, pady=5)
        self.__status = status
