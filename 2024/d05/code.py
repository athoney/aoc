from collections import defaultdict
import math

def p1(filename="input.txt"):
    before = defaultdict(lambda: [])
    correct_nums = []
    with open(filename) as f:
        for line in f:
            if "|" in line:
                nums = list(map(int,(line.strip().split("|"))))
                before[nums[0]].append(nums[1])
            elif len(line.strip()) != 0:
                nums = list(map(int,(line.strip().split(","))))
                correct = True
                for i in range(len(nums)):
                    infront = nums[:i]
                    if nums[i] in before.keys():
                        for j in infront:
                            if j in before[nums[i]]:
                                correct = False
                                break
                if correct:
                    correct_nums.append(nums)

    print(dict(before))
    print(f"correct: {correct_nums}")

    sum = 0
    for num in correct_nums:
        sum += num[len(num)//2]

    print(f"sum: {sum}")

# p1()

def p2(filename="sm.txt"):
    before = defaultdict(lambda: [])
    check = []
    correct_nums = []
    with open(filename) as f:
        for line in f:
            if "|" in line:
                nums = list(map(int,(line.strip().split("|"))))
                before[nums[0]].append(nums[1])
            elif len(line.strip()) != 0:
                nums = list(map(int,(line.strip().split(","))))
                correct = True
                for i in range(len(nums)):
                    infront = nums[:i]
                    if nums[i] in before.keys():
                        for j in infront:
                            if j in before[nums[i]]:
                                correct = False
                                break
                if not correct:
                    check.append(nums)
                if correct:
                    correct_nums.append(nums)

    #print(dict(before))
    order_f = []
    order_b = []
    for key in before.keys():
        #print(f"key: {key}")
        if order_f == []:
            order_f.append(key)
            order_b.extend(before[key])
            #print(f"order_f: {order_f}")
            #print(f"order_b: {order_b}")
        elif order_f[-1] in before[key]:
            order_f.insert(-1,key)
            order_b = list(set(order_b) | set(before[key]))
            order_b = [o for o in order_b if o not in order_f]
            #print(f"order_f: {order_f}")
            #print(f"order_b: {order_b}")
        elif key in order_b:
            order_f.append(key)
            order_b = list(set(order_b) | set(before[key]))
            order_b = [o for o in order_b if o not in order_f]
            #print(f"order_f: {order_f}")
            #print(f"order_b: {order_b}")
    
    print(f"ordering: {order_f}")
    print(f"b: {order_b}")


    #print(f"ordering: {order_f}")

    print(f"length = {len(correct_nums)+len(check)}")
    sum = 0
    for num in correct_nums:
        sum += num[len(num)//2]

    print(f"sum p1: {sum}")

    sum = 0

    # print(f"nums: {check}")
    for c in check:
        to_sort = list(map(lambda x: (x, order_f.index(x)) if x in order_f else (x,math.inf), c))
        # print(f"c: {to_sort}")
        to_sort.sort(key=lambda x: x[1])
        # print(f"sorted: {to_sort}")
        sum += to_sort[len(to_sort)//2][0]

    print(f"sum p2: {sum}")


# p2()


def p3(filename="sm.txt"):
    before = defaultdict(lambda: [])
    check = []
    correct_nums = []
    with open(filename) as f:
        for line in f:
            if "|" in line:
                nums = list(map(int,(line.strip().split("|"))))
                before[nums[0]].append(nums[1])
            elif len(line.strip()) != 0:
                nums = list(map(int,(line.strip().split(","))))
                correct = True
                for i in range(len(nums)):
                    infront = nums[:i]
                    if nums[i] in before.keys():
                        for j in infront:
                            if j in before[nums[i]]:
                                correct = False
                                break
                if not correct:
                    check.append(nums)
                if correct:
                    correct_nums.append(nums)

    #print(dict(before))
    order_f = []
    order_b = []
    for key in before.keys():
        print(f"key: {key}")
        if order_f == []:
            order_f.append(key)
            order_b.extend(before[key])
            # print(f"order_f: {order_f}")
            # print(f"order_b: {order_b}")
        elif len(set(order_f) & set(before[key])) != 0:
            # print(f"order_f before: {order_f}")
            i = list(set(order_f) & set(before[key]))[0]
            print(f"i: {i}")

            order_f.insert(order_f.index(i),key)
            order_b = list(set(order_b) | set(before[key]))
            order_b = [o for o in order_b if o not in order_f]
            # print(f"order_f: {order_f}")
            # print(f"order_b: {order_b}")
        # problem here
        elif key in order_b:
            order_f.append(key)
            order_b = list(set(order_b) | set(before[key]))
            order_b = [o for o in order_b if o not in order_f]
            # print(f"order_f: {order_f}")
            # print(f"order_b: {order_b}")
    
    print(f"ordering: {order_f}")
    print(f"b: {order_b}")


    #print(f"ordering: {order_f}")

    print(f"length = {len(correct_nums)+len(check)}")
    sum = 0
    for num in correct_nums:
        sum += num[len(num)//2]

    print(f"sum p1: {sum}")

    sum = 0

    # print(f"nums: {check}")
    for c in check:
        to_sort = list(map(lambda x: (x, order_f.index(x)) if x in order_f else (x,math.inf), c))
        print(f"c: {to_sort}")
        to_sort.sort(key=lambda x: x[1])
        print(f"sorted: {to_sort}")
        sum += to_sort[len(to_sort)//2][0]

    print(f"sum p2: {sum}")


p3()