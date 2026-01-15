from email import message
import PyConsole as con
from datetime import datetime as dt
from os import path
import sys
import inspect

class PyErrorMeta:
    def __init__(self):
        self.i = None
        self.rArgs = []
        self.gArgs = []

class PyError:
    active = None
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
        self.extract_argument_info(exception)
        self.assign_error_code()

    def BindMetadeta(self, i, function, *args, **kwargs):
        sig = inspect.signature(function)
        required = [ p.annotation if p.annotation != inspect._empty 
                    else p.name
                    for p in sig.parameters.values() ]
        PyError.active = PyErrorMeta()
        PyError.active.i = i
        PyError.active.rArgs = required
        PyError.active.gArgs = list(args) + list(kwargs.values())

    def extract_traceback(self, exception):
        trace = exception.__traceback__
        while trace.tb_next:
            trace = trace.tb_next

        self.file = trace.tb_frame.f_code.co_filename
        self.line = trace.tb_lineno
        self.method = trace.tb_frame.f_code.co_name

    def extract_argument_info(self, exception):
        try:
            msg = str(exception)
            if PyError.active:
                self.i = PyError.active.i
                self.rArgs = PyError.active.rArgs
                self.gArgs = PyError.active.gArgs
        except Exception:
            pass

    def assign_error_code(self):
        msg = str(self.exception)

        self.CheckArgs(msg)

        self.CheckIndex(msg)

        self.CheckFileIO(msg)

        self.CheckMath(msg)

        self.CheckValue(msg)

    @staticmethod 
    def register_global_hook(): 
        def global_error_hook(exc_type, exc, tb): 
            PyError(exc) 
        sys.excepthook = global_error_hook


    def CaptureIndex(self, i):
        self.i = i

    def CaptureRequiredArgs(self, *args):
        self.rArgs = args

    def CaptureGivenArgs(self, *args):
        self.gArgs = args


    def Parse(self, msg, *args):
        for arg in args:
            if arg in msg:
                return True
        return False

    def ErrorMessage(self, message):
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


    def CheckArgs(self, msg):
        
        if self.Parse(msg,"got multiple values for argument","got an unexpected keyword argument", "were given", "positional arguments but"):
            extra = len(self.gArgs) - len(self.rArgs)
            incorrect = []
            for i in range( 0, len(self.rArgs) ): 
                if self.gArgs[i] != self.rArgs[i]: 
                    incorrect.append(type(self.gArgs[i]))
            errMSG = f"Too Many Arguments. Extra Functions Count: {extra} == The Argumaents: {incorrect}"
            self.ErrorMessage(errMSG)
            return

        if self.Parse(msg,"missing 1 required keyword-only argument","required keyword-only argument", "missing 1 required positional argument", "missing {n} required positional arguments", "required positional argument"):
            missing = len(self.rArgs) - len(self.gArgs)
            incorrect = []
            for i in range(len(self.rArgs) - missing, len(self.rArgs)):
                if i < len(self.rArgs):
                    incorrect.append(type(self.rArgs[i]))
            errMSG = f"Too Many Arguments. Missing Functions Count: {missing} == The Arguments: {incorrect}"
            self.ErrorMessage(errMSG)
            return

        if self.Parse(msg,"not supported between instances of","expected","must be","unsupported operand type(s) for", "unexpected keyword argument", "got an unexpected keyword argument"):
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
                self.ErrorMessage(errMSG)

    def CheckFileIO(self, msg):
        if self.Parse(msg, "No such file or directory"):
            errMSG = f"That is not a File or Directory"
            self.ErrorMessage(errMSG)
        elif self.Parse(msg, "Permission denied"):
            errMSG = f"Permission denied to File or Directory"
            self.ErrorMessage(errMSG)
        elif self.Parse(msg, "Not a directory"):
            errMSG = f"NOT a Directory"
            self.ErrorMessage(errMSG)
        else:
            errMSG = f"Unrecognized File I/O Error"
            self.ErrorMessage(errMSG)

    def CheckMath(self, msg):
        if self.Parse(msg, "division by zero", "integer division or modulo by zero"):
            errMSG = f"Division by Zero"
            self.ErrorMessage(errMSG)


    def CheckValue(self, msg):
        if self.Parse(msg, "has no attribute"):
            errMSG = "No Attribute Exists"
            self.ErrorMessage(errMSG)
            return


        if self.Parse(msg, "KeyError"):
            errMSG = "No Key Exists"
            self.ErrorMessage(errMSG)
            return


        if self.Parse(msg,
                      "invalid literal for int() with base",
                      "not enough values to unpack",
                      "too many values to unpack"):
            errMSG = "Incorrect or Invalid Value"
            self.ErrorMessage(errMSG)
            return


        incorrect = []
        for i in range(min(len(self.gArgs), len(self.rArgs))):
            if type(self.gArgs[i]) != type(self.rArgs[i]):
                incorrect.append(self.gArgs[i])

        if incorrect:
            errMSG = f"Incorrect Values: {incorrect}"
            self.ErrorMessage(errMSG)
            return