# Project 3
# This project will serve to emulate the functions of Page Management in an Operating System.
# The project showcases two algorithms modeling the FIFO and LRU policies.
# Each of these policies will be available for testing some amount of input data.
# The program will use given data from the user to determine the best policy to handle
# the needs of their system.

# sample run of program:
#
# get the list of jobs as input
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


class Job:
    """
    An object that simulates a job loaded into a system's memory.
    Has lists containing pages the job has been partitioned into,
    and the necessary page requests needed to complete the job.
    """
    __slots__ = ['pages', 'steps']

    def __init__(self, pages, steps):
        self.pages = pages
        self.steps = steps

    def runJob(job):
        """run each step in order to 'complete' a job."""

    def randomizePageOrder(job):
        """creates a semi randomized list of steps to be executed to complete a job."""
        # for each page in the job,
        # get a random number 1 through 3
        # assign that number to the page
        # for the sum of the numbers assigned to the pages,
        # put each page into a list in a random order
        # this is the steps of how to complete the job.
        return steps

def assignFrameFIFO(job):
    """assigns a page of a job to a frame in memory, removing pages using FIFO policy."""

def assignFrameLRU(job):
    """assigns a page of a job to a frame in memory, removing pages using LRU policy."""



