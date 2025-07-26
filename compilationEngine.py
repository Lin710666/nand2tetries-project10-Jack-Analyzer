import tokenizer

class CompilationEngine:
    def __init__(self,input_file):
        self.input_file = input_file
        self.output_file = open(input_file.split('.')[0]+'.xml', 'w')
        self.tokenizer_obj = tokenizer.Tokenizer(input_file)
        self.tokenizer_obj.Constructer()
        self.op = ['+','-','*', '/', '&', '|', '<', '>', '=']   
        self.unaryOp = ['-','~']
        self.keywordConstant = ['true', 'false', 'null', 'this']
        self.deepth = 0
        self.classNames = ['Math','String','Array','Output','Screen','Keyboard','Memory','Sys']
        self.varNames = []
        self.subroutinNames = []


    def printSpace(self):
        return "    "*self.deepth
    
    
    def addToClassNames(self,className):
        if not(className in self.classNames):
            self.classNames.append(className)

    def addToVarNames(self,varName):
        if not(varName in self.varNames):
            self.varNames.append(varName)

    def addToSubroutineNames(self,subroutineName):
        if not(subroutineName in self.subroutinNames):
            self.subroutinNames.append(subroutineName)

    def compileClass(self):
        if self.tokenizer_obj.current_token == "class":
            self.output_file.write('<class>\n')
            self.deepth += 1

            #<keyword> class </keyword>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            #<identifier> className </identifier>
            self.tokenizer_obj.advance()
            self.addToClassNames(self.tokenizer_obj.current_token)
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            #<symbol> { </symbol>
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<classVarDec> classVarDec </classVarDec>
            self.compileClassVarDec()
            self.tokenizer_obj.back()
            #<subroutineDec> subroutineDec </subroutineDec>
            self.compilesubroutineDec()
            #<symbol> } </symbol>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')

            self.output_file.write('</class>\n')
            self.deepth -= 1
        else:
            print("Error: class keyword expected")
            exit()

    def compileClassVarDec(self):
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+'<classVarDec>\n')
        self.deepth += 1
        while (self.tokenizer_obj.current_token == "static" or self.tokenizer_obj.current_token == "field"):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            self.tokenizer_obj.advance()
            
            #<?> type </?>
            if (self.tokenizer_obj.current_token in self.classNames):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
                self.tokenizer_obj.advance()
            elif (self.tokenizer_obj.current_token in ['int','char','boolean']):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
                self.tokenizer_obj.advance()
      
         #<identifier> varName </identifier>
            self.addToVarNames(self.tokenizer_obj.current_token)
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            #<?> (, varName, ) </?>
            self.tokenizer_obj.advance()
            while (self.tokenizer_obj.current_token == ","):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.tokenizer_obj.advance()
                self.addToVarNames(self.tokenizer_obj.current_token)
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
                self.tokenizer_obj.advance()
                
            #<symbol> ; </symbol>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.tokenizer_obj.advance()

            
        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</classVarDec>\n')
                 
    

    def compilesubroutineDec(self):
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+'<subroutineDec>\n')
        self.deepth += 1
        while (self.tokenizer_obj.current_token == "constructor") or (self.tokenizer_obj.current_token == "function") or (self.tokenizer_obj.current_token == "method"):

            #<keyword> constructor | function | method </keyword>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            self.tokenizer_obj.advance()
            #<?> void|type </?>
            #<keyword> void|int|char|boolean </keyword>
            if self.tokenizer_obj.current_token in ["void" , "int" , "char" , "boolean"]:
                self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            #<identifier> className </identifier>
            elif (self.tokenizer_obj.current_token in self.classNames):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            #<identifier> subroutineName </identifier>
            self.tokenizer_obj.advance()
            self.addToSubroutineNames(self.tokenizer_obj.current_token)
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            #<symbol> ( </symbol>
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<parameterList> parameterList </parameterList>
            self.tokenizer_obj.advance()
            if (self.tokenizer_obj.current_token != ")"):
                self.compileParameterList()
                self.tokenizer_obj.advance()
            #<symbol> ) </symbol>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<subroutineBody> subroutineBody </subroutineBody>
            self.compileSubroutineBody()

            self.tokenizer_obj.advance()

        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</subroutineDec>\n')


    def compileParameterList(self):
        self.output_file.write(self.printSpace()+'<parameterList>\n')
        self.deepth += 1

        #<?> type </?>
        #<identifier> className </identifier>
        if (self.tokenizer_obj.current_token in self.classNames):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
        #<keywork> int|char|boolean </keyword>
        elif (self.tokenizer_obj.current_token in ['int','char','boolean']):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        else:
            print("Error: type expected")
            exit()
        #<identifier> varName </identifier>
        self.tokenizer_obj.advance()
        self.addToVarNames(self.tokenizer_obj.current_token)
        self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')

        #<?> (, type varName )* </?>
        self.tokenizer_obj.advance()
        while (self.tokenizer_obj.current_token == ","):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<?> type </?>
            self.tokenizer_obj.advance()
            #<identifier> className </identifier>
            if (self.tokenizer_obj.current_token in self.classNames):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            #<keywork> int|char|boolean </keyword>
            elif (self.tokenizer_obj.current_token in ['int','char','boolean']):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            else:
                print("Error: type expected")
                exit()
            #<identifier> varName </identifier>
            self.tokenizer_obj.advance()
            self.addToVarNames(self.tokenizer_obj.current_token)
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            self.tokenizer_obj.advance()

        self.tokenizer_obj.back()
        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</parameterList>\n')

    def compileSubroutineBody(self):
        self.tokenizer_obj.advance()
        if (self.tokenizer_obj.current_token == "{"):
            self.output_file.write(self.printSpace()+'<subroutineBody>\n')
            self.deepth += 1
            #<symbol> { </symbol>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<varDec> varDec </varDec>
            self.compileVarDec()
            #<statements> statements </statements>
            self.compileStatements()
            #<symbol> } </symbol>
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')

            self.deepth -= 1
            self.output_file.write(self.printSpace()+'</subroutineBody>\n')
        else:
            print("Error: { expected")
            exit()

    def compileVarDec(self):
        self.tokenizer_obj.advance()
        while self.tokenizer_obj.current_token == "var":
            self.output_file.write(self.printSpace()+'<varDec>\n')
            self.deepth += 1
            #<keyword> var </keyword>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            #<?> type </?>
            self.tokenizer_obj.advance()
            if (self.tokenizer_obj.current_token in self.classNames):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            elif (self.tokenizer_obj.current_token in ['int','char','boolean']):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            else:
                print("Error: type expected")
                exit()
            #<identifier> varName </identifier>
            self.tokenizer_obj.advance()
            self.addToVarNames(self.tokenizer_obj.current_token)
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            #<?> (, varName, ) </?>
            self.tokenizer_obj.advance()
            while (self.tokenizer_obj.current_token == ","):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                #<identifier> varName </identifier>
                self.tokenizer_obj.advance()
                self.addToVarNames(self.tokenizer_obj.current_token)
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
                self.tokenizer_obj.advance()

            #<symbol> ; </symbol>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.deepth -= 1
            self.output_file.write(self.printSpace()+'</varDec>\n')
            self.tokenizer_obj.advance()
        else:
            self.tokenizer_obj.back()

    def compileStatements(self):
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+'<statements>\n')
        self.deepth += 1
        while  (self.tokenizer_obj.current_token in ['let','if','while','do','return']):
            if self.tokenizer_obj.current_token == "let":
                self.compileLet()
            elif self.tokenizer_obj.current_token == "if":
                self.compileIf()
            elif self.tokenizer_obj.current_token == "while":
                self.compileWhile()
            elif self.tokenizer_obj.current_token == "do":
                self.compileDo()
            elif self.tokenizer_obj.current_token == "return":
                self.compileReturn()
            else:
                print("Error: let, if, while, do or return keyword expected")
                exit()
            self.tokenizer_obj.advance()
        self.tokenizer_obj.back()
        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</statements>\n')

    def compileLet(self):
        self.output_file.write(self.printSpace()+'<letStatement>\n')
        self.deepth += 1
        #<keyword> let </keyword>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        #<identifier> varName </identifier>
        self.tokenizer_obj.advance()
        self.addToVarNames(self.tokenizer_obj.current_token)
        self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
        #<> [ expression ] </?>
        self.tokenizer_obj.advance()
        if (self.tokenizer_obj.current_token == "["):
            #<symbol> [ </symbol>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<expression> expression </expression>
            self.compileExpression()
            #<symbol> ] </symbol>
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.tokenizer_obj.advance()
        #<symbol> = </symbol>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<expression> expression </expression>
        self.compileExpression()
        #<symbol> ; </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</letStatement>\n')

    def compileIf(self):
        self.output_file.write(self.printSpace()+'<ifStatement>\n')
        self.deepth += 1
        #<keyword> if </keyword>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        #<symbol> ( </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<expression> expression </expression>
        self.compileExpression()
        #<symbol> ) </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<symbol> { </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<statements> statements </statements>
        self.compileStatements()
        #<symbol> } </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<?> else </?>
        self.tokenizer_obj.advance()
        if (self.tokenizer_obj.current_token == "else"):
            #<keyword> else </keyword>
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
            #<symbol> { </symbol>
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            #<statements> statements </statements>
            self.compileStatements()
            #<symbol> } </symbol>
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.tokenizer_obj.advance()
        self.tokenizer_obj.back()
        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</ifStatement>\n')

    def compileWhile(self):
        self.output_file.write(self.printSpace()+'<whileStatement>\n')
        self.deepth += 1
        #<keyword> while </keyword>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        #<symbol> ( </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<expression> expression </expression>
        self.compileExpression()
        #<symbol> ) </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<symbol> { </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #<statements> statements </statements>
        self.compileStatements()
        #<symbol> } </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')

        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</whileStatement>\n')

    def compileDo(self):
        self.output_file.write(self.printSpace()+'<doStatement>\n')
        self.deepth += 1
        #<keyword> do </keyword>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        #<identifier> subroutineCall </identifier>
        self.tokenizer_obj.advance()
        self.compileSubroutineCall()
        #<symbol> ; </symbol>
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')

        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</doStatement>\n')

    def compileReturn(self):
        self.output_file.write(self.printSpace()+'<returnStatement>\n')
        self.deepth += 1
        #<keyword> return </keyword>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        #<?> expression </?>
        self.tokenizer_obj.advance()
        if (self.tokenizer_obj.current_token != ";"):
            self.compileExpression()
        #<symbol> ; </symbol>
        self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')

        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</returnStatement>\n')

    def compileExpression(self):
        self.tokenizer_obj.advance()
        self.output_file.write(self.printSpace()+'<expression>\n')
        self.deepth += 1
        #if current token is a term, then call compileTerm()
        self.compileTerm()
        #while next token is a op, then call compileOp() and compileTerm()
        self.tokenizer_obj.advance()
        while (self.tokenizer_obj.current_token in self.op):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.tokenizer_obj.advance()
            self.compileTerm()
            self.tokenizer_obj.advance()

        self.tokenizer_obj.back()
        self.deepth -= 1
        self.output_file.write(self.printSpace()+' </expression>\n')

    def compileTerm(self):
        self.output_file.write(self.printSpace()+'<term>\n')
        self.deepth += 1
        #when term is a subroutineCall
        self.compileSubroutineCall()
        #when term is a integerConstant
        if self.tokenizer_obj.current_token.isdigit():
            self.output_file.write(self.printSpace()+self.tokenizer_obj.intVal()+'\n')
        #when term is a stringConstant
        elif self.tokenizer_obj.current_token[0] == '"' and self.tokenizer_obj.current_token[-1] == '"':
            self.output_file.write(self.printSpace()+self.tokenizer_obj.stringVal()+'\n')
        #when term is a keywordConstant
        elif self.tokenizer_obj.current_token in self.keywordConstant:
            self.output_file.write(self.printSpace()+self.tokenizer_obj.keyword()+'\n')
        #when term is a varName | varName[expression]
        elif self.tokenizer_obj.current_token in self.varNames:
            self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
            self.tokenizer_obj.advance()
            #when term form is like: varName[expression]
            if (self.tokenizer_obj.current_token == "["):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.compileExpression()
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            else:
                self.tokenizer_obj.back()
        #when term is a (expression)
        if (self.tokenizer_obj.current_token == "("):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.compileExpression()
            self.tokenizer_obj.advance()
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
        #when term is a unaryOp term
        if (self.tokenizer_obj.current_token in self.unaryOp):
            self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
            self.tokenizer_obj.advance()
            self.compileTerm()

        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</term>\n')

    def compileSubroutineCall(self):
        #when sunroutineCall is like: subroutineName(expressionList)
        if (self.tokenizer_obj.tokenType() == "IDENTIFIER"):
            self.tokenizer_obj.advance()
            if (self.tokenizer_obj.current_token == "("):
                self.output_file.write(self.printSpace()+'<subroutineCall>\n')
                self.deepth += 1
                self.tokenizer_obj.back()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.compileExpressionList()
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.deepth -= 1
                self.output_file.write(self.printSpace()+'</subroutineCall>\n')
            else:
                self.tokenizer_obj.back()
        #when sunroutineCall is like: className|varName.subroutineName(expressionList)
        if(self.tokenizer_obj.current_token in self.classNames)or (self.tokenizer_obj.current_token in self.varNames):
            self.tokenizer_obj.advance()
            if (self.tokenizer_obj.current_token == "."):
                self.output_file.write(self.printSpace()+'<subroutineCall>\n')
                self.deepth += 1
                self.tokenizer_obj.back()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.identifier()+'\n')
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.compileExpressionList()
                self.tokenizer_obj.advance()
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.deepth -= 1
                self.output_file.write(self.printSpace()+'</subroutineCall>\n')
            else:
                self.tokenizer_obj.back()



    def compileExpressionList(self):
        self.output_file.write(self.printSpace()+'<expressionList>\n')
        self.deepth += 1
        self.tokenizer_obj.advance()
        if self.tokenizer_obj.current_token != ")":
            self.tokenizer_obj.back()
            self.compileExpression()
            self.tokenizer_obj.advance()
            while (self.tokenizer_obj.current_token == ","):
                self.output_file.write(self.printSpace()+self.tokenizer_obj.symbol()+'\n')
                self.compileExpression()
                self.tokenizer_obj.advance()
        self.tokenizer_obj.back()
        self.deepth -= 1
        self.output_file.write(self.printSpace()+'</expressionList>\n')
        
        
        
        

        









        

        

            
