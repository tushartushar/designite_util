import typer
from src.designite_diff import process

def main(oldpath: str, newpath:str, outputpath: str):
    process(oldpath, newpath, outputpath)

def entry_point():
    typer.run(main)

if __name__=="__main__":
    typer.run(main)