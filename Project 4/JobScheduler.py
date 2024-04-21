# From Flynn & McHoes 8th ed.
# Pg 139 Exercise 19
# Write a program that will simulate FCFS, SJN, SRT, and round robin
# scheduling algorithms. For each algorithm, the program should compute waiting
# time and turnaround time for every job, as well as the average waiting time
# and average turnaround time. The average values should be consolidated in a
# table for easy comparison. You may use the following data to test your program.
# The time quantum for the round robin is 4 ms. (Assume that the context switching time is 0).


import sys


class Processor:
    """
    Simulates a Processor of the System. The processor can handle one process
    at a time.
    """
    __slots__ = ['name', 'assignedProcess']

    def __init__(self, name = None, assignedProcess = None):
        self.name = str(name)
        self.assignedProcess = assignedProcess


class Job:
    """
    Simulates a job in a system. Has an ID, time arriving in the system, and time
    it takes the CPU to complete the job.
    """
    __slots__ = ['name', 'arrivalTime', 'cpuCycle', 'remainingTime']

    def __init__(self, name = None, arrivalTime = 0, cpuCycle = 0, remainingTime = 0):
        self.name = str(name)
        self.arrivalTime = int(arrivalTime)
        self.cpuCycle = int(cpuCycle)
        self.remainingTime = int(remainingTime)


class JobStatistic:
    """
    Details the Turnaround Time and Waiting Time associated with a job.
    """

    __slots__ = ['name', 'finTime', 'turnaroundTime', 'waitingTime']

    def __init__(self, name = None, finTime = 0, turnaroundTime = 0, waitingTime = 0):
        self.name = str(name)
        self.finTime = int(finTime)
        self.turnaroundTime = int(turnaroundTime)
        self.waitingTime = int(waitingTime)

    def calcTurnaround(self, currentTime, job):
        """
        Calculates the turnaround time of a job.
        """
        self.turnaroundTime = int(currentTime - job.arrivalTime)

    def calcWaitingTime(self, job):
        """
        calculates the waiting time of a job.
        """
        self.waitingTime = int(self.turnaroundTime - job.cpuCycle)


def chooseAlgorithm():
    """
    defines the user choice for a scheduling algorithm to simulate.
    :return: an integer representing the choice
    """
    print("What algorithm would you like to run?")
    print("1. First Come First Serve")
    print("2. Shortest Job Next")
    print("3. Shortest Time Remaining")
    print("4. Round Robin")
    choice = -1
    while choice < 0:
        choice = input("Enter a number choice from the list: ")
        if 0 < int(choice) < 5:
            return int(choice)
        else:
            print("Incorrect input.")
            choice = -1


def runAlgorithm(processors, waitingJobs, currTime, choice = 1):
    """
    runs the chosen scheduling algorithm to replace running jobs.
    :param waitingJobs:
    :param choice:
    :param processors:
    :return: updated processors list and waiting jobs list
    """
    if choice == 1:
        return runFCFS(processors, waitingJobs)
    elif choice == 2:
        return runSJN(processors, waitingJobs)
    elif choice == 3:
        return runSRT(processors, waitingJobs)
    elif choice == 4:
        return runRoundRobin(processors, waitingJobs, currTime)


def runFCFS(processors, waitingQueue):
    # typical run of program assigns processors as jobs finish in FCFS order
    # no changes to lists within algorithm method.
    return processors, waitingQueue


def runSJN(processors, waitingQueue):
    # check all assigned jobs run time against each waiting job run time. if running job has higher run time,
    # replace it with the current waiting job.
    for processor in processors:
        thisProcess = Job(processor.assignedProcess)
        for job in waitingQueue:
            theJob = Job(job)
            if thisProcess.remainingTime > theJob.cpuCycle:
                waitingQueue.append(thisProcess)
                processor.assignedProcess = theJob
                waitingQueue.remove(theJob)
    return processors, waitingQueue


def runSRT(processors, waitingQueue):
    # check all assigned jobs remaining run time against the next waiting job. if running job has higher run time,
    # replace it with the current waiting job.
    for processor in processors:
        # get the process current processor is allocated to
        thisProcess = Job(processor.assignedProcess)
        for job in waitingQueue:
            # compare each waiting job remaining time to that process
            theJob = Job(job)
            # if waiting job has less time remaining,
            if thisProcess.remainingTime > theJob.remainingTime:
                # allocate the processor to it and place deallocated job back in wait queue
                waitingQueue.append(thisProcess)
                processor.assignedProcess = theJob
                waitingQueue.remove(theJob)
    return processors, waitingQueue


