#!/usr/bin/env python3
import os, sys, time, re

pid = os.getpid()               # get and remember pid

args = ['clear']
while not "exit" in args:
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        # print(args) debugging Tool
        if '>' in args:
            #get the file where we would put the output
            newFile = args[args.index('>') + 1]
            args = args[0:args.index('>')] # get everything from left of '>'
            os.close(1)                 # redirect child's stdout
            sys.stdout = open(newFile, "w")
            fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)

        if '<' in args:
            execFile = args[args.index('<') + 1]
            args = args[0:args.index('<')]
            args.append(execFile)
            pass

        if '|' in args:
            leftArg = args[0:args.index('|')]
            rightArg = args[args.index('|')+1:]


            nc = os.fork()
            if nc == 0:  #left argument to be executed
                os.close(1)
                sys.stdout = open('file', 'w')
                fd =  sys.stdout.fileno()
                os.set_inheritable(fd, True)
                for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                    program = "%s/%s" % (dir, leftArg[0])
                    try:
                        os.execve(program, leftArg[1:], os.environ) # try to exec program
                    except FileNotFoundError:             # ...expected
                        pass
                sys.exit(1)


            else:
                os.wait()
                os.close(0)
                sys.stdin = open('file', 'r')
                fd =  sys.stdin.fileno()
                os.set_inheritable(fd, True)
                for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                    program = "%s/%s" % (dir, rightArg[0])
                    try:
                        os.execve(program, rightArg[1:], os.environ) # try to exec program
                    except FileNotFoundError:             # ...expected
                        pass
                sys.exit(1)

            pass

        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        sys.exit(1)

    else:               # parent (forked ok)
        os.wait() # waiting for process to die
    args = input(">$ ").split(" ")
sys.exit(0)