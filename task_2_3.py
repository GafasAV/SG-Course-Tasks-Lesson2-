__author__ = 'Andrew Gafiychuk'

import os


def check_file_descriptor(fn):
    """
    Decorator that check file descriptor access
    for class methods
    """

    def wrapper(self, *args, **kwargs):
        try:
            res = fn(self, *args, **kwargs)
        except(OSError, Exception):
            print("File access error: File closed or does not exist !")
            return None
        else:
            return res

    return wrapper


class File(object):
    """
    Class imitated file access, as open() function

    Uses low level os-module functions, work with file descriptors
    Takes 3 params: (filename, mode, encoding)

    Methods:
        - read(n) - read n bytes from file, if n is None - read all file
        - readLine() - read first line from file
        - write(s) - write s-text to file
        - writeLine(s) - takes first line from s and write to file
        - close() - close the file

    Class can uses with Context Manager
    """

    def __init__(self, filename, mode, encoding="utf-8"):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file_rewrite = True
        self.file_pos = 0
        self._init_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.close(self.fd)

        return True

    def __del__(self):
        try:
            os.close(self.fd)
        except OSError:
            return None

    def _init_file(self):
        """
        This protected method check all main params throw correct
        (filename, mode, encoding) - init and set them if correct
        else raise an exception and print error

        Also create and open file descriptor use os.open()
        """
        if not isinstance(self.filename, str):
            raise TypeError("Invalid file name: {0}".format(self.filename))
        if not isinstance(self.mode, str):
            raise TypeError("Invalid mode args: {0} Must be (r,w,a)\
                            ".format(self.mode))
        if not isinstance(self.encoding, str):
            raise TypeError("Invalid encoding: {0}".format(self.encoding))

        modes = set(self.mode)
        if "a" in modes:
            self.file_rewrite = False

        self.fd = os.open(self.filename, (os.O_RDWR | os.O_CREAT))

    @check_file_descriptor
    def read(self, n=None):
        if not n:
            file_size = os.stat(self.filename).st_size
        elif isinstance(n, int):
            file_size = n
        else:
            raise TypeError("File size error. Size must be integer {0}".format(n))

        os.lseek(self.fd, 0, os.SEEK_SET)

        byte_arr = os.read(self.fd, file_size)
        if len(byte_arr) == 0:
            print("File is clear")

        string = byte_arr.decode(encoding=self.encoding)

        return string

    @check_file_descriptor
    def readLine(self):
        text = self.read()
        line = text.split("\n")[self.file_pos]
        self.file_pos += 1

        return line

    @check_file_descriptor
    def write(self, s):
        if not isinstance(s, str):
            s = str(s)

        if self.file_rewrite:
            os.lseek(self.fd, 0, 0)
            self.file_rewrite = False

        byte_arr = s.encode(encoding=self.encoding)
        bw = os.write(self.fd, byte_arr)

        return bw

    @check_file_descriptor
    def writeLine(self, s):
        if not isinstance(s, str):
            s = str(s)

        s = "\n" + s
        bw = self.write(s)

        return bw

    @check_file_descriptor
    def close(self):
        os.close(self.fd)
        return True


if __name__ == "__main__":
    file = "file.txt"
    mode = "rw"

    fw = File(file, mode)
    print("[+]File write opened")

    res = fw.read() # if No text in file (Output that file is clear)
    print(res)

    res = fw.write("Hello World")
    print(res)
    res = fw.write("!!!")
    print(res)
    res = fw.writeLine("New line text added")
    print(res)

    fw.close()
    print("[+]File closed !")

    fr = File(file, mode)
    print("[+]File read opened")

    res = fr.read() # Read all file
    print(res)

    res = fr.readLine() # Read first line
    print(res)

    fr.close()
    print("[+]File closed !")

    # Used context manager
    with File(file, mode) as ofile:
        print(ofile.read(1))
        print(ofile.read())
        print(ofile.readLine())
        print(ofile.readLine())
        print(ofile.readLine())