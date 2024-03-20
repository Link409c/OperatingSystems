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

def assignframeFIFO(page):
    """assigns a page of a job to a frame in memory, removing pages using FIFO policy."""

def assignframeLRU(page):
    """assigns a page of a job to a frame in memory, removing pages using LRU policy."""




