from Models.GameModels import *
from Models.TkinterModels import *


def main():
    main_layout = MainLayout(main)
    app = Game(main_layout)
    app.play()
    main_layout.mainloop()


# main function will run only if the file was run directly, and not imported.
if __name__ == "__main__":
    main()