def runRoundRobin(processors, waitingQueue, currentTime):
    # for one time cycle, update the processors by assigning the next waiting job to the oldest active processor,
    # and place the job that just released the processor to the end of the waiting queue
    # if current time is a multiple of 4, (time quantum = 4)
    if int(currentTime) % 4 == 0:
        # deallocate the processors and swap in the next two jobs in the waiting queue
        for processor in processors:
            currJob = processor.assignedProcess
            waitingQueue.append(processor.assignedProcess)
            processor.assignedProcess = None
            waitingQueue.remove(currJob)
    return processors, waitingQueue


def createJobs(file):
    """
    uses the values read from a passed file to create a list of jobs.
    :param file: the file passed to the program
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
    while type(processorAmt) is not int:
        processorAmt = int(input("Invalid input format. Input an integer for number of processors: "))
    # create list to hold processors
    processors = []
    # populate processors list with given amount
    for i in range(int(processorAmt)):
        processor = Processor()
        processors.append(processor)
    # return the list
    return processors


def assignFreeProcessor(processors, waitingQueue):
    for job in waitingQueue:
        for processor in processors:
            # add if available
            if processor.assignedProcess is None:
                processor.assignedProcess = job
                # job is removed from waiting queue
                waitingQueue.remove(job)
                break
    return processors, waitingQueue


def printResults(algorithmID, processorCount, results, jobs):
    # get the algorithm used
    if algorithmID == 1:
        algName = "FCFS"
    elif algorithmID == 2:
        algName = "SJN"
    elif algorithmID == 3:
        algName = "SRT"
    else:
        algName = "Round Robin"
    print(f"{algName} Scheduling Statistics for {len(jobs)} Jobs on {processorCount} Processors:")
    avgTurn, avgWait = 0, 0
    # for each result,
    for i in range(len(results)):
        result = results[i]
        avgTurn += result.turnaroundTime
        avgWait += result.waitingTime
        associatedJob = jobs[i]
        # print the job id, its arrival time, turnaround time, and wait time.
        print(f"Job {result.name}\nArrived at {associatedJob.arrivalTime}s\nFinished at {result.finTime}s\n"
              f"Turnaround Time: {result.turnaroundTime}s\nWait Time: {result.waitingTime}s\n--\n")
    # print average turnaround and wait times
    print(f"Average Turnaround Time: {float(avgTurn / len(results))}\n"
          f"Average Wait Time: {float(avgWait / len(results))}")


def runprogram(arg):
    print("Welcome to the Job Scheduling Program.")
    # read the input file arg with createJobs
    jobs = createJobs(arg)
    # sentinel variable for continuing program loop
    run = 1
    while run > 0:
        # create processors
        processors = makeProcessors()
        # queue holds jobs arriving at the system
        waitingQueue = []
        # list holds completed jobs statistics
        runResults = []
        # track time
        time = 0
        # get user input for algorithm
        algorithm = chooseAlgorithm()
        # while there are still jobs to finish,
        while len(runResults) < len(jobs):
            # for each incoming job,
            for job in jobs:
                # if current time corresponds to a job's arrival time,
                if time == job.arrivalTime:
                    # if it is not in the waiting queue,
                    if not waitingQueue.__contains__(job):
                        # add it.
                        waitingQueue.append(job)
            # check for available processor first
            processors, waitingQueue = assignFreeProcessor(processors, waitingQueue)
            # increment time
            time += 1
            # simulate cpu cycle
            for processor in processors:
                thisProcess = Job(processor.assignedProcess)
                if thisProcess.name != 'None':
                    # reduce each process remaining time by 1
                    thisProcess.remainingTime -= 1
                    # then if a process has finished,
                    if thisProcess.remainingTime <= 0:
                        # log the stats and remove it
                        thisJobStats = JobStatistic(thisProcess.name)
                        thisJobStats.calcTurnaround(time, thisProcess)
                        thisJobStats.calcWaitingTime(thisProcess)
                        runResults.append(thisJobStats)
                        processor.assignedProcess = None
            # if waiting jobs remain in queue,
            if len(waitingQueue) > 0:
                # run replacement algorithm
                processors, waitingQueue = runAlgorithm(processors, waitingQueue, time, algorithm)
        # after all jobs have finished print results
        printResults(algorithm, len(processors), runResults, jobs)
        # get input to continue
        run = int(input("Try Again? 0/1: "))
        while int(run) > 1 or int(run) < 0:
            run = input("Invalid Input. Input 0 to end the program, or 1 to run again: ")


if __name__ == "__main__":
    runprogram(sys.argv[1])
