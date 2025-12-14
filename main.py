from gui.main_window import HangmanWindow
from database import Base, engine

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app = HangmanWindow()
    app.mainloop()
