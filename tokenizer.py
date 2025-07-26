import tokenTable

class Tokenizer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.jack_code = []
        self.current_token = ''
        self.tokens = []
        self.tokenPointer = 0

    def isNotComment(self, line):
        if (line[0:2] == '//')or ('/**' in line) or (line [0] == '*') or ( '*/' in line):
            return False
        else:
            return True
        
    def includeComment(self, line):
        if ('//' in line)or ('/*' in line):
            return True
        else:
            return False
        
    def isNotEmpty(self, line):
        if line == '':
            return False
        else:
            return True       

#打开jack文件，准备进行tokenize       
    def Constructer(self):
        input_file = open(self.input_file, 'r')
        for line in input_file:
            line = line.strip()
            if self.isNotEmpty(line):
                if self.isNotComment(line):
                    if self.includeComment(line):
                        line = line.split('//')[0]
                        self.jack_code.append(line)
                    else:
                        self.jack_code.append(line)
        input_file.close()
        self.getTokens()
        self.current_token = self.tokens[self.tokenPointer]
        return self

    def addToken(self, token):
        if not(token == ''):
            self.tokens.append(token)
    def getTokens(self):
        token = ''
        for line in self.jack_code:
            quoteCount = 0
            for letter in line:
                #若letter是symbol，直接加入tokens
                if letter in tokenTable.Tokens['symbol']:
                    self.addToken(token)
                    token = ''
                    self.tokens.append(letter)
                #若letter是双引号
                elif letter == '"':
                    quoteCount += 1
                    if quoteCount % 2 == 0:
                        token += letter
                        self.addToken(token)
                        token = ''
                    else:
                        token += letter
                #若letter是空格
                elif letter == ' ':
                    if quoteCount % 2 == 0:
                        self.addToken(token)
                        token = ''
                    else:
                        token += letter
                else:
                    token += letter
                
                        
#判断后面是否还有token   
    def hasMoreTokens(self):
        if self.tokenPointer < len(self.tokens)-1:
            return True
        else:
            return False
        
#获取下一个token    
    def advance(self):
        if self.hasMoreTokens():
            self.tokenPointer += 1
            self.current_token = self.tokens[self.tokenPointer]
            
#获取上一个token    
    def back(self):
        if self.tokenPointer > 0:
            self.tokenPointer -= 1
            self.current_token = self.tokens[self.tokenPointer]

    def tokenType(self):
        if self.current_token in tokenTable.Tokens['keyword']:
            return 'KEYWORD'
        elif self.current_token in tokenTable.Tokens['symbol']:
            return 'SYMBOL'
        elif self.current_token.isdigit():
            return 'INT_CONST'
        elif self.current_token[0] == '"' and self.current_token[-1] == '"':
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'
        
    def keyword(self):
        if self.tokenType() == 'KEYWORD':
            return '<keyword> '+self.current_token+' </keyword>'
        
    def symbol(self):
        if self.tokenType() == 'SYMBOL':
            return '<symbol> '+self.current_token+' </symbol>'
        
    def identifier(self):
        if self.tokenType() == 'IDENTIFIER':
            return '<identifier> '+self.current_token+' </identifier>'
        
    def intVal(self):
        if self.tokenType() == 'INT_CONST':
            return '<integerConstant> '+self.current_token+' </integerConstant>'
        
    def stringVal(self):
        if self.tokenType() == 'STRING_CONST':
            return '<StringConstant> '+self.current_token.replace('"','')+' </StringConstant>'
        



 
                    
                    
                    
                    



    
