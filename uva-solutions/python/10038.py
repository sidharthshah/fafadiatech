#!/usr/bin/python
#Solution to Jolly Jumper 
#URL: http://www.algorithmist.com/index.php/UVa_10038
#Author: Sidharth Shah

def jolly(input):
    """
    Return True is sequence is jolly
    """
    nums = []
    uniq = [] 

    for i in range(len(input)):
        if i != (len(input)-1):
            a , b = input[i],input[i+1]
            result = abs(a-b)
        
            if result not in nums:
                nums.append(result)
    
        if input[i] not in uniq:
            uniq.append(input[i])


    if len(nums) == (len(uniq) - 1):
        return True
    else:
        return False

if __name__ == "__main__":
    file = open("10038-input.txt")
    for eachLine in file:
        eachLine = eachLine.strip()
        input = map(int,eachLine.split(" "))
        if(jolly(input)):
            print "Jolly"
        else:
            print "Not jolly"
