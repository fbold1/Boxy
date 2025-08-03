from interpreter import Interpreter
from modules import log_ast,log
Logger="Parser"

class Tokenizer:
    def __init__(self,code):
        self.code = code
        self.tokens = []
        pass

    def tokenize(self):
        i = 0
        while i < len(self.code):
            if self.code[i].isspace(): #Ha, a karakter space
                i += 1
            elif self.code[i].isdigit(): #ha szám
                num=""
                while i < len(self.code) and self.code[i].isdigit() or self.code[i]==",":
                    num+=self.code[i]
                    i+=1
                if "," in num:
                    self.tokens.append(("FLOAT",num))
                else:
                    self.tokens.append(("NUMBER",num))
            elif self.code[i].isalpha(): #ha szöveg - akármilyen szöveg
                text=""
                while i < len(self.code) and (self.code[i].isalpha() or self.code[i].isdigit()):
                    text+=self.code[i]
                    i+=1
                self.tokens.append(("TEXT",text))
            elif self.code[i] in ["+"]:
                self.tokens.append(("OP",self.code[i])) #ha operátor
                i+=1
            elif self.code[i] == "*": #ha csillag
                self.tokens.append(("ASTERISK",self.code[i]))
                i+=1
            elif self.code[i] == "/": #ha per
                self.tokens.append(("SLASH",self.code[i]))
                i+=1
            elif self.code[i] == "@": #ha @
                self.tokens.append(("REG",self.code[i]))
                i+=1
            elif self.code[i] == "#": #ha #
                self.tokens.append(("GET",self.code[i]))
                i+=1
            elif self.code[i] == ":": # ha :
                self.tokens.append(("COLON",self.code[i]))
                i+=1
            elif self.code[i] == "=": #ha =
                self.tokens.append(("EQUAL",self.code[i]))
                i+=1
            elif self.code[i] == ".": #ha .
                self.tokens.append(("DOT",self.code[i]))
                i+=1
            elif self.code[i] == "-": #ha -
                if i + 1 < len(self.code) and self.code[i + 1]=="-":
                    i+=2
                    self.tokens.append(("SECTION","--"))
                else:
                    self.tokens.append(("OP",self.code[i]))
                    i+=1
            elif self.code[i] in ["!","?"]: #ha !, vagy ?
                self.tokens.append(("BRANCH",self.code[i]))
                i+=1
            elif self.code[i] == '"':
                string=""
                i+=1
                while i < len(self.code) and self.code[i] != '"':
                    string+=self.code[i]
                    i+=1
                i+=1
                self.tokens.append(("STRING",string))

            elif self.code[i] == '$':
                i+=1
                while i < len(self.code) and self.code[i] != '$':
                    i+=1
                i+=1
            elif self.code[i] == "/" and i + 1 < len(self.code) and self.code[i + 1] == "/":
                if i + 2 < len(self.code) and self.code[i + 2] == "/":
                    # Többsoros komment: /// ... ///
                    i += 3
                    while i + 2 < len(self.code) and not (
                            self.code[i] == "/" and self.code[i + 1] == "/" and self.code[i + 2] == "/"):
                        i += 1
                    i += 3  # záró /// után továbblépünk
                else:
                    # Egysoros komment: // ...
                    i += 2
                    while i < len(self.code) and self.code[i] != "\n":
                        i += 1
            else:
                raise Exception("[TOKENIZER]: Illegal character: " + self.code[i])



