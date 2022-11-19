import fileinput


class Error_login:
    def __init__(self, count: int, interval: int, start_lock_time: int, max_lock_time: int, start_time: int):
        self.max_trying = count
        self.count_of_trying = 0
        self.interval = interval
        # self.start_lock_time = start_lock_time
        # self.max_lock_time = max_lock_time
        self.start_time = start_time
        self.next_time_lock = start_lock_time

        self.first_error_time = 0
        self.last_error_time = 0

    def check_of_trying(self, time: int):
        self.first_error_time = min(self.first_error_time,time) if self.first_error_time!=0 \
            else time

        print(time - self.first_error_time,self.count_of_trying+1,self.next_time_lock)
        if time - self.first_error_time < self.interval:
            self.count_of_trying += 1
            if self.count_of_trying == self.max_trying:
                # lock him
                self.next_time_lock *= 2
                self.count_of_trying = 0
            else:
                self.last_error_time = max(self.last_error_time, time) if self.last_error_time != 0 \
                    else time

        else:
            self.count_of_trying = 1
            self.first_error_time= time

def main():
    info: list = input().split()
    error = Error_login(int(info[0]), int(info[1]), int(info[2]), int(info[3]), int(info[4]))
    for line in fileinput.input():
        error.check_of_trying(int(line))
    print(error.next_time_lock/2,error.last_error_time)
    print(error.next_time_lock/2+error.last_error_time)
    # print(1659990835-)

if __name__ == '__main__':
    # main()
    print(1659990835-1659976435)
    # array = []
    # diff = []
    # for line in fileinput.input():
    #     array.append(int(line))
    # for i in range(len(array)-1):
    #     diff.append(array[i+1]-array[i])
    #
    # print(*diff)