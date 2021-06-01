import requests
from flask import Flask, render_template, request, jsonify, json
from runcode import runcode
import filecmp

app = Flask(__name__)

default_c_code = """#include <stdio.h>

int main(int argc, char **argv)
{
    printf("Hello C World!!\\n");
    return 0;
}    
"""

default_cpp_code = """#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    cout << "Hello C++ World" << endl;
    return 0;
}
"""

default_py_code = """import sys
import os

if __name__ == "__main__":
    print "Hello Python World!!"
"""
default_java_code = """public class Java {
  public static void main(String[] args){
    System.out.println("This is my first program in java");
  }//End of main
}"""

default_rows = "15"
default_cols = "60"


@app.route("/")
@app.route("/runc", methods=['POST', 'GET'])
def runc():
    if request.method == 'POST':
        code = request.form['code']
        input = request.form['inputUrl']
        run = runcode.RunCCode(code, input)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_c_code
        resrun = 'No result!'
        rescompil = ''

    outputurl = request.form['outputUrl']
    r = requests.get(outputurl)
    result = "false"
    output = r.content.decode("utf-8")
    filename = "./running/output.txt"
    with open(filename, "w") as f:
        f.write(resrun)
    filename = "./running/output1.txt"
    with open(filename, "w") as f:
        f.write(output)

    result = filecmp.cmp("./running/output1.txt", "./running/output.txt")

    return jsonify({"result": result, "compile": rescompil})



@app.route("/runcpp", methods=['POST', 'GET'])
def runcpp():
    if request.method == 'POST':
        code = request.form['code']
        input = request.form['inputUrl']
        run = runcode.RunCppCode(code, input)
        rescompil, resrun = run.run_cpp_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_cpp_code
        resrun = 'No result!'
        rescompil = ''

    outputurl = request.form['outputUrl']
    r = requests.get(outputurl)
    result = "false"
    output = r.content.decode("utf-8")
    filename = "./running/output.txt"
    with open(filename, "w") as f:
        f.write(resrun)
    filename = "./running/output1.txt"
    with open(filename, "w") as f:
        f.write(output)

    result = filecmp.cmp("./running/output1.txt", "./running/output.txt")

    return jsonify({"result": result, "compile": rescompil})


@app.route("/py")
@app.route("/runpy", methods=['POST', 'GET'])
def runpy():
    if request.method == 'POST':
        code = request.form['code']
        input = request.form['inputUrl']
        run = runcode.RunPyCode(code, input)
        rescompil, resrun = run.run_py_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_py_code
        resrun = 'No result!'
        rescompil = "No compilation for Python"

    outputurl = request.form['outputUrl']
    r = requests.get(outputurl)
    result = "false"
    output = r.content.decode("utf-8")
    filename = "./running/output.txt"
    with open(filename, "w") as f:
        f.write(resrun)
    filename = "./running/output1.txt"
    with open(filename, "w") as f:
        f.write(output)

    result = filecmp.cmp("./running/output1.txt", "./running/output.txt")

    return jsonify({"result": result, "compile": rescompil})


@app.route("/java")
@app.route("/runjava", methods=['POST', 'GET'])
def runjava():
    if request.method == 'POST':
        code = request.form['code']
        input = request.form['inputUrl']
        run = runcode.RunJavaCode(code, input, request.form['classname'])
        rescompil, resrun = run.run_java_code()
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_java_code
        resrun = 'No result!'
        rescompil = "No compilation for Python"

    outputurl = request.form['outputUrl']
    r = requests.get(outputurl)
    result = "false"
    output = r.content.decode("utf-8")
    filename = "./running/output.txt"
    with open(filename, "w") as f:
        f.write(resrun)
    filename = "./running/output1.txt"
    with open(filename, "w") as f:
        f.write(output)

    result = filecmp.cmp("./running/output1.txt", "./running/output.txt")

    return jsonify({"result": result, "compile": rescompil})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
