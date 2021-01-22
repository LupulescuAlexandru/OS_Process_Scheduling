from scripts.os_proc_sc import fcfs, sjf, rr, srtn, parse_input

# test1
input_list = [
    [7, 11],
    [7, 53],
    [3, 24],
    [2, 23],
    [8, 27],
]
result_fcfs = [[42, 53], [53, 106], [22, 46], [0, 23], [105, 132]]
result_sjf = [[18, 29], [80, 133], [33, 57], [0, 23], [52, 79]]
result_srtn = [[18, 29], [80, 133], [33, 57], [0, 23], [52, 79]]
result_rr = [[39, 50], [80, 133], [77, 101], [77, 100], [96, 123]]

# queue_fcfs = [[]]

assert fcfs(parse_input(input_list), True)[0] == result_fcfs
assert sjf(parse_input(input_list), True)[0] == result_sjf
assert rr(parse_input(input_list), -1, True)[0] == result_rr
assert srtn(parse_input(input_list), -1, True)[0] == result_srtn

queue_list = []
