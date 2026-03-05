# Coursework 1 Solution
## Question 1
### Q1.1
- MQ1\
    Formalise:\
    $R$ = number of pet rabbits;\
    $C$ = number of pet cats;\
    $D$ = number of pet dogs;\
    total = total number of pets = $R + C + D$;\
    lemma R_to_C_and_D: $R = C + D - 12$;\
    lemma C_ratio_D: $C = 2D$;\
    let $D = 60$;\
    by lemma C_ratio_D, $C = 60*2 = 120$;\
    by lemma R_to_C_and_D, $R = 120 + 60 - 12 = 168$;\
    total = $R + C + D = 60 + 120 + 168 = 348$;\
    Conclusion: the total number of pets in the neighbourhood is 448.
- MQ2\
    Formalise:\
    D = Defective;\
    N = Normal;\
    Total D = $3$;\
    D | Y = $2$;\
    $P(Y | D) = 2/3$\
    Conclusion: choose d.
### Q1.2
- MQ1 
    - Identification and Definition\
        Variables: $r$ (number of pet rabbits), $c$ (number of pet cats), $t$ \
        Constants: $D$ (number of pet dogs, 60), $\delta$ (difference, 12), $k$ (cat-per-dog ratio, 2)
    - Structural Logic Translation\
        $r = c + D - \delta$
        $c = k \cdot D$
        $t = c + r + D$\
        $r \geq 0, c \geq 0, t \geq 0$

    - Explicit Factual Representation\
        $D = 60$
        $\delta = 12$
        $k = 2$
    - Question Formalisation\
        In this question, we are tasked with finding $t$, the total number of pets in the neighbourhood:\
        Find $t : (r = c + D - 12) \land (c = 2D) \land (t = c + r + D)$
- MQ2
    - Identification and Definition\
        Variables: $p$ (the required probability) \
        Constants: $N_X$ (chips from company X, 5), $D_X$ (defective chips from company X, 1), $N_Y$ (chips from company Y, 4), $D_Y$ (defective chips from company Y, 2), $N$ (total chips, 9)
    - Structural Logic Translation\
        $p = P(Y|D)$\
        $P(Y|D) = \frac{P(Y \cap D)}{P(D)}$\
        $P(Y \cap D) = \frac{D_Y}{N}$\
        $P(D) = \frac{D_X + D_Y}{N}$
    - Explicit Factual Representation\
        $N_X = 5, D_X = 1$\
        $N_Y = 4, D_Y = 2$\
        $N = 9$
    - Question Formalisation\
        Determine which stated probability of a chosen defective chip came from Company Y.
### Q1.3
- MQ1\
    The total number of pets in the neighbourhood is $348$.
- MQ2\
    Statement d is true.
### Q1.4
Mechanically, in these two questions, the structure is clear that all formulas have no embedded figures. It can help to solve more complex problems that have more variables and constants more easily. It turned each sentence into an equation made the solution a straightforward “substitute and compute” procedure. However, a misinterpretation of the question can end up with a wrong answer or a dead end. 
### Q1.5
**This question I am not quite sure, it seems to me in practical that how the intermediate steps are produced is more important**\
In MQ2, the probability can be calculated from two different way: 1 is to use the Bayes rule like stated in Q1.2; 2 is to use a simple counting approach to calculae: $P(D|Y) = \frac{D_Y}{D_Y + D_X}$. The complexity of these two approaches differences allot.  
## Question 2
### Q2.1
### Q2.2
### Q2.3
## Question 3
### Q3.1
### Q3.2
### Q3.3
### Q3.4
### Q3.5
## Question 4
### Q4.1
### Q4.2
### Q4.3
## Question 5
### Q5.1
### Q5.2