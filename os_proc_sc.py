import math
import copy
import numpy as np
import matplotlib.pyplot as plt

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def compute_quantum(process_list):
    quantum = 0
    for process in process_list:
        quantum += process[1]
    return quantum / len(process_list) * 80 / 100


def parse_input(process_list):
    process_list_copy = copy.deepcopy(process_list)
    for i in range(len(process_list_copy)):
        process_list_copy[i].append(i+1)
    return sorted(process_list_copy)


def compute_wait_average(result_list):
    sum = 0
    for process in result_list:
        sum += process[0]
    return sum / len(result_list)


def compute_turn_average(result_list):
    sum = 0
    for process in result_list:
        sum += process[1]
    return sum / len(result_list)


def fcfs(process_list):
    print('start FCFS')
    current_time = process_list[0][0]

    process_list_copy = copy.deepcopy(process_list)
    process_list_copy.sort(key=lambda x: x[2])
    result = []
    for i in range(len(process_list)):
        result.append([0, 0])

    times_list = []
    process_order = []

    while len(process_list) is not 0:
        # print('current_time = ' + str(current_time))
        # print('process_list: ' + str(process_list))

        times_list.append(current_time)
        process_order.append(process_list[0][2])

        process_index = process_list[0][2] - 1
        result[process_index][0] = current_time - process_list[0][0]
        result[process_index][1] = result[process_index][0] + process_list_copy[process_index][1]

        current_time += process_list[0][1]
        process_list.pop(0)
        # print('(updated) current_time = ' + str(current_time))
        # print(result)
        # print()
    times_list.append(current_time)
    # print('current_time = ' + str(current_time) + '\n')
    statistics(process_list_copy, times_list, process_order, result, "FCFS")
    print('end FCFS\n\n')
    return result


def sjf(process_list):
    print('start SJF')
    current_time = process_list[0][0]

    process_list_copy = copy.deepcopy(process_list)
    process_list_copy.sort(key=lambda x: x[2])
    result = []
    for i in range(len(process_list)):
        result.append([0, 0])

    times_list = []
    process_order = []

    while len(process_list) is not 0:
        # print('current_time = ' + str(current_time))
        # print('process_list: ' + str(process_list))

        times_list.append(current_time)
        process_order.append(process_list[0][2])

        process_index = process_list[0][2] - 1
        result[process_index][0] = current_time - process_list[0][0]
        result[process_index][1] = result[process_index][0] + process_list_copy[process_index][1]

        current_time += process_list[0][1]
        process_list.pop(0)
        # print('(updated) current_time = ' + str(current_time))

        if len(process_list) > 1:
            temp_min = math.inf
            for process in process_list:
                if process[1] < temp_min and process[0] <= current_time:
                    temp_min = process[1]
                    temp_process = process
            process_list.remove(temp_process)
            process_list.append(temp_process)
            process_list.reverse()
        # print()
    times_list.append(current_time)
    # print('current_time = ' + str(current_time) + '\n')
    statistics(process_list_copy, times_list, process_order, result, "SJF")
    print('end SJF\n\n')
    return result

# def rr(process_list, quantum=-1):
#     print('start RR')
#     if quantum == -1:
#         quantum = math.ceil(compute_quantum(process_list))
#     print('quantum = ' + str(quantum))
#     current_time = process_list[0][0]
#
#     process_list_copy = copy.deepcopy(process_list)
#     process_list_copy.sort(key=lambda x: x[2])
#     result = []
#     for i in range(len(process_list)):
#         result.append([0, 0])
#
#     times_list = []
#     process_order = []
#
#     while len(process_list) is not 0:
#         # print('current_time = ' + str(current_time))
#         # print('process_list: ' + str(process_list))
#
#         times_list.append(current_time)
#         process_order.append(process_list[0][2])
#
#         process_index = process_list[0][2] - 1
#         result[process_index][0] += current_time - process_list[0][0]
#
#         if process_list[0][1] <= quantum:
#             result[process_index][1] = result[process_index][0] + process_list_copy[process_index][1]
#             current_time += process_list[0][1]
#             process_list.pop(0)
#         else:
#             process_list[0][1] -= quantum
#             process_list[0][0] = current_time + quantum
#             temp_process = process_list[0]
#             process_list.remove(temp_process)
#             for i in range(len(process_list)):
#                 if process_list[i][0] > current_time + quantum:
#                     process_list.insert(i, temp_process)
#                     break
#             if temp_process not in process_list:
#                 process_list.append(temp_process)
#             current_time += quantum
#         # print()
#     times_list.append(current_time)
#     # print('current_time = ' + str(current_time) + '\n')
#     statistics(process_list_copy, times_list, process_order, result, "Round Robin")
#     print('end RR\n\n')
#     return result

