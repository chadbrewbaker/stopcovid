from z3 import*
import math
import time

start = time.time()

GROUPS = 4
MIN_GROUP_SIZE = 4
MAX_GROUP_SIZE = 17
BIT_COLORS = True  # Use bitvectors instead of integers to encode classroom assignments
IN_EDGES = False   # Also assume classrooms are cliques to add those edges
TIME_OUT =  100000 # 100 seconds


borders={"Albania": ["Greece", "Kosovo", "Macedonia", "Montenegro"],
"Andorra": ["France", "Spain"],
"Austria": ["CzechRepublic", "Germany", "Hungary", "Italy", "Liechtenstein", "Slovakia", "Slovenia", "Switzerland"],
"Belarus": ["Latvia", "Lithuania", "Poland", "Ukraine"],
"Belgium": ["France", "Germany", "Luxembourg", "Netherlands"],
"BosniaHerzegovina": ["Croatia", "Montenegro", "Serbia"],
"Bulgaria": ["Greece", "Macedonia", "Romania", "Serbia"],
"Croatia": ["BosniaHerzegovina", "Hungary", "Montenegro", "Serbia", "Slovenia"],
"Cyprus": [],
"CzechRepublic": ["Austria", "Germany", "Poland", "Slovakia"],
"Denmark": ["Germany"],
"Estonia": ["Latvia"],
"Finland": ["Norway", "Sweden"],
"France": ["Andorra", "Belgium", "Germany", "Italy", "Luxembourg", "Monaco", "Spain", "Switzerland"],
"Germany": ["Austria", "Belgium", "CzechRepublic", "Denmark", "France", "Luxembourg", "Netherlands", "Poland", "Switzerland"],
"Greece": ["Albania", "Bulgaria", "Macedonia"],
"Hungary": ["Austria", "Croatia", "Romania", "Serbia", "Slovakia", "Slovenia", "Ukraine"],
"Iceland": [],
"Ireland": ["UnitedKingdom"],
"Italy": ["Austria", "France", "SanMarino", "Slovenia", "Switzerland", "VaticanCity"],
"Kosovo": ["Albania", "Macedonia", "Montenegro", "Serbia"],
"Latvia": ["Belarus", "Estonia", "Lithuania"],
"Liechtenstein": ["Austria", "Switzerland"],
"Lithuania": ["Belarus", "Latvia", "Poland"],
"Luxembourg": ["Belgium", "France", "Germany"],
"Macedonia": ["Albania", "Bulgaria", "Greece", "Kosovo", "Serbia"],
"Malta": [],
"Moldova": ["Romania", "Ukraine"],
"Monaco": ["France"],
"Montenegro": ["Albania", "BosniaHerzegovina", "Croatia", "Kosovo", "Serbia"],
"Netherlands": ["Belgium", "Germany"],
"Norway": ["Finland", "Sweden"],
"Poland": ["Belarus", "CzechRepublic", "Germany", "Lithuania", "Slovakia", "Ukraine"],
"Portugal": ["Spain"],
"Romania": ["Bulgaria", "Hungary", "Moldova", "Serbia", "Ukraine"],
"SanMarino": ["Italy"],
"Serbia": ["BosniaHerzegovina", "Bulgaria", "Croatia", "Hungary", "Kosovo", "Macedonia", "Montenegro", "Romania"],
"Slovakia": ["Austria", "CzechRepublic", "Hungary", "Poland", "Ukraine"],
"Slovenia": ["Austria", "Croatia", "Hungary", "Italy"],
"Spain": ["Andorra", "France", "Portugal"],
"Sweden": ["Finland", "Norway"],
"Switzerland": ["Austria", "France", "Germany", "Italy", "Liechtenstein"],
"Ukraine": ["Belarus", "Hungary", "Moldova", "Poland", "Romania", "Slovakia"],
"UnitedKingdom": ["Ireland"],
"VaticanCity": ["Italy"]}

students = list(borders.keys())
PERSONS = len(students)

s = Optimize()

if(BIT_COLORS):
    student_color=[BitVec('student%d_color' % c,2) for c in range(PERSONS)]
else: 
    student_color=[Int('student%d_color' % c) for c in range(PERSONS)]

def student_name_to_idx(s):
    return students.index(s)

if(BIT_COLORS):
    pass
else:
    s.add(student_color[0]==0)

if(BIT_COLORS):
    pass
else:
    for i in range(PERSONS):
        s.add(And(student_color[i]>=0, student_color[i] < GROUPS))


cohort_edges = []
#edges between groups
for i in range(PERSONS):
    for b in borders[students[i]]:
        #For (a,b) and (b,a) only use (a,b)
        if(i < student_name_to_idx(b)):
            cohort_edges.append(If(student_color[i] != student_color[student_name_to_idx(b)],1,0))

def binomial(n,k):
    return int(math.factorial(n) // (math.factorial(k) * math.factorial(n-k)))

bins = []
for i in range(len(students)+1):
    if( i < 2):
        bins.append(0)
        continue
    bins.append(binomial(i,2))

def count_persons_in_group(g):
    return Sum(*[If( (student_color[i]  == g), 1, 0) for i in range(PERSONS)])

inedges = []
if(IN_EDGES):
    #function to count edges between groups
    iv = Function('iv', IntSort(),IntSort())
    for i in range(len(students)+1):
        s.add(iv(i) == bins[i])
        #s.add(f(i) == binomial(i,2))
    for g in range(GROUPS):
        inedges.append(iv(count_persons_in_group(g)))

#max students per classroom
for g in range(GROUPS):
    s.add(count_persons_in_group(g) < MAX_GROUP_SIZE)

#min students per classroom
for g in range(GROUPS):
    s.add(count_persons_in_group(g) > MIN_GROUP_SIZE)

if(IN_EDGES):
    edges = cohort_edges + inedges
else:
    edges = cohort_edges

esum = Int('Edge Sum') 
s.add(esum == Sum(edges))

s.set("timeout", TIME_OUT)
h = s.minimize(Sum(edges))

print(s.check())
m = s.model()
print(m)
groups={}
for i in range(PERSONS):

    g = m[student_color[i]].as_long()
    if g not in groups:
        groups[g]=[]
    groups[g].append(students[i])
for g in groups:
    print( "group%d,persons:" % g, groups[g])
    print(len(groups[g]))

end = time.time()
print(end - start)