import numpy as np
import threading
import multiprocessing
import time
import operator

s=10 #矩陣size
###-*Numpy處理兩矩陣相乘-*###
def main():
    # Generate random matrix and result matrix
    start_time = time.time()
    matA = np.random.randint(10, size = (s, s))
    matB = np.random.randint(10, size = (s, s)) 
    result = np.matmul(matA, matB)
    

    # Compare with numpy's multiplication result
    end_time = time.time()
    print('Time elapsed 1:\t', end_time - start_time)  
    return matA,matB,result

###-*Treading-*###
def thread_func(start, end, matrix_a, matrix_b, result_2):
    result_2[start:end] = matrix_a[start:end].dot(matrix_b)
def main2():
    # How many thread you want to use
    start_time = time.time()
    thread_num = 10
    up=s//10
    low=0
    threads = []
    thread=[]
    res=[]
    result_2=np.zeros((s,s))
    
    # Assign job to threads
    for i in range(thread_num):
        # Pass argument to function with tuple
        thread = threading.Thread(target = thread_func,args=(low,up,matA,matB,result_2))
        threads.append(thread)
        low=up
        up+=s//10

    # run all threads
    for thread in threads:
        thread.start()

    # Wait for threads finish
    for thread in threads:
        thread.join()
    

    for i in range(s):
        res.append(result_2[i])
    end_time = time.time()
    print('Time elapsed 2:\t', end_time - start_time)
    print('Answer is correct:', np.all(result == res))


##-*Processing-*###
def process_func(low,up, result_dict): 
    for i in range(low,up):
        result_dict[i]= np.matmul(matA[i], matB)
    # print(result_dict)
def main3():
    # print(result)#numpy的結果，用來比對
    start_time = time.time()
    # Generate queue for communication
    result_dict = multiprocessing.Manager().dict()
    re=[]
    processes = 10
    up=s//10
    low=0
    jobs = []
    for i in range(processes):
        process = multiprocessing.Process(target = process_func, args = (low,up,result_dict))
        jobs.append(process)
        low=up
        up+=s//10
        

    for process in jobs:
        process.start()

    for process in jobs:
        process.join()
    
    
    for i in range(s):
        re.append(result_dict[i])  
    end_time = time.time()
    print('Time elapsed 3:\t', end_time - start_time)
    print('Answer is correct:', np.all(result == re))  
     



#main
matA,matB,result=main()
main2()
main3()