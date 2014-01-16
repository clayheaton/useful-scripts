# multi_process.py
# v.1
# 15 JAN 2014

# Adapted from code found on StackOverflow.com for this question:
# http://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing

import multiprocessing
from multiprocessing import Process
import threading

# ================================================================
# ====================== Baseline Classes ========================
# ================ (edit to fit your use case) ===================
# ================================================================
class ThreadRunner(threading.Thread):
    """ This class represents a single instance of a running thread"""
    def __init__(self, name=""):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print self.name,'\n'

class ProcessRunner:
    """ This class represents a single instance of a running process """
    def runp(self, pid, numThreads):
        mythreads = []
        for tid in range(numThreads):
            name = "Proc-"+str(pid)+"-Thread-"+str(tid)
            th = ThreadRunner(name)
            mythreads.append(th) 
        for i in mythreads:
            i.start()
        for i in mythreads:
            i.join()

class ParallelExtractor:    
    def runInParallel(self, numProcesses, numThreads):
        myprocs = []
        prunner = ProcessRunner()

        for pid in range(numProcesses):
            pr = Process(target=prunner.runp, args=(pid, numThreads)) 
            myprocs.append(pr) 
        for i in myprocs:
            i.start()

        for i in myprocs:
            i.join()

# =====================================================================
# ====================== The Main Program Loop +=======================
# ============== (must exist to allow multiple processes) +============
# =====================================================================

if __name__ == '__main__':    

    # This is where you change the starting parameters

    # This example, if run as-is, will launch 6 processes (different CPU cores)
    # with 4 threads on each process. Your likely limitation is your disk I/O,
    # depending on what you're trying to do.

    # I suggest running tests starting with 1 process and 1 thread, and then
    # scaling up the number of processes (until you max out your CPU cores),
    # and scaling up the number of threads per process after that. The Python
    # GIL (Global Interpreter Lock) possibly will kick into effect for each process 
    # that has more than 1 thread, as those threads compete for resources and
    # Python restricts their activity to prevent race conditions.

    # You can alter this to send different parameters around, etc. For example,
    # if you have 10,000 files that need processing, you can build a list of all
    # of them here, send it to the ParallelExtractor, and from there you can 
    # divide up the list so that each thread has a certain number of files to
    # process. 

    # Don't forget that this script and the __main__ loop also occupy a process
    # exclusive from the number you specify below.

    processes = 6
    threads   = 4

    extractor = ParallelExtractor()
    extractor.runInParallel(numProcesses=processes, numThreads=threads)