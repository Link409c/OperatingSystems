# Project 2
# The Memory Manager
# Christian Simpson
##
# This program emulates the different memory management schemes in Operating Systems which allocate
# system memory to user jobs, programs, and processes.
#
# Pseudocode for the program:
#
# The Program should
# Process a list of jobs and their memory costs from a text file
# create a list of jobs in order of their submission
# allocate memory in different ways
#   Best-Fit
#   First-Fit
# the program should keep several lists:
#   submitted jobs - have a job ID and memory needed
#   memory partitions - each tuple has an ID number, assigned Job ID, and memory allocation
#   working jobs
#   completed jobs - ID, memory needed, order of completion
# the program should adjust memory segments using compaction.
# the program should print the lists to a file?
# the program should print some type of results for the user?

import sys
import math
import re

'''
Function to read a file as input and separate the lines into a data structure.
'''


def readfile(a_file):
    # first line of parameter file is system memory
    # second line is partitions of system memory
    # third line and beyond are jobs
    jobs = []
    with open(a_file, 'r') as file:
        # read all lines of file
        contents = file.readlines()
        # get system memory from index 0
        system_memory = contents[0]
        # get memory partitions from index 1
        partitions = [contents[1].split(',')]
        # loop from index 1 to end of contents for jobs
        for job in contents[2:]:
            # format is name, memory needed
            job_name, job_memory = job.split(',')
            jobs.append([job_name, job_memory])
    # close file once loop terminates
    file.close()
    # return the needed values
    return system_memory, partitions, jobs


'''
Function to check job memory against system memory for errors.
'''


def checkjobmemory(memory, jobs_list):
    error_index = 0
    # for each job in the list,
    for job in jobs_list:
        # if that job's memory exceeds system memory,
        if job[1] > memory:
            # return the index number
            return error_index
        else:
            # else increment index
            error_index += 1
    return -1

'''
Function to check total system memory against sum of partitions for errors.
'''

def checkmemorymismatch(memory, partitions):
    # get the sum of all memory partitions
    partitions_sum = math.fsum(partitions)
    # check sum against total memory
    if partitions_sum < memory or partitions_sum > memory:
        return True
    return False

'''
Function to emulate memory allocation using first-fit method.
'''


def first_fit(memory_partitions, job_list, wait_list):
    # for each job in the job list,
    # compare it to each partition
    # if the memory needed by the job is less than or equal to the current partition,
    # and the current partition does not have an assigned job,
    # assign that partition to the current job
    # remove that job from the job list
    # if end of partitions list is reached without an assignment for current job,
    # put that job in the wait list
    # return the three updated lists in order
    return None


'''
Function to emulate memory allocation using best-fit method.
'''


def best_fit(memory_partitions, job_list, wait_list):
    # for each partition in the partitions list,
    # compare it to each job in the job list
    # assign the job closest to that partition's memory without going over.
    # once all partitions are filled, add the remaining jobs to the wait list
    # return the three updated lists in order
    return None


'''
Function to perform compaction on the memory partitions.
'''


def compact():
    # for each memory partition,
    # if it has been assigned a job,
    # get the difference in its total memory and memory allocated to the job
    # add this difference to a total available memory
    # compare this total to the remaining jobs in the waiting list
    # partition the remaining memory to serve the waiting jobs
    # return an updated list of the memory partitions
    return None


'''
Function to print the list of results.
'''


def printList(a_list):
    return None


'''
Function to run the program.
'''


def runprogram(arg):
    # pass in the file as input
    # parse the file into the given system memory, memory partitions, and a list of jobs
    system_memory, partitions, jobs = readfile(arg)
    # check memory and jobs list for any input error
    error_code = checkjobmemory(system_memory, jobs)
    # if the error code is given,
    if error_code >= 0:
        # print an error message and close the program
        print(f"Job ID {error_code} exceeds given system memory. Refer to instructions for correct input.")
        sys.exit("Input Error: A Job's needed memory exceeds the specified System Memory")
    # check partitions for error
    bad_memory_allocation = checkmemorymismatch(system_memory, partitions)
    if bad_memory_allocation:
        print(f"System Memory of {system_memory} mismatched with partitions totaling {math.fsum(partitions)}")
    # else continue
    else:
        # run both types of memory allocation methods
        # compare steps of each algorithm
        # print steps for user?


if __name__ == "__main__":
    runprogram(sys.argv[1])
