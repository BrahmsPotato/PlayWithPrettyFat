from copy import deepcopy

class Combinations(object):
    def __init__(self):
        self.result_list = []

    def combinations(self, l, r):

        if (len(l) < r):
            return self.result_list

        items = [l[0]]
        del l[0]
        self.find_comb(items, l, r)
        self.combinations(l, r)

    def find_comb(self, items, l, r):
        if (len(items) >= r):
            self.result_list.append(tuple(items))
            return

        for i,v in enumerate(l):
             temp_items = deepcopy(items)
             temp_items.append(v)
             temp_l = l[i+1:]
             self.find_comb(temp_items, temp_l, r)

if __name__ =='__main__':
    a = [1,2,2,4,5]
    comb = Combinations()
    comb.combinations(a,r=3)
    print(comb.result_list)
