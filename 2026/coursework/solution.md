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
involved are not stated explicitly. Important relationships and quantities are embedded in natural language, which makes it easy to overlook key pieces of information or misinterpret how elements of the problem relate to one another. As a result, a solver may quickly jump to an incorrect interpretation and arrive at a wrong answer even when the underlying mathematics is simple.

The structured reasoning steps used in the formalisation process helped reduce this issue. By first identifying and extracting the relevant entities and facts from the question, the process forces the solver to isolate the important information and remove unnecessary wording or contextual clutter. Translating the problem into a more explicit and structured mathematical representation then makes the relationships between variables clearer and allows the problem to be approached more mechanically. Once the relationships are written formally, deriving the final answer becomes a more straightforward step of applying logical or mathematical operations rather than interpreting language.

Another advantage of this approach is that it reduces the risk of falling for misleading wording. Word problems sometimes include phrasing that encourages an intuitive but incorrect interpretation. Breaking the question down into explicit components helps prevent this by ensuring that each piece of information is carefully analysed before it is used in the reasoning process.

However, the structured approach also has limitations. The formalisation process can be time-consuming, especially for relatively simple problems where an experienced solver might arrive at the correct answer more quickly through intuition. Additionally, if the initial identification or representation of facts is incorrect, the structured process may simply formalise the mistake rather than correct it. In this sense, the approach improves clarity but does not guarantee correctness.

Overall, the structured reasoning steps helped make the reasoning process more systematic and less dependent on intuition. While the approach may add extra steps and time to the process, it provides a clearer framework for understanding the problem and reduces the likelihood of misinterpreting the information given.
### Q1.5
**This question I am not quite sure, it seems to me in practical that how the intermediate steps are produced is more important**\
In MQ2, the probability can be calculated from two different way: 1 is to use the Bayes rule like stated in Q1.2; 2 is to use a simple counting approach to calculae: $P(D|Y) = \frac{D_Y}{D_Y + D_X}$. The complexity of these two approaches differences allot.  
## Question 2
### Q2.1
### Q2.2
### Q2.3
## Question 3
### Q3.1
In line 72 of file main.py /finetuning, the line is to use the function Datasets.train_test_split () to split the training set and the testing set. The argument test_size was set to 0.9, which means that 90% of the dataset will be used for testing and only 10% will be used for training. This will cause the models in the experiment to underperform due to a small sample size and a large amount of unseen data in the testing set.

### Q3.2
| Run |  Qwen2.5-0.5B (Base) | Qwen2.5-0.5B-Instruct |
| --- | -------------------- | ---------------------|
| 1   | 13.00% Valid: 13.13%; Invalid: 1.00% | 13.00% Valid: 13.00%; Invalid: 0.00% |
| 2   | 13.00% Valid: 13.13%; Invalid: 1.00% | 13.00% Valid: 13.00%; Invalid: 0.00% |
| 3   | 13.00% Valid: 13.13%; Invalid: 1.00% | 13.00% Valid: 13.00%; Invalid: 0.00% |
| Mean| 13.00% | 13.00% |
### Q3.3
<|im_start|>system\nThink step by step before answering the question, and provide the final answer as 'the answer is [answer]' format.<|im_end|>\n<|im_start|>user\nBlanch has 15 slices of pizza in the fridge. During breakfast, she eats 4 slices. At lunch, Blanch eats 2 slices, then takes two slices as a snack. Finally, she consumes 5 slices for dinner. How many slices of pizza are left?<|im_end|>\n<|im_start|>assistant\nDuring breakfast, Blanch has 15 - 4 = <<15-4=11>>11 slices left.\nAt lunch, she still has 11 - 2 = <<11-2=9>>9 slices left.\nAfter the snack, there are still 9 - 2 = <<9-2=7>>7 slices left.\nFinally after dinner, Blanch has 7 - 5 = <<7-5=2>>2 slices left.\n\nThe answer is 2<|im_end|>\n<|im_end|>
### Q3.4
| Run |  Qwen2.5-0.5B-sft | Qwen2.5-0.5B-Instruct-sft |
| --- | -------------------- | ---------------------|
| 1   | 29.00% Valid: 29.00%; Invalid: 0.00% | 33.00% Valid: 33.00%; Invalid: 0.00% |
| 2   | 31.00% Valid: 31.00%; Invalid: 0.00% | 33.00% Valid: 33.00%; Invalid: 0.00% |
| 3   | 31.00% Valid: 31.00%; Invalid: 0.00% | 32.00% Valid: 32.00%; Invalid: 0.00%|
| Mean| 31.00% | 33.00% |

### Q3.5
## Question 4
### Q4.1
### Q4.2
| Run | Overall Acc | Valid Acc | Invalid Acc |
| --- | ------ | ----- | ----- |
| 1   | 28.00% | 28.00% | 0.00% |
| 2   | 31.00% Valid: 31.00%; Invalid: 0.00% | 33.00% Valid: 33.00%; Invalid: 0.00% |
| 3   | 31.00% Valid: 31.00%; Invalid: 0.00% | 32.00% Valid: 32.00%; Invalid: 0.00%|
| Mean| 31.00% | 33.00% |
### Q4.3
## Question 5
### Q5.1
### Q5.2