class Parser:
    def __init__(self,tokens):
        self.ids = None
        self.tokens = tokens
        self.pos=0
        self.ast=[]

    def peek(self):
        return self.tokens[self.pos] if self.tokens[self.pos] else None

    def move(self, steps=1):
        if self.pos+steps <= len(self.tokens):
            self.pos+=steps
        else:
            raise Exception("[PARSER]: Illegal expression: unexpected end of expression, check if something is missing! (colons, dots, etc.")


    def match(self, token_type,delay=0):
        if self.tokens[self.pos][0] == token_type:
            return self.tokens[self.pos][1]
        else:
            return False


    def dot(self,must=False,caller=None):
        if self.match("DOT"):
            return True
        if must:
            if caller is None:
                raise Exception("[PARSER]: Illegal expression: missing dot!")
            else:
                raise Exception(f"[PARSER],[{caller}]: Illegal expression: missing dot!")
        return False


    def match_bool(self):
        if self.tokens[self.pos][1] == "True":
            return "TRUE"
        else:
            return "FALSE"



    def run_parser(self):
        while self.pos < len(self.tokens):
            new_ast=self.parse()
            if not new_ast:
                raise Exception("[PARSER]: Illegal expression!")
            self.ast.append(new_ast)
        return self.ast

    def parse(self):
        while self.pos < len(self.tokens):

            if self.peek()[0] == "NUMBER":
                integer=("INT",self.peek()[1])
                self.move(1)
                return integer
            elif self.peek()[0] == "FLOAT":

                new_float= ("FLOAT",self.peek()[1])
                self.move(1)
                return new_float

            elif self.peek()[0] == "STRING":
                string= ("STRING",self.peek()[1])
                self.move(1)
                return string
            elif self.peek()[0] == "BOOL":
                bool= ("BOOL",self.peek()[1])
                self.move(1)
                return bool
            elif self.peek()[0]=="REG":
                ids=[]
                while self.peek()[0] == "REG":
                    self.move(1)
                    new_id=self.peek()
                    if new_id:
                        ids.append(new_id)
                    self.move(1)
                if not self.match("COLON"):
                    raise Exception("[PARSER]: Illegal entity declaration! ':' is needed after the entity name")
                self.move()
                content=self.parse()
                return ("REGISTER",("ENTITY",ids,(content)))

            elif self.peek()[0] == "SLASH":
                self.move(1)
                if self.peek()[0] == "REG":
                    ids = []
                    while self.peek()[0] == "REG":
                        self.move(1)
                        new_id = self.peek()[1]
                        if new_id:
                            ids.append(new_id)
                        self.move(1)
                    self.dot(True)
                    self.move()
                    return ("REGISTER","LINE",ids)
                return ("OP","/")
            elif self.peek()[0] == "GET":
                ids=[]
                requirements="*"
                op=None
                values=[]
                while self.peek()[0] == "GET":
                    self.move(1)
                    new_id = self.peek()
                    if new_id:
                        ids.append(new_id)
                    self.move(1)

                if self.match("SLASH"):
                    self.move(1)
                    if self.match("TEXT"):
                        op=self.peek()[1]
                    self.move(1)
                    if self.match("SLASH"):
                        self.move(1)
                        while self.peek()[0] != "DOT":
                            value=self.parse()
                            if value[0]!="OP":
                                values.append(value)




                if self.match("COLON"):
                    self.move(1)
                    requirements=self.parse()
                    self.move(-1)

                    print(self.pos,"--------------------------------\n\nHOLAAAAAA\n\n")



                print(self.pos,self.tokens[self.pos][1],"\n\n\n")

                if self.dot():
                    self.move(1)
                    print("DOT!!!!",("GET",(ids,op,requirements)))
                    return ("GET",(ids,op,values,requirements))


            elif self.peek()[0] == "TEXT":
                text=self.match("TEXT")
                if text:
                    if text=="False":
                        self.move(1)
                        return ("BOOL","FALSE")
                    elif text=="True":
                        self.move(1)
                        return ("BOOL","TRUE")
                    if text=="new":
                        print("NEW ASSIGNMENT:", end=" ")
                        new_assign=self.assign()
                        if not new_assign:
                            raise Exception("[PARSER]: Illegal assignment!")
                        return new_assign
                    elif text=="run":
                        print("RUN FUNCTION:", end=" ")
                        self.move(1)
                        name=self.match("TEXT")
                        if not name:
                            raise Exception("[PARSER]: Illegal function name")
                        self.move(1)
                        asterisk=self.match("ASTERISK")
                        if not asterisk:
                            raise Exception("[PARSER]: Illegal Params declaration! * is needed after the function name")
                        self.move(1)
                        params=[]
                        while self.peek()[0] != "DOT":
                            new_param=self.parse()
                            if not new_param:
                                raise Exception("[PARSER]: Illegal Parameter name!")
                            params.append(new_param)
                        if self.dot(True):
                            self.move(1)
                            print(("RUN",(name,params)))
                            return ("RUN",(name,params))
                    elif text=="answer":
                        self.move(1)
                        answer=self.parse()
                        print("ANSWER: ",answer)

                        self.dot(True)
                        self.move(1)
                        print("RETURNING!")
                        return ("ANSWER",answer)
                    elif text=="while":
                        log("WHILE",Logger)
                        self.move(1)
                        if not self.match("ASTERISK"):
                            raise Exception("[PARSER]: Illegal condition!")
                        log("ASTERISK", Logger)
                        self.move(1)
                        condition=self.parse()
                        if not condition:
                            raise Exception("[PARSER]: Illegal condition!")
                        log(f"CONDITION:{condition}", Logger)

                        if not self.match("COLON"):
                            raise Exception("[PARSER]: Illegal body!")
                        log("COLON", Logger)
                        self.move(1)
                        body=[]

                        while self.peek()[0] != "DOT":
                            new_body=self.parse()
                            if not new_body:
                                raise Exception("[PARSER]: Illegal body!")
                            body.append(new_body)
                        if self.dot(True):
                            self.move(1)
                            print(("WHILE",(condition,body)))
                            return ("WHILE",(condition,body))

                    else:
                        if self.tokens[self.pos+1][0]=="EQUAL":
                            if self.tokens[self.pos+2][0]=="EQUAL":
                                compareison=self.compare()
                            reassignment=self.re_assign()
                        elif self.tokens[self.pos+1][0]=="SECTION":
                            reassignment=("SECTION",self.tokens[self.pos][1])
                            self.move(2)
                        else:
                            reassignment=("VAR",(text))
                            self.move()

                        if reassignment:
                            return reassignment

            elif self.peek()[0] == "BRANCH":
                if self.peek()[1]=="?":
                    branch=self.create_branch()
                    if not branch:
                        raise Exception("[PARSER]: Illegal branch!")
                    return branch
                else:
                    path=self.create_path()
                    if not path:
                        raise Exception("[PARSER]: Illegal path!")
                    return path
        else:
            raise Exception("[PARSER]: Illegal expression!")


    def compare(self):
        left=self.parse()
        if not left:
            raise Exception("[PARSER]: Illegal left operand!")
        self.move(2)
        right=self.parse()
        if not right:
            raise Exception("[PARSER]: Illegal right operand!")
        if left==right:
            self.move(1)
            return ("BOOL","TRUE")
        else:
            self.move(1)
            return ("BOOL","FALSE")


    def create_path(self):
        self.move(1)
        value=self.parse()
        if not value:
            raise Exception("[PARSER]: Illegal path value!")
        colon=self.match("COLON")
        if not colon:
            raise Exception("[PARSER]: Illegal path declaration! ':' is needed after the path value")
        self.move(1)
        body=[]
        while self.peek()[0] != "DOT":
            new_body=self.parse()
            if not new_body:
                raise Exception("[PARSER]: Illegal body!")
            body.append(new_body)

        if self.dot(True,"create_path"):
            self.move(1)
            print(("PATH",value,body))
            return ("PATH",value,body)


    def create_branch(self):
        self.move(1)
        value=self.parse()
        colon=self.match("COLON")
        if not colon:
            raise Exception("[PARSER]: Illegal branch declaration! ':' is needed after the branch value")
        self.move(1)
        body=[]
        while self.peek()[0] != "DOT":
            new_body=self.parse()
            if not new_body:
                raise Exception("[PARSER]: Illegal body!")
            body.append(new_body)
            print("DEBUG-----------------------------------------")
        if self.dot(True):
            self.move(1)
            print(("BRANCH",value,body))
            return ("BRANCH",value,body)
        raise Exception("[PARSER]: Illegal end of branch!")

    def assign_func(self):
        self.move(1)
        name=self.match("TEXT")
        if not name:
            raise Exception("[PARSER]: Illegal function name")
        self.move(1)
        asterisk=self.match("ASTERISK")
        if not asterisk:
            raise Exception("[PARSER]: Illegal Params declaration! * is needed after the function name")
        self.move(1)
        params=[]
        while self.peek()[0] != "COLON":
            new_param=self.parse()
            if not new_param:
                raise Exception("[PARSER]: Illegal Parameter name!")
            params.append(new_param)
        colon=self.match("COLON")
        if not colon:
            raise Exception("[PARSER]: Illegal body declaration! ':' is needed after the Params declaration")
        self.move(1)
        body=[]
        while self.peek()[0] != "DOT":
            new_body=self.parse()
            if not new_body:
                raise Exception("[PARSER]: Illegal body!")
            body.append(new_body)
        dot=self.match("DOT")
        if not dot:
            raise Exception("[PARSER]: Illegal end of function!")
        return ("FUNC",name,params,body)

    def assign_string(self):
        self.move(1)
        name=self.match("TEXT")
        if not name:
            raise Exception("[PARSER]: Illegal variable name")
        print(name, end=" ")
        self.move(1)
        equal=self.match("EQUAL")
        if not equal:
            self.dot(must=True)
            return ("STRING",name,"NULL")
        self.move(1)
        string=self.parse()
        self.dot(must=True)

        return ("STRING",name,string)


    def assign_bool(self):
        self.move(1)
        name=self.match("TEXT")
        if not name:
            raise Exception("[PARSER]: Illegal variable name")
        print(name, end=" ")
        self.move(1)
        equal=self.match("EQUAL")
        if not equal:
            dot=self.match("DOT")
            if not dot:
                raise Exception("[PARSER]: Illegal end of variable!")
            return ("BOOL",name,"FALSE")
        print("=", end=" ")
        self.move(1)
        bool=self.parse()
        self.dot(must=True)
        return ("BOOL",name,bool)

    def assign_int(self):
        self.move(1)
        name=self.match("TEXT")
        if not name:
            raise Exception("[PARSER]: Illegal variable name")
        print(name, end=" ")
        self.move(1)
        equal=self.match("EQUAL")
        if not equal:
            dot=self.match("DOT")
            if not dot:
                raise Exception("[PARSER]: Illegal end of variable!")
            return ("INT",name,"NULL")
        print("=", end=" ")
        self.move(1)
        number=self.parse()
        self.dot(True)
        return ("INT",name,number)

    def assign_float(self):
        name=self.match("TEXT")
        if not name:
            raise Exception("[PARSER]: Illegal variable name")
        print(name, end=" ")
        equal=self.match("EQUAL")
        if not equal:
            self.dot(must=True)
            return ("FLOAT",name,"NULL")
        print("=", end=" ")
        self.move(1)
        number=self.parse()
        self.dot(must=True)
        return ("FLOAT",name,number)






    def assign(self):
        self.move(1)
        assignment=[] # ("ASSIGN","FUNC","<name>",("PARAMS":("ASSIGN","BOOL","<name>","NULL")),("BODY":()))
        text=self.match("TEXT")
        if text:
            if text=="S" or text=="string":
                new_string=self.assign_string()
                if not new_string:
                    raise Exception("[PARSER]: Illegal assignment!")
                assignment=("ASSIGN",new_string)
            elif text=="b":
                new_bool=self.assign_bool()
                if not new_bool:
                    raise Exception("[PARSER]: Illegal assignment!")
                assignment=("ASSIGN",new_bool)
            elif text=="i":
                print("INT:", end=" ")
                new_int=self.assign_int()
                if not new_int:
                    raise Exception("[PARSER]: Illegal assignment!")
                assignment=("ASSIGN",new_int)
            elif text=="f":
                new_float=self.assign_float()
                if not new_float:
                    raise Exception("[PARSER]: Illegal assignment!")
                assignment=("ASSIGN",new_float)
            elif text=="func":
                print("FUNC:", end=" ")
                new_func=self.assign_func()
                if not new_func:
                    raise Exception("[PARSER]: Illegal assignment!")
                assignment=("CREATE",new_func)
                print("FUNC:", end=" ")
                print(new_func)
            elif text=="class":
                pass
            else:
                raise Exception("[PARSER]: Illegal assignment: " , text)
        if assignment:

            self.move(1)
            return assignment
        return None


    def re_assign(self):
        name=self.match("TEXT")
        if not name:
            raise Exception("[PARSER]: Illegal variable name")
        print(name, end=" ")
        self.move(1)
        equal=self.match("EQUAL")
        if not equal:
            raise Exception("[PARSER]: Illegal end of variable!")
        print("=", end=" ")
        self.move(1)
        new_value=self.parse()
        if not new_value:
            raise Exception("[PARSER]: Illegal value!")
        if not self.dot():
            raise Exception("[PARSER]: Illegal end of variable!")
        self.move(1)
        print(("REASSIGN",(new_value[0],name,(new_value[0],new_value[1]))))
        return ("REASSIGN",(new_value[0],name,(new_value[0],new_value[1])))

File=open( "code", "rt")
Log=open("log","at")

raw_code=('''''') #'''new func func* new b bool.:?bool:!False:answer True..!True:answer False....'''
t=Tokenizer(str(File.read()))
t.tokenize()
print(t.tokens)
p=Parser(t.tokens)
ast_list=p.run_parser()
print("-----------------------------------------------------------------\nABSTRACT TREE (AST): \n")
print(ast_list)


for ast in ast_list:
    tabs = 0
    for char in str(ast):


        if char in ["(","[",]:
            print("\n",end="")
            tabs += 1
            for tab in range(tabs):
                print(" ", end="")

        elif char in [")","]"]:
            print("\n",end="")

            for tab in range(tabs):
                print(" ", end="")
            tabs -= 1
        print(char, end="")

    print("\n---------------------------------------------------\n")

log_ast(ast_list,"log")

interpreter=Interpreter(ast_list)
print("INTERPRETER RESULT:")
print(interpreter.run())