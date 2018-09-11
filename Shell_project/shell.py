#! /usr/bin/env python3
import os, sys, time, re

pid = os.getpid()               # get and remember pid
rc = os.fork()


if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                 (os.getpid(), pid)).encode())

    args = input("Command to execute: ").split(" ")
    print(args)
    if '>' in args:
        #get the file where we would put the output
        newFile = args[args.index('>') + 1]
        args = args[0:args.index('>')] # get everything from left of '>'
        os.close(1)                 # redirect child's stdout
        sys.stdout = open(newFile, "w")
        fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

    if '<' in args:
        execFile = args[args.index('<') + 1]
        args = args[0:args.index('<')]
        args.append(execFile)
        pass

    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

    sys.exit(1)

else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                 (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                 childPidCode).encode())
