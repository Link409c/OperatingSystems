# Project 3
# This project will serve to emulate the functions of Page Management in an Operating System.
# The project showcases two algorithms modeling the FIFO and LRU policies.
# Each of these policies will be available for testing some amount of input data.
# The program will use given data from the user to determine the best policy to handle
# the needs of their system.

import sys
import random


class PageTableEntry:
    """
    An object representing a single entry in a Page Management Table.
    Has flags for wether the page is stored in a page frame, if the page
    has been referenced since being loaded into memory, if the page has been
    modified since being loaded into memory, and the frame number the page is
    stored at.
    """
    __slots__ = ['inMemory', 'referenced', 'modified', 'frameNumber']

    def __init__(self, inMemoryflag = False, referenceflag = 0, modifiedflag = 0, aframeNumber = None):
        self.inMemory = inMemoryflag
        self.referenced = referenceflag
        self.modified = modifiedflag
        self.frameNumber = aframeNumber


class Job:
    """
    An object that simulates a job loaded into a system's memory.
    Has lists containing pages the job has been partitioned into,
    and the necessary page requests needed to complete the job.
    """
    __slots__ = ['memory', 'pages', 'steps']

    def __init__(self, memory):
        """creates the job object, using the passed memory value to create pages and steps to complete."""
        # the total memory needed for the job
        self.memory = memory
        # the pages memory is equally split into
        self.pages = self.makepages()
        # the required steps accessing each page to complete the job
        self.steps = self.makesteps()

    def runjob(self, frames, pmt, policy="FIFO"):
        """run each step in order to 'complete' a job."""
        print(f"Running job {id(self)}")
        interrupts = 0
        # for the steps of the job,
        for step in self.steps:
            # if the step is not in memory,
            if not frames.__contains__(step):
                # if there is not an empty frame,
                if not frames.__contains__(None):
                    # call one of the assignment functions based on the algorithm in use
                    frames, pmt = assignFramePolicy(policy, self, step, frames, pmt)
                    # then increment the interrupt counter.
                    interrupts += 1
                # else,
                else:
                    # put the page in the next available frame
                    nextindex = frames.index(None)
                    frames[nextindex] = step
                    # update the pmt for that page
                    pmt[pmt.index(self)][step] = PageTableEntry(True, 0, 0, nextindex)
            # else, step is already in memory
            else:
                steppte = PageTableEntry(pmt[pmt.index(self)][step])
                # if pte for this step is referenced, set as modified
                if steppte.referenced == 1:
                    steppte.modified = 1
                # set pte for that step as referenced
                else:
                    steppte.referenced = 1
                # update the pmt with the up to date pte
                pmt[pmt.index(self)][step] = steppte
        # return the number of interrupts
        return interrupts

    def makepages(self):
        """equally distributes job memory into pages."""
        # get the total memory
        # assumption is memory is in bytes
        # divide by 100 to get number of pages needed
        numpages = self.memory // 100
        pages = []
        for i in range(numpages):
            pages.append(i)
        # return an ordered list of numbers
        return pages

    def makesteps(self):
        """creates a semi randomized list of steps to be executed to complete a job."""
        # list to hold steps
        steps = []
        # for each page in the job,
        for page in self.pages:
            # get a random number 1 through 3
            numcalls = random.randint(1, 3)
            # add that many instances of the page to the steps list
            for j in range(numcalls):
                steps.append(page)
        # randomize the order of the steps
        random.shuffle(steps)
        # return the list
        return steps


def makePMT(jobs):
    """
    creates the page management tables for each job.
    :param jobs: the list of jobs in the system
    :return: a list of PMTs, one for each job.
    """
    print("Creating Page Management Tables for each job.")
    pmts = []
    # for each job,
    for i in range(len(jobs)):
        # for each of its pages,
        jobpages = jobs[i].pages
        for j in range(len(jobpages)):
            # create a new PTE
            pmts[i][j] = PageTableEntry()
    return pmts


def makeNewFrames(numframes, jobs, pmt):
    """
    creates a new list of frames according to the passed parameter,
    and populates the list with as many pages as possible.
    """
    print("Populating new list of frames.")
    # make list of frames
    frames = [None for _ in range(numframes)]
    # for each job,
    for job in jobs:
        # if there are no empty frames,
        if not frames.__contains__(None):
            # leave the loop
            break
        else:
            for i in range(len(job.pages)):
                # while there are empty frames,
                if frames.__contains__(None):
                    # get next empty frame
                    nextindex = frames.index(None)
                    # assign page to that frame
                    frames[nextindex] = job.pages[i]
                    # update the page entry for that page
                    pmt[pmt.index(job)][i] = PageTableEntry(True, 0, 0, nextindex)
                else:
                    break
    # return frames once filled with pages
    return pmt, frames


