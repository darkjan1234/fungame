from cx_Freeze import setup, Executable

setup(
    name="Otin Game",
    version="1.0",
    description="this game is for fun only",
    executables=[Executable("script.py")],
)
