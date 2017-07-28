import copy

def loop(array_input, com_len, head, array_output):
    n= com_len-1;sign=range(head+1,head+com_len)
    if(n>1):
        while(sign[n-1]<=len(array_input)-1):
            core(head,sign, n,array_input,array_output)
            sign=[x + 1 for x in sign] 
    else:
        core(head,sign, n,array_input,array_output)

            
def core(head, sign, n, array_input,array_output):   
    fetch=sign[n-1]
    array_child=[array_input[head]]+array_input[sign[0]:fetch+1]
    while fetch < len(array_input):
        array_child[n]=array_input[fetch]
        array_output.append(copy.deepcopy(array_child))
        fetch+=1   

if __name__ == "__main__":
    array_input=[1,2,3,4,5,6,7,8]; com_len=0; array_output=[]
    if(com_len>1):
        for head in range(0,len(array_input)-com_len+1):
            loop(array_input, com_len, head,array_output) 
    else:
        array_output=array_input
    print array_output