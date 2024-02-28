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
#   memory partitions - each has allotted memory and an assigned job
#   completed jobs - ID, memory needed, order of completion
# the program should adjust memory segments using compaction.
# the program should print the lists to a file?
# the program should print some type of results for the user?
##
# updates:
# remove working jobs list
# in its place, change second variable of partition objects
# this field will hold the job at that partition insteald of assigned flag


import sys
import time

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
        # assign each size to partition and set parition job to None
        for partition in partition_sizes:
            partitions.append([partition, None])
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
        if float(job[1]) > float(system_memory):
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
        partitions_sum += float(partition[0])
    # check sum against total memory
    if partitions_sum < float(system_memory) or partitions_sum > float(system_memory):
        return True
    return False


'''
Function to shift the objects in a list.
'''


def removeAndShiftItems(aList, removeIndex):
    # set the item at aList[removeIndex] to none
    aList[removeIndex] = None
    # starting at the item to the right of that index,
    for item in range(removeIndex + 1, len(aList)):
        # shift each item to the left.
        aList[item - 1] = item
    # delete the last spot in the list.
    del aList[len(aList) - 1]
    # return the updated list
    return aList


'''
Function to emulate memory allocation using first-fit method.
'''


def first_fit(memory_partitions, job_list):
    # for each job in the job list,
    for job in range(len(job_list)):
        job_mem = float(job_list[job][1])
        # compare it to each partition
        for partition_index in range(len(memory_partitions)):
            # if partition memory will fit job and partition is unoccupied,
            if job_mem <= memory_partitions[partition_index][0] and \
                    memory_partitions[partition_index][1] is None:
                # assign that partition to the current job
                memory_partitions[partition_index][1] = job_list[job]
                # remove job from job list
                job_list[job] = None
                # terminate upon successful assignment
                break
    # put remaining jobs on the wait list
    wait_list = []
    for job in job_list:
        if job is not None:
            wait_list.append(job)
    # return the updated lists in order
    return memory_partitions, wait_list


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
Function to emulate memory allocation using worst-fit method.
'''


def worst_fit(memory_partitions, job_list, wait_list):
    # assign jobs based on their worst fit 
    # each job should be assigned to the partition with the largest difference between partition memory and job memory
    return None


'''
Function to get the sum of available memory across all partitions.
'''


def sumavailablemem(memory_partitions):
    available_sum = 0
    # for each partition,
    for partition in memory_partitions:
        # if the partition is assigned a job,
        if partition[1] is not None:
            # get job assigned to this partition
            job = partition[1]
            # get memory needed for that job
            job_mem = float(job[1])
            # add the difference between job memory and partition memory to the total memory available
            available_sum += partition[0] - job_mem
        # else add that partition's total memory to the sum
        else:
            available_sum += partition[0]
    # return the sum
    return available_sum


'''
Function to perform compaction on the memory partitions.
'''


def compact(memory_partitions, available_memory, wait_list):
    # var to track index
    next_partition_index = 0
    # list to hold new partitions
    new_partitions = []
    # for each waiting job,
    for job in range(len(wait_list)):
        # get its required memory
        required_memory = float(wait_list[job][1])
        # if its needs can be accommodated through compaction,
        if required_memory <= available_memory:
            # get the remaining memory from working partitions to cover this job's memory requirement
            new_partition_memory = 0
            # while the needs have not been met,
            while new_partition_memory < required_memory:
                # get job at next partition
                curr_part_job = memory_partitions[next_partition_index][1]
                # get total memory at that partition
                curr_part_memory = float(memory_partitions[next_partition_index][0])
                # if there is an assigned job, calculate available memory
                if curr_part_job is not None:
                    # get job's memory
                    curr_job_memory = float(curr_part_job[1])
                    # get difference
                    memory_to_share = curr_part_memory - curr_job_memory
                else:
                    memory_to_share = memory_partitions[next_partition_index][0]
                # allot this amount to the needed memory
                # add to new partition memory
                new_partition_memory += memory_to_share
                # subtract from current partition memory
                memory_partitions[next_partition_index][0] = curr_part_memory - memory_to_share
                # if current partition would be reduced to zero memory, remove it
                if memory_to_share - curr_part_memory == 0:
                    del memory_partitions[next_partition_index]
                # move to next partition
                next_partition_index += 1
            # once memory requirement is fulfilled, create new partition
            # add to new partition list
            new_partitions.append([new_partition_memory, job])
            # remove job from wait list
            wait_list[job] = None
            # update total available memory
            available_memory -= new_partition_memory
        # otherwise move to the next job, leaving current one on the waitlist until working jobs complete.
    # if any partitions have 0 memory remove them
    memory_partitions = [partition for partition in memory_partitions if partition[0] != 0]
    # remove None values from waitlist
    wait_list = [job for job in wait_list if job is not None]
    # append new partitions to partition list
    for partition in new_partitions:
        memory_partitions.append(partition)
    # return updated lists
    return memory_partitions, wait_list


'''
Function to print the list of results.
'''


def printList(a_list):
    for item in a_list:
        print("{0}: {1}".format(item[0], item[1]))
        # for part in item:
        #     print(part, sep=" ")


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
        # display the partitions
        print("Partitions:")
        printList(partitions)
        # create lists for jobs in progress, waiting jobs, and completed jobs
        wait_list, completed_jobs = [], []
        # variable to simulate time
        program_runtime = 0
        # variable to track completed jobs index
        next_completed_slot = 0
        # add function to choose method type here
        method = "First-Fit"
        # while any of the jobs lists are populated,
        while jobs.__len__() > 0 or wait_list.__len__() > 0:
            # if jobs need assignment, run the fit functions, then compact if necessary
            if jobs.__len__() > 0:
                # initial assignment of scheduled jobs
                print(f"\nInitial Scheduling of jobs using {method}.")
                partitions, wait_list = first_fit(partitions, jobs)
                jobs.clear()
            elif wait_list.__len__() > 0:
                # active assignment of waitlisted jobs
                print(f"\nScheduling waitlisted jobs using {method}.")
                partitions, wait_list = first_fit(partitions, wait_list)
            # display the current runtime
            print(f"\nTime: {program_runtime}\n")
            # print the lists
            print("Scheduled Jobs:\n")
            printList(partitions)
            print("\nWait List:\n")
            printList(wait_list)
            # get total available memory
            available_memory = sumavailablemem(partitions)
            # get next job in wait list
            next_job = wait_list[0]
            # if next waiting job would fit in the available memory,
            if float(next_job[1]) <= available_memory:
                print(f"\nJob ID {next_job[0]} requires compaction. Compacting available memory...")
                # compact the remaining memory
                partitions, wait_list = compact(partitions, available_memory, wait_list)
                # display the new partitions
                print("\nNew Partitions:\n")
                printList(partitions)
            # after assignment or if no jobs needed assignment, complete a job
            # get the next partition with an assigned job
            next_working_partition = 0
            for partition in partitions:
                if partition[1] is not None:
                    break
                next_working_partition += 1
            # complete that job by moving it to the completed list
            completed_jobs[next_completed_slot] = partitions[next_working_partition][1]
            # remove it from the partition
            partitions[next_working_partition][1] = None
            # increment clock
            program_runtime += time.process_time()
            # pause system for review
            input("Press any key to continue...")


if __name__ == "__main__":
    runprogram(sys.argv[1])
