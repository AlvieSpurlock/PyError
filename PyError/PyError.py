import PyConsole as con
from datetime import datetime as dt
from os import path

class PyError:
    def __init__(self, exception, rI = 0):
        self.exception = exception
        self.message = None
        self.msg = None
        self.date_time = dt.now()
        self.i = None
        self.rI = rI
        self.gArgs = []
        self.rArgs = []
        self.file = None
        self.line = None
        self.method = None
        self.extract_traceback(exception)
        self.extract_argumaent_info(exception)
        self.assign_error_code()

    def Parse(msg, *args):
        for arg in args:
            if arg in msg:
                return True
        return False

    def CaptureIndex(self, i):
        self.i = i

    def CaptureRequiredArgs(self, *args):
        self.rArgs = args

    def CaptureGivenArgs(self, *args):
        self.gArgs = args

    def CheckArgs(self, msg):
        
        if self.Parse(msg, "were given", "positional arguments but"):
            extra = len(self.gArgs) - len(self.rArgs)
            incorrect = []
            for i in range( 0, len(self.rArgs) ): 
                if self.gArgs[i] != self.rArgs[i]: 
                    incorrect.append(type(self.gArgs[i]))
            errMSG = f"Too Many Arguments. Extra Functions Count: {extra} == The Argumaents: {incorrect}"
            self.ErrorMessage(errMSG)
            return

        if self.Parse(msg, "missing 1 required positional argument", "missing {n} required positional arguments", "required positional argument"):
            missing = len(self.rArgs) - len(self.gArgs)
            incorrect = []
            for i in range(len(self.rArgs) - missing, len(self.rArgs)):
                if i < len(self.rArgs):
                    incorrect.append(type(self.rArgs[i]))
            errMSG = f"Too Many Arguments. Missing Functions Count: {missing} == The Arguments: {incorrect}"
            self.ErrorMessage(errMSG)
            return

        if self.Parse(msg, "unexpected keyword argument", "got an unexpected keyword argument"):
            incorrect = []
            for i in range(0, len(self.gArgs)): 
                if type(self.gArgs[i]) != type(self.rArgs[i]): 
                    incorrect.append(self.gArgs[i])
            errMSG = f"Incorrect Arguments. The Arguments: {incorrect}"
            self.ErrorMessage(errMSG)
            return



    def CheckIndex(self, msg):
        if self.Parse(msg, "list index out of range", "tuple index out of range"):
            if self.rI > self.i:
                errorIndex = self.rI - self.i
                errMSG = f"Index Out Of Range by {errorIndex}"
                self.ErrorMessage

    def ErrorMessage(self, message):
        trace = self.exception.__traceback__
        while trace.tb_next:
            trace = trace.tb_next
        self.file = trace.tb_frame.f_code.co_filename
        self.line = trace.tb_lineno
        self.method = trace.tb_frame.f_code.co_name
        readableTime = self.date_time.strftime("%B %d, %Y at %I:%M %p")


        filePath = f"\nFile Path of Error: \n{path.realpath(self.file)}\n------"
        method = f"\nMethod In Question: {self.method}"
        line = f"Line In Question{self.line}\n------"
        time = f"\nTime Of Error: {readableTime}"
        con.PrintHeader(message)

        self.msg = f"{filePath}{method}{line}{time}\n\n[======================]\n\n"
        print(self.msg)

        errLog = open("ErrorLog.txt", "w+")
        errLog.write(f"{self.msg}")
        errLog.close()