def assignFramePolicy(policy, job, stepindex, frames, pmt):
    """
    chooses the appropriate replacement policy and runs it.
    :param policy: the type to use
    :param job: the current job
    :param stepindex: the step the job is on
    :param frames: the list of frames
    :param pmt: the page management table
    :return: the updated frames and pmt after replacement.
    """
    print(f"Step {stepindex} not loaded in memory.")
    if(policy == "FIFO"):
        assignframeFIFO(job, stepindex, frames, pmt)
    elif(policy == "LRU"):
        assignframeLRU(job, stepindex, frames, pmt)
    # add more policies here in the future
    else:
        print("Input a valid policy acronym.")
        sys.exit("Incorrect Policy parameter. Refer to instructions.")
    return frames, pmt


def assignframeFIFO(job, stepindex, frames, pmt):
    """assigns a page of a job to a frame in memory, removing pages using FIFO policy."""
    print("Replacing using First In First Out Policy.")
    # get correct row for current job in PMT list
    jobindex = pmt.index(job)
    for frame in frames:
        # priority 1 is not modified but is referenced.
        currpage = PageTableEntry(pmt[jobindex][stepindex])
        # if the loaded page fits policy 1, remove it
        if currpage.modified == 0 and currpage.referenced == 1:
            # assign page to that frame
            frames[frame] = job.pages[stepindex]
            # update the page entry for that page
            pmt[jobindex][stepindex] = PageTableEntry(True, 0, 0, frame)
            # return the frames and pmt
            return frames, pmt
    for frame in frames:
        # priority 2 is modified and is referenced.
        currpage = PageTableEntry(pmt[jobindex][frame])
        # if the loaded page fits policy 2, remove it
        if currpage.modified == 1 and currpage.referenced == 1:
            # assign page to that frame
            frames[frame] = job.pages[stepindex]
            # update the page entry for that page
            pmt[jobindex][stepindex] = PageTableEntry(True, 0, 0, frame)
            # return the frames and pmt
            return frames, pmt
    return frames, pmt


def assignframeLRU(job, stepindex, frames, pmt):
    print("Replacing using Least Referenced Unit Policy.")
    """assigns a page of a job to a frame in memory, removing pages using LRU policy."""
    # priority 1 is not modified and not referenced.
    # priority 2 is not modified and is referenced.
    # for each frame,
        # if the loaded page fits policy 1, remove it
            # replace it with the required page
            # update its PTE
            # return the frames and pmt
        # else, if the loaded page fits policy 2, remove it
            # replace it with the required page
            # update its PTE
            # return the frames and pmt
    return frames, pmt


def readfile(file):
    """reads the passed file input from args and returns frame numbers and job memory requirements."""
    print("Creating frames and jobs list.")
    jobs = []
    with open(file, 'r') as thefile:
        contents = thefile.readlines()
        # first line is frame amount (2 through 5)
        numframes = contents[0]
        # second line and on is job memory requirements
        for line in contents[1:]:
            newjob = Job(line)
            jobs.append(newjob)
    thefile.close()
    return numframes, jobs


def printresults(policy, numframes, results):
    """
    displays the number of interrupts caused by running each job.
    :param policy: the used replacement policy
    :param numframes: the number of frames
    :param results: the list of jobs and caused interrupts
    """
    print(f"Results using {policy} with {numframes} frames:")
    for jobresult in results:
        print("{0} caused {1} interrupts.", jobresult[0], jobresult[1])


def runprogram(inputfile):
    print("Welcome to the Page Management Program.")
    # create number of frames and jobs list from file input
    numframes, jobs = readfile(inputfile)
    # populate list of page management tables for each job
    pmt = makePMT(jobs)
    # populate frames list
    pmt, frames = makeNewFrames(numframes, jobs, pmt)
    policy = input("Input the acronym for the replacement policy you wish to test: ")
    # list to hold job run results
    results = []
    # for each job, follow its list of page calls to complete it
    for job in jobs:
        interrupts = 0
        interrupts += job.runjob(frames, pmt, policy)
        results.append([id(job), interrupts])
    # print the results.
    printresults(policy, numframes, results)


if __name__ == "__main__":
    runprogram(sys.argv[1])




