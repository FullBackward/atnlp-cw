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
    Conclusion: the total number of pets in the neighbourhood is 348.
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

Yes, I think an additional formalisation step could improve the process. The current sequence identifies variables, translates relations, states facts, and formalises the final question, but it does not explicitly specify the most appropriate solution strategy. A useful additional formalisation step would be Method Selection and Simplification. In this step, the solver examines the formalised equations or probability expressions and rewrites them into the simplest directly solvable form. The purpose of this step is not to introduce new facts, but to reduce the number of possible solution paths and make the final derivation more mechanical.

For example, in MQ2, after formalising the task as finding $P(Y \mid D)$, the problem can be solved in at least two ways: by using Bayes' rule or by directly counting defective chips. Since there are 3 defective chips in total and 2 of them came from Company Y, the probability is simply:

$$
P(Y \mid D) = \frac{2}{3}
$$

This is simpler than applying the full Bayes' formula, even though both methods are valid.

Similarly, in MQ1, once the relationships have been formalised, a simplification step could substitute the known value $D = 60$ immediately, then derive $C = 120$ and $R = 168$. This reduces the problem to straightforward arithmetic.

Therefore, I do think an extra formalisation step would improve the process, because it bridges the gap between representing the problem and solving it efficiently. The existing four steps clarify the structure of the problem, but an explicit strategy-selection step would make the reasoning more reliable and less dependent on the solver informally deciding what to do next.
## Question 2
### Q2.2
#### a) 
Running the eval with temperature 0.0 gave accuracy:  77.78%
#### b) 
Running the eval with temperature 0.7 gave accuracy: 72.73%
#### c) 
When the temperature is increased from 0.0 to 0.7, the model becomes less deterministic and more willing to select lower-probability tokens. This can improve diversity, but for tasks with clear correct answers, such as mathematical questions, it usually harms performance because the model is more likely to deviate from the most reliable reasoning path. Therefore, the accuracy is expected to be lower at 0.7 than at 0.0.
#### d)
Other than temperature, several inference configurations could affect model performance. One important one is maximum completion length. This controls the maximum number of output tokens the model is allowed to generate. If this limit is too small, the model may not have enough space to complete all intermediate reasoning steps or even finish its final answer, which could directly reduce accuracy on more complex tasks.

Another important parameter is top_p. This limits the model’s candidate next-token set to the smallest group of high-probability tokens whose cumulative probability reaches 
𝑝
p. In other words, instead of sampling from all possible tokens, the model samples only from a restricted probability mass. Lower values make the output more focused and conservative, while higher values allow more variation. Because of this, top_p can affect accuracy by controlling how much low-probability noise is allowed into the generation process.

A further parameter is frequency penalty, which discourages the model from repeating the same tokens too often. This can help reduce repetitive or looping outputs, which may improve response quality in some cases. However, if set too aggressively, it could also harm performance by discouraging repetition that is actually useful or necessary for the task.

Finally, structured output constraints could also improve performance. If the model is required to respond in a fixed format, such as JSON or a single-option answer format, this reduces the risk of getting the answer marked wrong due to formatting issues rather than reasoning mistakes. In tasks where the system expects a very specific answer structure, this can improve reliability even if it does not directly improve the underlying reasoning itself.
### Q2.3
#### a) 
{1: 0.036, 2: 0.041, 3: 0.032, 4: 0.019}
#### b) 
The step with the highest Shapley value is Step 2, followed by Step 1, then 3, then 4. Step 2 involves translating the natural-language word problem into logical formulas, which is likely the most valuable part of the whole method. This is because it turns the question from a free-text reasoning problem into a more structured and therefore more solvable form. Instead of spending as much effort interpreting wording, context, and hidden relations in the text, the model can work with a clearer formal representation. That likely makes the reasoning process more reliable, which would explain why Step 2 has the highest Shapley value.
#### c) 
Ordering the steps by their Shapley values gives: Step 2 > Step 1 > Step 3 > Step 4. This ordering is largely unsurprising. As discussed earlier, Step 2 is the stage that converts the free-text problem into logical or mathematical formulas, so it makes sense that it has the highest contribution. This step removes much of the ambiguity of natural language and turns the problem into a more structured form that is easier to reason over.

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
| 3   | 31.00% Valid: 31.00%; Invalid: 0.00% | 35.00% Valid: 35.00%; Invalid: 0.00%|
| Mean| 31.00% | 34.00% |


### Q3.5
The Qwen2.5 Technical Report states that the Instruct model was already post-trained on over 1 million curated examples, including instruction-following and mathematical step-by-step reasoning. By contrast, our SFT uses only about 2,700 GSM8K examples.

This means the Instruct model starts from a much stronger state for tasks like GSM8K. It already knows better how to follow prompts and produce structured reasoning, while the Base model does not. Our smaller fine-tuning stage improves both models, but it is not enough to fully recreate the broad post-training that the Instruct model has already received.

