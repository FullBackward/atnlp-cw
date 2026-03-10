import pandas as pd
import itertools
import numpy as np

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
### IMPORTANT NOTE: In the comments that include "Input" and "Output" you should consider mostly the *structure*
### of the input and the output, rather than the specific inputs match to the output as you understand.
### In some cases, the output is divorced from the input above, to not make filling in the function too easy.
### Focus on the API through these comments, in the sense that, ensure that the input and the output of the functions is correct
### (and of course, semantically correct according to your understanding).

steps = [1, 2, 3, 4]

def get_included_steps(row, steps):
    """
    Get included steps as a tuple for each row.
    
    Example:
        Input: row = {'step1_present': 0, 'step2_present': 1, 'step3_present': 0, 'step4_present': 1},
               steps = [1, 2, 3, 4]
        Output: (2, 4)
    """
    included_steps = []

    hot_encoding = np.array(list(row.values))[:-1] #[0,1,0,1]
    steps = np.array(steps)
    included_steps = steps[hot_encoding == 1] # [2,4]
    return tuple(sorted(included_steps))

def generate_all_subsets(steps):
    """
    Generate all possible subsets for the included steps.

    Example:
        Input: steps = [1, 2, 3]
        Output: [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    all_subsets_included = []
    for r in range(len(steps) + 1):
        subsets_r = list(itertools.combinations(steps, r))
        all_subsets_included.extend(subsets_r)
    return all_subsets_included

def compute_v_S(df, all_subsets_included):
    """
    Compute v(S) for all subsets of included steps.

    Example:
        Input: 
            df = pd.DataFrame({'present_steps': [(), (1,), (2,), (1, 2)], 'is_correct': [0.8, 0.7, 0.6, 0.5]})
            all_subsets_included = [(), (1,), (2,), (1, 2)]
        Output: 
            v_S = {(): 0.8, (1,): 0.7, (2,): 0.6, (1, 2): 0.5}
    """
    valid_subsets = set(all_subsets_included)

    filtered_df = df[df["present_steps"].isin(valid_subsets)]

    v_S = (
        filtered_df
        .groupby("present_steps")["is_correct"]
        .mean()
        .to_dict()
    )

    logger.debug("v_S: %s", v_S)
    return v_S

def compute_marginal_contributions(steps, v_S):
    """
    Compute the marginal contributions for each step.

    Example:
        Input:
            steps = [1, 2]
            v_S = {(): 0.85, (1,): 0.67, (2,): 0.72, (1, 2): 0.75}
        Output:
            Delta_sum = {1: 0.08, 2: 0.12}, valid_permutations_count = 2
    """
    permutations = list(itertools.permutations(steps))
    Delta_sum = {i: 0.0 for i in steps}
    valid_permutations_count = 0

    for pi in permutations:
        valid_permutation = True
        temp_delta_sum = {i: 0.0 for i in steps}

        logger.debug("Starting permutation %s", pi)

        for i in steps:
            idx_i = pi.index(i)

            S_i = pi[:idx_i]
            S_i_union_i = pi[:idx_i + 1]
            included_S_i_sorted = tuple(sorted(S_i))
            included_S_i_union_i_sorted = tuple(sorted(S_i_union_i))

            v_S_i = v_S.get(included_S_i_sorted, np.nan)
            v_S_i_union_i = v_S.get(included_S_i_union_i_sorted, np.nan)

            if np.isnan(v_S_i) or np.isnan(v_S_i_union_i):
                valid_permutation = False
                logger.debug(
                    "Invalid permutation %s at step %s: S_i=%s, S_i_union_i=%s, "
                    "v_S_i=%s, v_S_i_union_i=%s",
                    pi, i, included_S_i_sorted, included_S_i_union_i_sorted,
                    v_S_i, v_S_i_union_i
                )
                break

            marginal = v_S_i_union_i - v_S_i
            temp_delta_sum[i] += marginal

            logger.debug(
                "pi=%s, i=%s, S_i=%s, S_i_union_i=%s, v_S_i=%s, "
                "v_S_i_union_i=%s, marginal=%s, temp_delta_sum=%s",
                pi, i, included_S_i_sorted, included_S_i_union_i_sorted,
                v_S_i, v_S_i_union_i, marginal, temp_delta_sum
            )

        if valid_permutation:
            valid_permutations_count += 1

            for i in steps:
                Delta_sum[i] += temp_delta_sum[i]

            logger.debug(
                "Accepted permutation %s, temp_delta_sum=%s, Delta_sum=%s, valid_permutations_count=%s",
                pi, temp_delta_sum, Delta_sum, valid_permutations_count
            )
        else:
            logger.debug(
                "Rejected permutation %s, Delta_sum unchanged=%s",
                pi, Delta_sum
            )

    logger.debug(
        "Finished marginal contributions: Delta_sum=%s, valid_permutations_count=%s",
        Delta_sum, valid_permutations_count
    )

    return Delta_sum, valid_permutations_count

def compute_shapley_values(Delta_sum, valid_permutations_count, steps):
    """
    Compute the Shapley values for each step.

    Example:
        Input: 
            Delta_sum = {1: 0.08, 2: 0.12}
            valid_permutations_count = 2
            steps = [1, 2]
        Output: 
            Shapley_values = {1: 0.04, 2: 0.06}
    """

    shapley_values = {}
    for i in steps:
        shapley_values[i] = Delta_sum[i] / valid_permutations_count
        logger.debug('Shapley_values: {}'.format(shapley_values[i]))

    return shapley_values

def main():
    df = pd.read_csv('evaluation_with_steps.csv')

    df['present_steps'] = df.apply(get_included_steps, axis=1, args=(steps,))

    ######################################################################################
    # Question 7.1: INSERT CODE HERE: Generate all possible subsets for the included steps#
    ######################################################################################
    all_subsets = generate_all_subsets(steps)
    ###############################################
    # Question 7.2: INSERT CODE HERE: Compute v(S)#
    ###############################################
    v_s = compute_v_S(df, all_subsets)
    delta_sum, valid_permutations_count = compute_marginal_contributions(steps, v_s)
    #############################################################
    # Question 7.3: INSERT CODE HERE: Compute the Shapley values#
    #############################################################
    shapely_values = compute_shapley_values(delta_sum, valid_permutations_count, steps)
    print(shapely_values)

if __name__ == "__main__":
    main()
