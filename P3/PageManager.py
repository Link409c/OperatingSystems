# Project 3
# This project will serve to emulate the functions of Page Management in an Operating System.
# The project showcases two algorithms modeling the FIFO and LRU policies.
# Each of these policies will be available for testing some amount of input data.
# The program will use given data from the user to determine the best policy to handle
# the needs of their system.

import sys
import random

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

    def runjob(self):
        """run each step in order to 'complete' a job."""
        # for the steps of the job,
        # if the needed page is in memory,
        # move to the next step
        # else,
        # if there is not an empty frame,
        # call one of the assignment functions based on the algorithm in use
        # then increment the interrupt counter.
        # else,
        # put the page in the next available frame
        # return the number of interrupts

    def makepages(self):
        """equally distributes job memory into pages."""
        # get the total memory
        # assumption is memory is in bytes
        # divide by 100 to get number of pages needed
        # return an ordered list of numbers
        return pages

    def makesteps(self):
        """creates a semi randomized list of steps to be executed to complete a job."""
        # for each page in the job,
        # get a random number 1 through 3
        # assign that number to the page
        # for the sum of the numbers assigned to the pages,
        # put each page into a list in a random order
        # this is the steps of how to complete the job.
        return steps

class PageTableEntry:
    """
    An object representing a single entry in a Page Management Table.
    Has flags for wether the page is stored in a page frame, if the page
    has been referenced since being loaded into memory, if the page has been
    modified since being loaded into memory, and the frame number the page is
    stored at.
    """
    __slots__ = ['inMemory', 'referenced', 'modified', 'frameNumber']

    def __init__(self):
        self.inMemory = False
        self.referenced = 0
        self.modified = 0
        self.frameNumber = None
    def __init__(self, inMemoryflag, referenceflag, modifiedflag, aframeNumber):
        self.inMemory = inMemoryflag
        self.referenced = referenceflag
        self.modified = modifiedflag
        self.frameNumber = aframeNumber
def makeNewFrames(numframes, jobs = [Job]):
    """
    creates a new list of frames according to the passed parameter,
    and populates the list with as many pages as possible.
    """
    # make list of frames
    frames = [None for _ in range(numframes)]
    # for each job,
    for Job in jobs:
        # if there are empty frames,
        if frames.__contains__(None):
            # for each page in the job,
            for page in Job.pages:
                # assign pages to empty frames
                frames[frames.index(None)] = page
        else:
            break
    # return frames once filled with pages
    return frames


def assignframeFIFO(page):
    """assigns a page of a job to a frame in memory, removing pages using FIFO policy."""

def assignframeLRU(page):
    """assigns a page of a job to a frame in memory, removing pages using LRU policy."""

def runprogram(inputfile):
    print("Welcome to the Page Management Program.")
    # create jobs from file input
    jobs = []
    with open(inputfile, 'r') as file:
        # get each number in sequence
        file.read()
        # these are the jobs' memory requirements
        # for each number, make a new job object

    # get number of page frames (variable user input)
    numframes = input("\nEnter the number of page frames you want to test with.")
    frames = makeNewFrames()
    # list representing page management table for each job
    pmts = [[None] for _ in range(len(jobs))]
    # divide each job into pages
    # assign each page a frame until no more frames available
    # for each job, follow its list of page calls to complete it
    # for each step,
    # check frames to see if that page is loaded
    # if it is, move to next step
    # if not, use the appropriate removal policy to load it into a frame,
    # then increment an interrupt counter.
    # record the amount of interrupts when using FIFO, then LRU.
    # print the results.

if __name__ == "__main__":
    runprogram(sys.argv[1])




