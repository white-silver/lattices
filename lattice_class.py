import itertools

class Elem:
    def __init__(self, name, ub):
        self.name = name
        self.ub = ub

flatten = lambda x: [z for y in x for z in (flatten(y) if hasattr(y, '__iter__') and not isinstance(y, str) else (y,))]

def normalize(x):
    return [i for i in list(set(flatten(x))) if i]

def find_upper(elem):
    if elem.ub == []:
        return ''
    else:
        return normalize([i for i in elem.ub]+[find_upper(i) for i in elem.ub])

def meet(a,b):
    #0-1
    if a == b:
        return a
    #0-2
    if a.ub == []:
        return a
    elif b.ub == []:
        return b
    
    #1
    if a in b.ub:
        return a   
    elif b in a.ub:
        return b 

    #2    
    a_upper = find_upper(a)
    b_upper = find_upper(b)

    a_and_b = list(set(a_upper) & set(b_upper)) 

    MIN = Elem('MIN',[''])

    for x in a_and_b:
        if MIN.name == 'MIN':
            MIN = x
        elif MIN in x.ub:
            MIN = x
    return MIN        
                
if __name__ == "__main__":
    one = Elem('1',[])

    a_bot = Elem('a\'',[one])
    b_bot = Elem('b\'',[one])
    c_bot = Elem('c\'',[one])
    a = Elem('a',[b_bot,c_bot,one])    
    b = Elem('b',[a_bot,c_bot,one])
    c = Elem('c',[a_bot,b_bot,one])

    d_bot = Elem('d\'',[one])
    e_bot = Elem('e\'',[one])
    f_bot = Elem('f\'',[one])
    d = Elem('d',[e_bot,f_bot,one])    
    e = Elem('e',[d_bot,f_bot,one])
    f = Elem('f',[d_bot,e_bot,one])

    zero = Elem('0',[a,b,c,a_bot,b_bot,c_bot, d, e, f, d_bot, e_bot, f_bot, one])

#lattice L = B * M
#Lの要素はタプル(b \in B, m \in M)

    B = [one, zero]
    M = [one, a, b, c, d, e, f, a_bot, b_bot, c_bot, d_bot, e_bot, f_bot, zero]

    L = list(itertools.product(B,M))

    Ideal = [(zero, zero), (one, zero)]

    equiv = []

    for l in L:
        for m in L:
            for i in Ideal:
                l_first = meet(l[0],i[0])
                l_second = meet(l[1],i[1])
                l_OR_i = (l_first,l_second)
            
                m_first = meet(m[0],i[0])
                m_second = meet(m[1],i[1])
                m_OR_i = (m_first,m_second)

                if l_OR_i == m_OR_i:
                    equiv.append((l,m))

    ans = []
    for x in list(set(equiv)):
        if x[0] != x[1]:
            ans.append(x)

    print(len(L))
    print(len(ans))
    for y in ans:
        print((y[0][0].name, y[0][1].name),(y[1][0].name,y[1][1].name))