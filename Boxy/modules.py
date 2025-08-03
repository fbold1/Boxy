import datetime

Clear=open("log","w")
Clear.write("")
Clear.close()

Log=open("log", "at", encoding="utf-8")
def log_ast(ast_list, log_file):


    with open(log_file, "at", encoding="utf-8") as f:
        f.write(f"DEBUG - {datetime.datetime.now()} - LOGGING AST\n")
        f.write("-----------------------------------------------------------------\n")
        f.write("ABSTRACT TREE (AST):\n")

        for ast in ast_list:
            tabs = 0
            for char in str(ast):
                if char in ["(", "["]:
                    f.write("\n")
                    tabs += 1
                    f.write(" " * tabs)
                elif char in [")", "]"]:
                    f.write("\n")
                    f.write(" " * tabs)
                    tabs -= 1
                f.write(char)
            f.write("\n---------------------------------------------------\n")

def log(text:str,logger:str=""):
    if logger=="":
        Log.write(f"{text}\n")
    else:
        Log.write(f"[{logger}]:"+text+"\n")


class Errors():
    WARING="WARING"
    SOFT_ERROR="SOFT ERROR"
    HARD_ERROR="HARD ERROR"

    def __init__(self):
        pass


def error(logger,errorType=Errors.HARD_ERROR,text="UNKNOWN ERROR..."):
    log("------------------------------------------------------------------------------------"+errorType)
    log(text,logger)


