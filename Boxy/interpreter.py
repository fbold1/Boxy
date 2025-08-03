from modules import log,Errors,error
Logger="INTERPRETER"

class Help:
    CLASS_KEY="CK"
    ENTITY_ID="EI"
    ENTITY_MAP="EM"
    ENTITY_DICT="ED"
    VAR_DICT="VD"
    FUNC_DICT="FD"
    POS="P"
    FRAME_COUNT="FC"
    MAX_FRAME_COUNT="MFC"

class Interpreter:
    def __init__(self, ast,max_frame_count:int=10):
        self.entity_dict={} #id+entity
        self.entity_map={} #key+id
        self.func_dict={}
        self.var_dict={}
        self.ast_list = ast
        self.pos=0
        self.max_frame_count=max_frame_count
        self.frame_count=0
        self.entity_id=0

    def helper(self):
        log("LOGGING STATS", Logger)
        log(f"MAX FRAME COUNT: {self.max_frame_count}", Logger)
        log(f"CURRENT FRAME COUNT: {self.frame_count}", Logger)
        log(f"ENTITY ID: {self.entity_id}", Logger)
        log(f"VAR DICT: {self.var_dict}", Logger)
        log(f"FUNC DICT: {self.func_dict}", Logger)
        log(f"ENTITY DICT: {self.entity_dict}", Logger)
        log(f"ENTITY MAP: {self.entity_map}", Logger)
        log(f"POS: {self.pos}", Logger)

    def run(self):
        log("STARTING INTERPRET--AST IS FINE",Logger)
        log(f"MAX FRAME COUNT: {self.max_frame_count}",Logger)
        log(f"CURRENT FRAME COUNT: {self.frame_count}",Logger)
        log(f"ENTITY ID: {self.entity_id}",Logger)
        log(f"VAR DICT: {self.var_dict}",Logger)
        log(f"FUNC DICT: {self.func_dict}",Logger)
        log(f"ENTITY DICT: {self.entity_dict}",Logger)
        log(f"ENTITY MAP: {self.entity_map}",Logger)
        log(f"POS: {self.pos}",Logger)
        while self.pos < len(self.ast_list):
            self.interpret(self.ast_list[self.pos])
            self.pos += 1

        return self.ast_list

    def use_up_entity_id(self):
        self.entity_id+=1
        return self.entity_id

    def find_id(self,keys):
        if keys[0] in self.entity_map:
            id=self.entity_map[keys[0]]
            if id in self.entity_dict:
                for key in keys[1:]:
                    if not key in self.entity_map:
                        return False
                    new_id=self.entity_map[key]
                    if new_id!=id:
                        return False
                return id

    def find_entity(self,keys=None,id=None):
        if keys:
            if keys[0] in self.entity_map:
                id=self.entity_map[keys[0]]
                if id in self.entity_dict:
                    for key in keys[1:]:
                        if not key in self.entity_map:
                            return False
                        new_id=self.entity_map[key]
                        if new_id!=id:
                            return False
                    return self.entity_dict[id]

        elif id:
            if id in self.entity_dict:
                return self.entity_dict[id]

            return False
        return None

    def insert_key_to_entity_map(self,key,entity_id):
        self.entity_map[key]=entity_id
        return entity_id

    def insert_entity_dict(self,key,entity):

        self.entity_dict[self.entity_id]=entity
        return entity

    def insert_entity_map(self,key,entity_id):
        self.entity_map[key]=entity_id
        return entity_id

    def register_entity(self,keys,entity):
        entity_id=self.use_up_entity_id()
        self.insert_entity_dict(entity_id,entity)
        for key in keys:
            self.insert_entity_map(key,entity_id)
        return entity_id

    def set_frame_count(self,op=1):
        self.frame_count+=op
        if self.frame_count>=self.max_frame_count:
            print("\n\n-------Error-------\n\n",end="")
            error(Logger,Errors.HARD_ERROR,f"Maximum frame count exceeded!  FRAME COUNT:{self.frame_count}/{self.max_frame_count}")
            print(f"Maximum frame count exceeded!")
            exit(1)

    def interpret(self,entity):
        print(entity)
        if entity[0]=="ASSIGN":

            type=entity[1][0]
            name=entity[1][1]
            if name in self.var_dict:
                print(f"'{name}' is already defined!")
                log(f"'{name}' is already defined!",Logger)

            assignment=self.interpret(entity[1][2])
            value_type=assignment[0]
            value=assignment[1]
            if type==value_type:
                self.var_dict[name]={"type":type,"value":value}
                print(f"'{name}' is now equal to {value} of type {value_type}!")
                log(f"'{name}' is now equal to {value} of type {value_type}!",Logger)

            else:
                print("\n\n-------Error-------\n\n",end="")
                log("\n\n-------Error-------\n\n",Logger)
                print(f"Could not assign {value} of type {value_type} to variable {name} of type {type}")
                error(Logger ,Errors.WARING ,f"Could not assign {value} of type {value_type} to variable {name} of type {type}")

        elif entity[0]=="REASSIGN":
            name=entity[1][1]
            if name in self.var_dict:
                assignment=self.interpret(entity[1][2])
                value_type=assignment[0]
                type=self.var_dict[name]["type"]
                value=assignment[1]
                if type==value_type:
                    self.var_dict[name]={"type":type,"value":value}
                    print(f"REASSIGNMENT: '{name}' is now equal to {value} of type {value_type}!")
                    log(f"REASSIGNMENT: '{name}' is now equal to {value} of type {value_type}!",Logger)


        elif entity[0]=="VAR":
            name=entity[1]
            if name in self.var_dict:
                print(f"'{name}' is equal to {self.var_dict[name]['value']} of type {self.var_dict[name]['type']}!")
                log(f"'{name}' is equal to {self.var_dict[name]['value']} of type {self.var_dict[name]['type']}!",Logger)
                return (self.var_dict[name]['type'], self.var_dict[name]['value'])
            else:
                print(f"Variable '{name}' is not defined!")
                error(Logger,Errors.WARING,"Variable '{name}' is not defined!")


        elif entity[0]=="BOOL":
            if entity[1]=="TRUE":
                return ("BOOL","TRUE")
            else:
                return ("BOOL","FALSE")
        elif entity[0]=="INT" or entity[0]=="NUMBER":
            return ("INT",entity[1])
        elif entity[0]=="FLOAT":
            return ("FLOAT",entity[1])
        elif entity[0]=="STRING":
            return ("STRING",entity[1])

        elif entity[0]=="CREATE":
            if entity[1][0]=="FUNC":
                name=entity[1][1]
                print(f"DEFINING NEW FUNCTION CALLED {name}")


                params= {}
                for param in entity[1][2]:
                    if param[0]=="ASSIGN":
                        param_name=param[1][1]
                        param_type=param[1][0]
                        param_value=param[1][2]
                        params[param_name]=(param_type,param_value)


                body=[]
                for body_entity in entity[1][3]:
                    body.append(body_entity)
                print(f"DEFINED {name} with params {params}!")
                log(f"DEFINED {name} with params {params} and body {body}!",Logger)
                self.func_dict[name]={"type":"FUNC","params":params,"body":body}

        elif entity[0]=="RUN":
            name=entity[1][0]
            log(f"RUNNING FUNCTION {name}! ",Logger)
            if name in self.func_dict:

                params=[]
                for param in entity[1][1]:
                    params.append(self.interpret(param))
                    defined_params = self.func_dict[name]["params"]
                    print("PARAMS: ",params)
                    if len(params)==len(defined_params):

                        old_var_dict=self.var_dict
                        self.var_dict={}
                        print("DEBUG: PARAMS LENGTH IS FINE!")


                        defined_keys=list(defined_params.keys())
                        for i in range(len(params)):
                            given_param=params[i]
                            defined_param=defined_keys[i]


                            given_type=given_param[0]
                            defined_type,_=defined_params[defined_param]
                            if given_type==defined_type:
                                given_value=given_param[1]
                                self.var_dict[defined_param]={"type":defined_type,"value":given_value}
                                print("DEBUG: PARAMS ARE OF THE SAME TYPE!")
                            else:
                                error(Logger,Errors.WARING,f"PARAMETERS DO NOT MATCH!: {given_param} != {defined_params[defined_param]}")
                                return entity
                        self.set_frame_count(1)
                        log(f"RUNNING FUNCTION {name}! ",Logger)
                        log(f"CURRENT FRAME COUNT:{self.frame_count} OUT OF {self.max_frame_count}",Logger)

                        for body_entity in self.func_dict[name]["body"]:
                            next=self.interpret(body_entity)
                            if next[0]=="ANSWER":
                                print(f"ANSWER IS {next[1]}!")
                                log(f"ANSWER IS {next[1]}!",Logger)
                                log(f"EXITING FUNCTION {name}!",Logger)
                                answer=self.interpret(next[1])
                                if not next[1][0]=="RUN":
                                    self.set_frame_count(-1)
                                self.var_dict = old_var_dict
                                return answer


                        self.var_dict=old_var_dict
                        log(f"RESET VARIABLES TO GLOBAL:{self.var_dict}!",Logger)
                        return entity
            log(f"FUNCTION {name} WASN'T FOUND!", Logger)
        elif entity[0]=="BRANCH":
            value=self.interpret(entity[1])
            print("BRANCH VALUE: ",value)
            log(f"BRANCH VALUE: {value}",Logger)
            body=entity[2]
            for branch_body in body:
                if branch_body[0]=="PATH":
                    path_value=self.interpret(branch_body[1])
                    print("PATH VALUE: ",path_value)
                    log(f"PATH VALUE: {path_value}",Logger)
                    if value==path_value:
                        log(f"BRANCH CHECK SUCCEEDED!",Logger)
                        for path_body in branch_body[2]:
                            log(f"RUNNING BRANCH BODY: {path_body}",Logger)
                            next=self.interpret(path_body)
                            log(f"NEXT ENTITY: {next[0]}",Logger)
                            if next[0]=="ANSWER":
                                log(f"ANSWER IS {next[1]}!",Logger)
                                return next
                        return entity

        elif entity[0]=="REGISTER":

            if entity[1][0]=="ENTITY":

                keys=entity[1][1]
                log(f"KEYS: {keys}",Logger)
                body=entity[1][2]
                self.register_entity(keys,body)
                log(f"REGISTERED ENTITY WITH KEYS: {keys}",Logger)
                return entity

        elif entity[0]=="GET":
            keys=entity[1][0]
            op = entity[1][1]
            entity_id=self.find_id(keys)
            body = self.find_entity(id=entity_id)
            values=entity[1][2]

            if op == "valid":
                log(f"VALIDITY CHECK FOR {keys}",Logger)
                log(f"DEBUG: ALL KEYS: {self.entity_map}",Logger)
                if body:
                    return ("BOOL","TRUE")
                else:
                    return ("BOOL","FALSE")
            elif body:
                if op=="run":
                    log(f"RUNNING ENTITY: {body[0]}",Logger)
                    self.set_frame_count(1)
                    self.interpret(body)
                    return entity
                if op=="change":
                    log(f"STARTING CHANGING {keys}",Logger)
                    self.helper()
                    command=body
                    log(f"COMMAND: {command}",Logger)

                    if command[0]=="ASSIGN":
                        log(f"ASSIGNMENT: {command}, VALUES: {values}",Logger)
                        value=values[0]
                        if value[0]=="ASSIGN":
                            new_type=self.interpret(value[1][0])
                            log(f"TYPE:{value[1][0]}", Logger)
                            new_name=self.interpret(value[1][1])
                            log(f"NAME:{value[1][1]}", Logger)
                            new_value=self.interpret(value[1][2])
                            log(f"VALUE:{new_value}",Logger)

                            old_name=body[1][1]
                            if old_name in self.var_dict:
                                del self.var_dict[old_name]
                                self.var_dict[new_name]={"type":new_type,"value":new_value}
                            body=("ASSIGN",(new_type,new_name,new_value))

                            log(f"{keys} ENTITY CHANGED TO: {new_type} {new_name} = {new_value}",Logger)

                if op=="add":
                    classes=values
                    for new_class in classes:
                        self.insert_key_to_entity_map(new_class,entity_id)
                        log(f"ADDED CLASS: {new_class} TO {keys} ENTITY ",Logger)








                else:
                    error(Logger,Errors.WARING,f"Operation {op} not found!")


            else:
                print(f"Entity {keys} not found!")
                error(Logger,Errors.WARING,f"Entity with {keys} keys wasn't found!")


        elif entity[0]=="ANSWER":
            return entity

        elif entity[0]=="WHILE":
            condition=entity[1][0]
            body=entity[1][1]
            while self.interpret(condition)[1]=="TRUE":
                for while_body in body:
                    next=self.interpret(while_body)
                    if next[0]=="ANSWER":
                        return next
            return entity





        else:
            print(f"Unknown entity: {entity}")
            error(Logger,Errors.WARING,f"Unknown entity/symbol: {entity[0]}")


        return entity