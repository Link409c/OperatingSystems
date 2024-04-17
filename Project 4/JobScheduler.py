# From Flynn & McHoes 8th ed.
# Pg 139 Exercise 19
# Write a program that will simulate FCFS, SJN, SRT, and round robin
# scheduling algorithms. For each algorithm, the program should compute waiting
# time and turnaround time for every job, as well as the average waiting time
# and average turnaround time. The average values should be consolidated in a
# table for easy comparison. You may use the following data to test your program.
# The time quantum for the round robin is 4 ms. (Assume that the context switching time is 0).

class Processor:
    """
    Simulates a Processor of the System. The processor can handle one process
    at a time.
    """
    __slots__ = ['id', 'assignedProcess']

    def __init__(self, id = None, assignedProcess = None):
        self.id = str(id)
        self.assignedProcess = assignedProcess


class Job:
    """
    Simulates a job in a system. Has an ID, time arriving in the system, and time
    it takes the CPU to complete the job.
    """
    __slots__ = ['id', 'arrivalTime', 'cpuCycle', 'remainingTime']

    def __init__(self, id = None, arrivalTime = 0, cpuCycle = 0, remainingTime = 0):
        self.id = str(id)
        self.arrivalTime = int(arrivalTime)
        self.cpuCycle = int(cpuCycle)
        self.remainingTime = int(remainingTime)


class JobStatistic:
    """
    Details the Turnaround Time and Waiting Time associated with a job.
    """

    __slots__ = ['id', 'turnaroundTime', 'waitingTime']

    def __init__(self, id = None, turnaroundTime = 0, waitingTime = 0):
        self.id = str(id)
        self.turnaroundTime = int(turnaroundTime)
        self.waitingTime = int(waitingTime)

    def calcTurnaround(self, currentTime, job = Job):
        """
        Calculates the turnaround time of a job.
        """
        self.turnaroundTime = int(currentTime - job.arrivalTime)

    def calcWaitingTime(self, job = Job):
        """
        calculates the waiting time of a job.
        """
        self.waitingTime = int(self.turnaroundTime - job.cpuCycle)

def chooseAlgorithm():
    """
    defines the user choice for a scheduling algorithm to simulate.
    :return: an integer representing the choice
    """
    choice = -1
    while choice < 0:
        print("What algorithm would you like to run?")
        print("1. First Come First Serve")
        print("2. Shortest Job Next")
        print("3. Shortest Time Remaining")
        print("4. Round Robin")
        choice = input("Enter a number choice from the list: ")
        if choice is int and 0 < int(choice) < 5:
                return choice
        else:
            print("Incorrect input.")
            choice = -1

def runAlgorithm(choice = 1, processors = [Processor], waitingJobs = [Job]):
    """
    runs the chosen scheduling algorithm to replace running jobs.
    :param choice:
    :param processors:
    :param jobs:
    :return: updated processors list and waiting jobs list
    """




def runFCFS(processors = [Processor], jobs = [Job]):

    return None


def runSJN(processors, jobs):

    return None


def runSRT(processors, jobs):
    # queue holds jobs arriving at the system
    # track time
    # jobs arrive at given times
    #
    #
    # when a job finishes, track its completion time
    # do this until no jobs remain
    # calculate turnaround time and average wait time
    # return these values
    return None


def runRoundRobin(processors, jobs):
    return None


def createJobs(file):
    """
    uses the values read from a passed file to create a list of jobs.
    :param arg: the file passed to the program
    :return: a list of Job objects
    """
    print("Creating jobs list.")
    jobs = []
    with open(file, 'r') as thefile:
        contents = thefile.readlines()
        # each line is a job
        for line in contents:
            # split the line at each comma
            jobID, theArrivalTime, theCycle = line.split(',', 3)
            # create a job object using the parameters
            newJob = Job(str(jobID), int(theArrivalTime), int(theCycle), int(theCycle))
            # add it to the list
            jobs.append(newJob)
    # once all lines read, close file
    thefile.close()
    # return the list of jobs
    return jobs

def makeProcessors():
    """
    checks errors and creates the specified number of processor objects to handle jobs.
    """
    # get user defined parameter
    processorAmt = int(input("Input the number of processors to test with: "))
    # check for valid parameter type
    while processorAmt is not int:
        input("Invalid input format. Input an integer for number of processors: ")
    # create list to hold processors
    processors = []
    # populate processors list with given amount
    for i in range(processorAmt):
        processor = Processor()
        processors.append(processor)
    # return the list
    return processors


def runprogram(arg):
    print("Welcome to the Job Scheduling Program.")
    # read the input file arg with createJobs
    jobs = createJobs(arg)
    # create processors
    processors = makeProcessors()
    # queue holds jobs arriving at the system
    waitingQueue = []
    # list holds completed jobs statistics
    # track time
    time = 0
    # get user input for algorithm
    algorithm = chooseAlgorithm()
    # for each incoming job,
    for job in jobs:
        # if current time corresponds to a job's arrival time,
        if time == job.arrivalTime:
            # if it is not in the waiting queue,
            if not waitingQueue.__contains__(job):
                # add it.
                waitingQueue.append(job)
                # then check the processors
                for processor in processors:
                    # if an open processor exists,
                    if processor.assignedProcess is None:
                        # add the job to it,
                        processor.assignedProcess = job
                        # and remove it from waiting.
                        waitingQueue.remove(job)
                    # otherwise,
                    else:
                        # perform chosen algorithm

                    # update running jobs remaining time.
                    processor.assignedProcess.remainingTime = int(processor.assignedProcess.cpuCycle - (time + 1))
    return None