def rr(process_list, quantum=-1):
    print('start RR')
    if quantum == -1:
        quantum = normal_round(compute_quantum(process_list))
    print('quantum = ' + str(quantum))

    process_list_copy = copy.deepcopy(process_list)
    process_list_copy.sort(key=lambda x: x[2])
    result = []
    for i in range(len(process_list)):
        result.append([0, 0])

    queue = [process_list[0]]
    current_time = queue[0][0]
    times_list = []
    process_order = []

    while len(queue) is not 0:
        process_cont = None
        process_index = queue[0][2] - 1
        times_list.append(current_time)
        process_order.append(queue[0][2])
        result[process_index][0] += current_time - queue[0][0]
        if queue[0][1] <= quantum:
            result[process_index][1] = result[process_index][0] + process_list_copy[process_index][1]
            current_time += queue[0][1]
            if queue[0] in process_list:
                process_list.remove(queue[0])
        else:
            current_time += quantum
            if queue[0] in process_list:
                process_list.remove(queue[0])
            queue[0][0] = current_time
            queue[0][1] -= quantum
            process_cont = queue[0]

        queue.pop(0)
        for process in process_list:
            if process[0] <= current_time and process not in queue:
                queue.append(process)
        if process_cont:
            queue.append(process_cont)
    times_list.append(current_time)
    statistics(process_list_copy, times_list, process_order, result, "Round Robin")
    print('end RR\n\n')
    return result


def srtn(process_list, quantum=-1):
    print('start SRTN')
    if quantum == -1:
        quantum = normal_round(compute_quantum(process_list))
    print('quantum = ' + str(quantum))
    current_time = process_list[0][0]

    process_list_copy = copy.deepcopy(process_list)
    process_list_copy.sort(key=lambda x: x[2])
    result = []
    for i in range(len(process_list)):
        result.append([-1, -1])

    times_list = []
    process_order = []

    while len(process_list) is not 0:
        # print('current_time = ' + str(current_time))
        # print('process_list: ' + str(process_list))

        times_list.append(current_time)
        process_order.append(process_list[0][2])

        process_index = process_list[0][2] - 1
        if result[process_index][0] == -1:
            result[process_index][0] = current_time - process_list[0][0]

        if process_list[0][1] <= quantum:
            result[process_index][1] = result[process_index][0] + process_list_copy[process_index][1]
            current_time += process_list[0][1]
            process_list.pop(0)
            if len(process_list) > 1:
                temp_min = math.inf
                for process in process_list:
                    if process[1] < temp_min and process[0] <= current_time:
                        temp_min = process[1]
                        temp_process = process
                process_list.remove(temp_process)
                process_list.append(temp_process)
                process_list.reverse()
        else:
            current_time += quantum
            process_list[0][1] -= quantum

        # print('(updated) current_time = ' + str(current_time))
        # print()
    times_list.append(current_time)
    # print('current_time = ' + str(current_time) + '\n')
    statistics(process_list_copy, times_list, process_order, result, "SRTN")
    print('end SRTN\n\n')
    return result


def statistics(process_list, times_list, process_order, result, title):
    # print('process_list: ' + str(process_list))
    #[4, 16, 33, 67, 90]
    print('times_list: ' + str(times_list))
    print('process_order: ' + str(process_order))
    print('context_switches: ' + str(len(process_order) - 1))
    print('result: ' + str(result))
    print('wait average = ' + str(compute_wait_average(result)))
    print('turn average = ' + str(compute_turn_average(result)))
    starting_points = np.array(times_list[:-1])
    y_axis_labels = np.array(process_order)
    process_val = []
    for i in range(1, len(times_list)):
        process_val.append(times_list[i]-times_list[i-1])
    print("process_val: " + str(process_val))

    plt.figure()
    plt.title(title)
    plt.ylabel("Processes")
    plt.barh(y_axis_labels, process_val, height=0.5, left=starting_points)
    plt.xticks(times_list)
    plt.show()


def main(process_list):
    fcfs_result = fcfs(parse_input(process_list))
    sjf_result = sjf(parse_input(process_list))
    rr_result = rr(parse_input(process_list))
    srtn_result = srtn(parse_input(process_list))


'''
    [4, 12],
    [30, 5],
    [15, 34],
    [25, 23],
    [10, 17]
    [5, 5], [10, 10], [15, 10], [10, 15], [5, 20], [0, 10], [0, 15]
        [25, 7], [12, 5], [5, 13], [10, 3], [7, 27], [19, 29], [12, 10], [5, 6], [21, 31], [2, 13]

    '''
input_list = [
    [6, 52],
    [1, 13],
    [0, 14],
    [0, 23],
    [0, 37]
]
main(input_list)
