import sys
import os
import compilationEngine

def main():
    # Read the input file
    input_ = sys.argv[1]

    #global class_name
    global_class_names = ['Math','String','Array','Output','Screen','Keyboard','Memory','Sys']

    #when input is a file:
    if (os.path.isfile(input_)):
        compilationEngine_obj = compilationEngine.CompilationEngine(input_)
        # get the xml code
        while compilationEngine_obj.tokenizer_obj.hasMoreTokens():
            compilationEngine_obj.compileClass()
    #when input is a directory:
    elif (os.path.isdir(input_)):
        jackFiles = []
        for file in os.listdir(input_):
            if file.endswith('.jack'):
                jackFiles.append(file)
                #initialize global class names
                global_class_names.append(file.split('.')[0])
        # get the xml code
        for jackFile in jackFiles:
            compilationEngine_obj = compilationEngine.CompilationEngine(input_+'/'+jackFile)
            compilationEngine_obj.classNames = global_class_names
            while compilationEngine_obj.tokenizer_obj.hasMoreTokens():
                compilationEngine_obj.compileClass()

if __name__ == '__main__':
    main()


