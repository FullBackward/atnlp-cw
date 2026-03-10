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
### Q1.5 **WIP**
**This question I am not quite sure, it seems to me in practical that how the intermediate steps are produced is more important**\
In MQ2, the probability can be calculated from two different way: 1 is to use the Bayes rule like stated in Q1.2; 2 is to use a simple counting approach to calculate: $P(D|Y) = \frac{D_Y}{D_Y + D_X}$. The complexity of these two approaches differs allot.  
## Question 2
### Q2.2
#### a) Running the eval with temperature 0.0 gave accuracy:  77.78%
#### b) Running the eval with temperature 0.7 gave accuracy: 72.73%
#### c) When the temperature is increased from 0.0 to 0.7, the model becomes less deterministic and more willing to select lower-probability tokens. This can improve diversity, but for tasks with clear correct answers, such as mathematical questions, it usually harms performance because the model is more likely to deviate from the most reliable reasoning path. Therefore, the accuracy is expected to be lower at 0.7 than at 0.0.
#### d)Other than temperature, several inference configurations could affect model performance. One important one is maximum completion length. This controls the maximum number of output tokens the model is allowed to generate. If this limit is too small, the model may not have enough space to complete all intermediate reasoning steps or even finish its final answer, which could directly reduce accuracy on more complex tasks.

Another important parameter is top_p. This limits the model’s candidate next-token set to the smallest group of high-probability tokens whose cumulative probability reaches 
𝑝
p. In other words, instead of sampling from all possible tokens, the model samples only from a restricted probability mass. Lower values make the output more focused and conservative, while higher values allow more variation. Because of this, top_p can affect accuracy by controlling how much low-probability noise is allowed into the generation process.

A further parameter is frequency penalty, which discourages the model from repeating the same tokens too often. This can help reduce repetitive or looping outputs, which may improve response quality in some cases. However, if set too aggressively, it could also harm performance by discouraging repetition that is actually useful or necessary for the task.

Finally, structured output constraints could also improve performance. If the model is required to respond in a fixed format, such as JSON or a single-option answer format, this reduces the risk of getting the answer marked wrong due to formatting issues rather than reasoning mistakes. In tasks where the system expects a very specific answer structure, this can improve reliability even if it does not directly improve the underlying reasoning itself.
### Q2.3
#### a) {1: 0.036253115107429124, 2: 0.04065355515143354, 3: 0.03240273006892528, 4: 0.019201409936912068}
#### b) The step with the highest Shapley value is Step 2, followed by Step 1, then 3, then 4. Step 2 involves translating the natural-language word problem into logical formulas, which is likely the most valuable part of the whole method. This is because it turns the question from a free-text reasoning problem into a more structured and therefore more solvable form. Instead of spending as much effort interpreting wording, context, and hidden relations in the text, the model can work with a clearer formal representation. That likely makes the reasoning process more reliable, which would explain why Step 2 has the highest Shapley value.
#### c) Ordering the steps by their Shapley values gives: Step 2 > Step 1 > Step 3 > Step 4. This ordering is largely unsurprising. As discussed earlier, Step 2 is the stage that converts the free-text problem into logical or mathematical formulas, so it makes sense that it has the highest contribution. This step removes much of the ambiguity of natural language and turns the problem into a more structured form that is easier to reason over.

It also makes sense that Step 1 has the second-highest Shapley value. Step 1 extracts the relevant variables, entities, and pieces of information from the free text, which already reduces ambiguity significantly. The fact that Step 2 is still ranked above Step 1 suggests that, while the model is already fairly capable of identifying relevant information from natural language, the larger gain comes from explicitly structuring that information into formal relations.

The more noticeable part of the ordering is the gap between Steps 3 and 4, especially the fact that Step 4 has the lowest Shapley value. Step 3 mainly formalises the explicit facts given in the problem, so it is reasonable that its contribution is lower than Steps 1 and 2. However, Step 4, which rewrites the actual question to be solved in symbolic form, might initially seem like it should be more important. The low Shapley value suggests that the model benefits more from having the problem context and relationships clarified than from having the final target expression written out explicitly. In other words, reducing ambiguity in the setup appears to help more than formalising the final question alone.
## Question 3
### Q3.1
In finetuning/main.py, line 75 uses Datasets.train_test_split() to divide the dataset into training and testing sets. In the original code, the argument test_size was set to 0.9, meaning that 90% of the dataset would be reserved for testing and only 10% for training. This is a bug because it leaves the model with far too little training data, which would likely reduce performance and make the fine-tuning experiment unreliable. The model would be evaluated on a large unseen test set despite having learned from only a small subset of the data. The fix is to change the split so that most of the data is used for training and only a smaller portion is reserved for testing.

There are also three unused, or “dead”, variables: DATASET_NAME, DATASET_CONFIG, and device. These do not directly affect the experiment, but they should still be removed because dead code reduces clarity and makes maintenance harder

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
As stated in the _Qwen2.5 Technical Report_, the instruct model went through a large supervised fine-tuning stage, stating over **1 million** curated examples
Covering various different aspects, amongst which are mathematical step-by-step reasoning. 
While our finetuning is performed on a much smaller subset of 2700 samples. The reason Base is still quite close to Instruct 
is due to the fact that, while instruct may have a more complex learned state, it doesn't necessarily immediately translate into better performance on our task.
Which is quite clear from the difference in performance before and after our own sft. So in conclusion, instruct is not just qwen base with sft on GSM8K. Rather it is base with a large amount of added post-training that already teaches it how to follow instrcutions better
and how to perform step-by-step reasoning, such that the model can understand and perform these tasks more implecitely. Where as Base does not have this. This is also strenghtened by the fact that we performed LoRa Fine tuning, where we are updating specific parts of the model, which reduces any 
_lose_ of previously trained and learned aspects.


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