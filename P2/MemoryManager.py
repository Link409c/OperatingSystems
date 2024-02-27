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
#   memory partitions
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
        # get system memory from index 0 (line 1)
        system_memory = contents[0]
        # get memory partitions sizes from index 1 (line 2)
        partition_sizes = map(float, contents[1].split(','))
        # make list to represent partitions
        partitions = []
        # assign each size to partition and flag occupied status to false
        for partition in partition_sizes:
            partitions.append([partition, False])
        # loop from index 2 to end of contents for jobs (line 3 : end)
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


def checkjobmemory(system_memory, jobs_list):
    error_index = 0
    # for each job in the list,
    for job in jobs_list:
        # if that job's memory exceeds system memory,
        if job[1] > system_memory:
            # return the index number
            return error_index
        else:
            # else increment index
            error_index += 1
    return -1


'''
Function to check total system memory against sum of partitions for errors.
'''

def checkmemorymismatch(system_memory, memory_partitions):
    # get the sum of all memory partitions
    partitions_sum = 0
    for partition in memory_partitions:
        partitions_sum += partition[0]
    # check sum against total memory
    if partitions_sum < system_memory or partitions_sum > system_memory:
        return True
    return False


'''
Function to emulate memory allocation using first-fit method.
'''


def first_fit(memory_partitions, job_list, working_list):
    # for each job in the job list,
    for job in job_list:
        job_mem = job[1]
        # compare it to each partition
        partition_index = 0
        for partition in memory_partitions:
            # if the memory needed by the job is less than or equal to the current partition,
            # and the current partition does not have an assigned job,
            if job_mem <= partition[0] and not partition[1]:
                # assign that partition to the current job
                working_list.append([partition_index, job])
                # flag partition as occupied
                partition[1] = True
                # remove that job from the job list
                job_list.__delitem__(job)
            # increment index
            partition_index += 1
    # put remaining jobs not assigned partitions in the wait list
    wait_list = []
    for job in job_list:
        wait_list.append(job)
    # clear the job list
    job_list.clear()
    # return the updated lists in order
    return memory_partitions, working_list, wait_list


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
Function to get the sum of available memory across all partitions.
'''


def sumavailablemem(memory_partitions, working_jobs):
    available_sum = 0
    jobs_index = 0
    # for each partition,
    for partition in memory_partitions:
        # if the partition is assigned a job,
        if partition[1]:
            # get job assigned to this partition
            assigned_job = working_jobs[jobs_index]
            # get memory needed for that job
            job_mem = assigned_job[1]
            # add the difference between job memory and partition memory to the total memory available
            available_sum += partition[0] - job_mem
        # else add that partition's total memory to the sum
        else:
            available_sum += partition[0]
        # increment partition index
        jobs_index += 1
    # return the sum
    return available_sum


'''
Function to perform compaction on the memory partitions.
'''

# delete partitions with 0 memory remaining which do not have assigned jobs
def compact(memory_partitions, available_memory, working_jobs, wait_list):
    # var to track index
    next_partition_index = 0
    # list to hold new partitions
    new_partitions = []
    # for each waiting job,
    for job in wait_list:
        # get its required memory
        required_memory = job[1]
        # if its needs can be accommodated through compaction,
        if required_memory <= available_memory:
            # get the remaining memory from working partitions to cover this job's memory requirement
            new_partition_memory = 0
            # while the needs have not been met,
            while new_partition_memory < required_memory:
                # get memory of job at next partition
                assigned_job_memory = working_jobs[next_partition_index][1]
                # get total memory at that partition
                memory = memory_partitions[next_partition_index][0]
                # get difference
                memory_to_share = memory - assigned_job_memory
                # if all remaining memory at current partition is used, or the partition has a job assigned,
                # move to next partition
                if memory_to_share == 0:  # or memory_partitions[next_partition_index][1]:
                    continue
                # else allot this amount to the needed memory
                else:
                    # add to new partition memory
                    new_partition_memory += memory_to_share
                    # subtract from current partition memory
                    memory_partitions[next_partition_index][0] = memory - memory_to_share
                # move to next partition
                next_partition_index += 1
            # once memory requirement is fulfilled, create new partition
            # add to new partition list
            new_partitions.append([new_partition_memory, True])
            # remove job from wait list
            wait_list.remove(job)
            # add job to working list
            working_jobs.append(job)
            # update total available memory
            available_memory -= new_partition_memory
        # otherwise move to the next job, leaving current one on the waitlist until working jobs complete.
        # if any partitions have 0 memory remove them
        # append new partitions to partition list
    for partition in new_partitions:
        memory_partitions.append(partition)
    # return updated lists
    return memory_partitions, working_jobs, wait_list


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
    # if back memory check returns true,
    if bad_memory_allocation:
        # print error and exit
        sys.exit("System Memory and sum of partition sizes are not equal. Refer to instructions and check your math!")
    # else continue
    else:
        # create lists for jobs in progress, waiting jobs, and completed jobs
        working_list, wait_list, completed_jobs = [], [], []
        # variable to simulate time
        time = 0
        # variable to track completed jobs index
        next_completed_slot = 0
        # while any of the jobs lists are populated,
        while jobs.__len__() > 0 or wait_list.__len__() > 0 or working_list.__len__() > 0:
            # if jobs need assignment, run the fit functions, then compact if necessary
            if jobs.__len__() > 0:
                # initial assignment of scheduled jobs
                partitions, working_list, wait_list = first_fit(partitions, jobs, working_list)
                jobs.clear()
            elif wait_list.__len__() > 0:
                # active assignment of waitlisted jobs
                partitions, working_list, wait_list = first_fit(partitions, wait_list, working_list)
            # get total available memory
            available_memory = sumavailablemem(partitions, working_list)
            # get next job in wait list
            next_job = wait_list[0]
            # if next waiting job would fit in the available memory,
            if next_job[1] <= available_memory:
                # compact the remaining memory
                partitions, working_list, wait_list = compact(partitions, available_memory, working_list, wait_list)
            # after assignment or if no jobs needed assignment, complete a job
            # get the next partition with an assigned job
            next_working_partition = 0
            for partition in partitions:
                if partition[1]:
                    break
                next_working_partition += 1
            # complete that job by moving it to the completed list
            completed_jobs[next_completed_slot] = working_list[next_working_partition]
            # remove it from the working list
            working_list[next_working_partition] = None
            # set the partition assignment flag to false
            partitions[next_working_partition][1] = False
            # increment clock
            time += 1
        # compare steps of each algorithm
        # print steps for user?


if __name__ == "__main__":
    runprogram(sys.argv[1])
