import subprocess
import sys
import os

import requests


class RunCCode(object):

    def __init__(self, code=None, inputfilelink=None ):
        self.inputfilelink = inputfilelink
        self.code = code
        self.compiler = "gcc"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_c_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename, "-Wall", "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_c_prog(self, cmd="./running/a.out < ./running/input.in"):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_c_code(self, code=None):
        filename = "./running/test.c"
        inputfilename = "./running/input.in"
        r = requests.get(self.inputfilelink)
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        with open(inputfilename, "w") as f:
            f.write(r.text)
        res = self._compile_c_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_c_prog()
            result_run = self.stdout
        return result_compilation, result_run


class RunCppCode(object):

    def __init__(self, code=None, inputfilelink=None):
        self.inputfilelink = inputfilelink
        self.code = code
        self.compiler = "g++"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_cpp_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename,  "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_cpp_prog(self, cmd="./running/a.out < ./running/input.in"):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_cpp_code(self, code=None):
        filename = "./running/test.cpp"
        inputfilename = "./running/input.in"
        r = requests.get(self.inputfilelink)
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        with open(inputfilename, "w") as f:
            f.write(r.text)
        res = self._compile_cpp_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_cpp_prog()
            result_run = self.stdout
        return result_compilation, result_run


class RunPyCode(object):

    def __init__(self, code=None, inputfilelink=None):
        self.inputfilelink = inputfilelink
        self.code = code
        if not os.path.exists('running'):
            os.mkdir('running')

    def _run_py_prog(self, cmd="python3 ./running/a.py <./running/input.in"):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_py_code(self, code=None):
        filename = "./running/a.py"
        inputfilename = "./running/input.in"
        r = requests.get(self.inputfilelink)
        if not code:
            code = self.code
        with open(filename, "w") as f:
            f.write(code)
        with open(inputfilename, "w") as f:
            f.write(r.text)
        self._run_py_prog()
        return self.stderr, self.stdout


class RunJavaCode(object):

    def __init__(self, code=None, inputfilelink=None, classname=None):
        self.classname = classname
        self.inputfilelink = inputfilelink
        self.code = code
        self.compiler = "javac"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_java_code(self, filename):
        cmd = [self.compiler, filename]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_java_prog(self):
        cmd = "java -cp ./running "+self.classname+" <./running/input.in"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout = a.decode("utf-8")
        return result

    def run_java_code(self, code=None):
        filename = "./running/"+self.classname+".java"
        inputfilename = "./running/input.in"
        r = requests.get(self.inputfilelink)
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        with open(inputfilename, "w") as f:
            f.write(r.text)
        res = self._compile_java_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_java_prog()
            result_run = self.stdout
        return result_compilation, result_run
