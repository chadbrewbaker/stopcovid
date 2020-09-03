# stopcovid
There is controversy in Iowa and elsewhere on how to effectively keep classrooms as in person as possible. I decided to model the problem in z3py. The model is simple, it minimizes outside contact edges between students in different classrooms. 

I hosted it [here](https://www.github.com/chadbrewbaker/stopcovid). Feedback is welcome.

For simplicity (dataset from Yurichev's book) I used a school of international students, one from every country in Europe. Where borders touch it is assumes students might be exposed to each other. See [Network theory and SARS: predicting outbreak diversity](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7094100/) if you want to generate your own social networks.

I also wrote a second model that assumes classrooms are a clique and minimizes total edges. It uses the [formula](https://en.wikipedia.org/wiki/Triangular_number) for edges within a clique of a given size instead of counting them.

There was a 3x speedup by using fixed length BitVec() values instead of constrained size Int() values to encode the four classroom assignments.

```python
if(BIT_COLORS):
    student_color=[BitVec('student%d_color' % c,2) for c in range(students_total)]
else: 
    student_color=[Int('student%d_color' % c) for c in range(students_total)]
    for i in range(PERSONS):
        s.add(And(student_color[i]>=0, student_color[i] < GROUPS))
```

If you want to learn more about encoding NP hard problems in z3py see the [Z3 hamiltonian example](https://github.com/Z3Prover/z3/blob/master/examples/python/hamiltonian/hamiltonian.py),   [Z3 Playground](https://github.com/0vercl0k/z3-playground), and [SAT SMT by Example](https://yurichev.com/SAT_SMT.html).