This is also reinforced by LoRA fine-tuning, since LoRA only updates part of the model rather than fully retraining it. As a result, the Instruct model keeps more of its existing instruction-following and reasoning ability, which helps explain why it still performs better after fine-tuning.


## Question 4
### Q4.1
### Q4.2
| Run | Overall Acc | Valid Acc | Invalid Acc |
| --- | ------ | ----- | ----- |
| 1   | 28.00% | 28.00% | 0.00% |
'the answer is' count: 78(sft), 86(grpo)

The accuracy after training with GRPO is 28.00% overall, 28.00% valid accuracy and 0.00% invalid accuracy; The accuracy for SFT is 35.00% overall, 35.00% valid accuracy and 0.00& invalid accuracy. By counting the appearance of "the answer is" in the generated answers, there are 78 answers with the correct format in the SFT model, while 86 in the GRPO model, so the frequency of the phrase "the answer is" does increase. From the observing the results produced by SFT model and GRPO model, we spot the following differences:
1. The GRPO model generally produce longer answers than the SFT model. These longer answer did not guarantee a better accuracy, in certain questions we find the GRPO model over complicating the question. The model stated every step with lots of verbal explanation, but certain explaination are meaningless and verbose, for example: Since Raymond was born 25 years ago, he was born 25 years ago; these explainations did not contribute to reasoning.
2. The GRPO model seems to be overfitting to the format reward. There appears to be formats like: Therefore, the answer is: the answer is 17. This will cause evaluation to flag the answer as incorrect no matter what the answer in side the nested phrase is.
3. A new format of: "the answer is [number]", "the answer is \[\boxed{number}\]" and "the answer is \boxed{number}" appeared, which is some unexplainable phenonmenon only appears in the GRPO model.
### Q4.3
This phenonmenon is called Specification gaming, which means when a literal specification is satisfied in an unintended way, that contribute less to the goal of the specification. This phenonmenon was descibed by Google DeepMind (https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) as: a behaviour that satisfies the literal specification of an objective without achieving the intended outcome. However, there are also paper stated a phenonmenon called Shortcut learning (https://arxiv.org/pdf/2004.07780), the paper define it as: decision
rules that perform well on standard benchmarks but fail to transfer to more challenging
testing conditions, such as real-world scenarios. With consider to our reward functions, this seems inappropriate with our model, since the model has not yet solve our problem, but play around the specification to achieve better rewards. The reward function for our GPRO model has set 0.5 reward to correct format and 2.0 reward to correct answer. That means the model can get 0.5 reward simply by adding "the answer is" at the end of the answer, while to get the correct answer involve long correct reasoning steps, small changes in the reasoning steps can pivot answers alot. Compared to answering correctly, correct formating is a much cheaper and easier way to get reward for the model.
## Question 5
### Q5.1
#### Proposed Method: Self-Consistency Decoding at Evaluation Time

The main proposed improvement is to replace single-pass greedy decoding during evaluation with self-consistency decoding. In the current pipeline, the model generates only one answer for each GSM8K question, and that single output is treated as the final prediction. This makes evaluation fragile, particularly for mathematical reasoning, where one early decoding error can derail the entire reasoning chain and lead to an incorrect final answer. This issue is especially relevant for a small model, whose outputs may vary substantially depending on the exact sequence of token choices made during generation.

To address this, the evaluation procedure will be modified so that the model produces multiple candidate solutions for each question using stochastic decoding rather than greedy decoding. Specifically, sampling will be enabled in model.generate, making use of parameters such as temperature and top-p to encourage diverse reasoning paths. For each question, the model will generate five separate completions. A final numeric answer will then be extracted from each completion, and the overall prediction will be determined by majority vote across the extracted answers. In other words, the answer that appears most frequently among the sampled outputs will be selected as the model’s final response.

The motivation for this method is that mathematical reasoning often admits several possible intermediate trajectories, some of which may fail while others still converge to the correct result. Under greedy decoding, the model is forced to commit to a single reasoning path, making it highly sensitive to early mistakes. Self-consistency decoding reduces this brittleness by allowing several sampled attempts and aggregating them into one final answer. As a result, even if some generations are incorrect or contain flawed reasoning, the correct answer may still emerge as the most consistent prediction across samples.

In addition to the main change, a minor supporting adjustment may be made to the answer extraction procedure. The current fallback behaviour, which extracts the final number appearing anywhere in the output, is overly permissive and may incorrectly treat malformed generations as valid answers. Tightening this extraction logic would make the evaluation more reliable and better aligned with the output format encouraged during fine-tuning. However, this remains a supporting implementation detail rather than the main contribution. The central improvement in this section is the use of self-consistency decoding itself.

A limitation of this approach is that it does not improve the model’s underlying mathematical ability through training. Instead, it improves the robustness of inference by reducing dependence on a single sampled reasoning trace. It also increases evaluation cost, since each question must be generated multiple times. Nevertheless, this trade-off is reasonable in the present setting, as the GSM8K test subset is small and the goal of this section is to propose a meaningful and well-motivated improvement to the pipeline rather than a computationally minimal one.

Secondary Exploratory Analysis: Reward Redesign

As a secondary exploratory analysis, an additional variation can be considered in the GRPO reward design. This is not the primary proposed method, but rather a small follow-up experiment motivated by qualitative observations from earlier results. In particular, some GRPO outputs showed bracketed answers, nested answer phrases, and other formatting artefacts, suggesting that the current reward structure may not distinguish strongly enough between merely matching the expected template and producing a correctly formatted final answer.

To explore this, the reward function could be modified so that outputs receiving both the correct answer and the correct format obtain a slightly higher reward than outputs that are correct but badly formatted. For example, the reward for correct answer + correct format could be set to 2.5, while the reward for correct answer + incorrect format remains 2.0. At the same time, the reward for format compliance alone could be increased to 1.0. The intention is to give the model a clearer incentive structure: correct reasoning remains the main objective, but properly formatted correct answers are preferred over loosely formatted ones.

This secondary analysis is included only as an exploratory extension. Unlike self-consistency decoding, which directly targets the brittleness of evaluation, the reward redesign changes the training objective itself and would require additional GRPO training runs. It is therefore treated as a supplementary investigation rather than the main proposed improvement.### Q5.2

### Q5.2
From Q5.1, two hypotheses were investigated:

Hypothesis 1. The proposed multi-sample, vote-based evaluation process provides a more robust estimate of model performance on mathematical reasoning than the original single greedy decode evaluation.

Hypothesis 2. A revised three-scenario reward mechanism, which distinguishes between correct answers with correct format and correct answers with incorrect format, improves GRPO training performance.

Experiments

Newly trained GRPO model with the revised three-scenario reward mechanism, evaluated on the original evaluation pipeline.

Pretrained GRPO model from Q4, evaluated on the new self-consistency evaluation pipeline.

Newly trained GRPO model with the revised three-scenario reward mechanism, evaluated on the new self-consistency evaluation pipeline.

Pretrained SFT model from Q3, evaluated on the new self-consistency evaluation pipeline.

Results

Experiment 1: overall accuracy = 26.00%, valid accuracy = 26.00%, invalid rate = 0.00%

Experiment 2: overall accuracy = 49.00%, valid accuracy = 52.69%, invalid rate = 7.00%

Experiment 3: overall accuracy = 35.00%, valid accuracy = 39.77%, invalid rate = 12.00%

Experiment 4: overall accuracy = 46.00%, valid accuracy = 48.42%, invalid rate = 5.00%

Discussion

The results provide preliminary support for Hypothesis 1, but they do not support Hypothesis 2.

For Hypothesis 1, both the GRPO and SFT models performed better under the new evaluation pipeline than under the original single-pass greedy evaluation. Previously, the best SFT-Instruct result was 35.00%, whereas under the new evaluation pipeline the pretrained SFT model reached 46.00%. Similarly, the pretrained GRPO model reached 49.00% under the new pipeline. This suggests that the added self-consistency decoding procedure, together with the tighter answer extraction logic, captures correct answers that may be missed when evaluation depends on only one greedy generation.

However, this comparison should be interpreted carefully. The evaluation setup was changed not only through multi-sample majority voting, but also through answer extraction that was made more closely aligned with the fine-tuning target format. As a result, some of the observed improvement may come from more appropriate evaluation rather than from the decoding change alone. Even so, the results still suggest that single-pass greedy decoding likely understated the performance of both models, especially on tasks where one early decoding error can derail the full reasoning chain.

For Hypothesis 2, the revised three-scenario reward mechanism did not improve performance. The newly trained GRPO model performed worse than the pretrained GRPO model under both evaluation settings, scoring 26.00% on the original pipeline and 35.00% overall accuracy on the new pipeline. This indicates that the modified reward design did not successfully improve reasoning performance in this setup.

One possible explanation is that the revised reward mechanism still does not reward good intermediate reasoning strongly enough. It changes how formatting is valued, but it may still fail to guide the model toward more reliable mathematical solution paths. In other words, the reward adjustment may have changed the surface behavior of the model more than its actual reasoning quality.

Conclusion

Overall, the main proposed method, self-consistency decoding at evaluation time, appears to be the more useful improvement. It produced higher reported performance for both pretrained models and seems to provide a more robust estimate than relying on a single greedy decode. By contrast, the revised three-scenario reward mechanism should be treated as a secondary exploratory analysis, since the current experiments do not show evidence that it improves performance. Under the present setup, the reward modification did not help, whereas the evaluation-time self-consistency method showed clearer practical benefit.