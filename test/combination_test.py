
def loop(array_input, com_len, head, array_output):
    n= com_len-1;sign=range(head+1,head+com_len)
    while(sign[n-1]<=len(array_input)-n):
        core(head,sign, n,array_input,array_output)
    sign=[x + 1 for x in sign] 

            
def core(head, sign, n, array_input,array_output):   
    fetch=sign[n-1]
    array_child=[array_input[head]].extend(array_input[sign[0]:fetch]) 
    while fetch < len(array_input):
        i=0
        array_child[n-1]=array_input[fetch]
        array_output.append(array_child)
        fetch+=1
        i+=1     

if __name__ == "__main__":
    array_input=[1,2,3,4,5]; com_len=3; array_output=[]
    for head in range(0,len(array_input)-com_len+2):
        loop(array_input, com_len, head,array_output)
        
    print (array_output)

