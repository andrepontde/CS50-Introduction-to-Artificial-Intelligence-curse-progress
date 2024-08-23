import csv
import itertools
import sys
import pdb

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    #pdb.set_trace()
    
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    joint = 1
    
    for person in people:
        
        # For individuals without parents (founders)
        if people[person]['mother'] is None:
            if person in one_gene:
                # Probability of having one gene and the corresponding trait probability
                if person in have_trait:
                    joint *= PROBS['gene'][1] * PROBS["trait"][1][True]
                else:
                    joint *=  PROBS['gene'][1] * PROBS["trait"][1][False]
            elif person in two_genes:
                # Probability of having two genes and the corresponding trait probability
                if person in have_trait:
                    joint *= PROBS['gene'][2] * PROBS["trait"][2][True]
                else:
                    joint *= PROBS['gene'][2] * PROBS["trait"][2][False]
            else:
                # Probability of having zero genes and the corresponding trait probability
                if person in have_trait:
                    joint *= PROBS['gene'][0] * PROBS["trait"][0][True]
                else: 
                    joint *= PROBS['gene'][0] * PROBS["trait"][0][False]

        # For individuals with parents
        else:
            # Initialize mother and father gene inheritance probabilities
            mother_gene = 0
            father_gene = 0
            
            # Calculate mother's gene probability
            if people[person]['mother'] in one_gene:
                mother_gene = 0.50
            elif people[person]['mother'] in two_genes:
                mother_gene = 1 - PROBS["mutation"]
            else:
                mother_gene = PROBS["mutation"]

            # Calculate father's gene probability
            if people[person]['father'] in one_gene:
                father_gene = 0.50
            elif people[person]['father'] in two_genes:
                father_gene = 1 - PROBS["mutation"]
            else:
                father_gene = PROBS["mutation"]

            # If person has one gene
            if person in one_gene:
                # Probability of having one gene by inheriting one gene from either mother or father, but not both
                prob_gene = (mother_gene * (1 - father_gene)) + (father_gene * (1 - mother_gene))
                
                # Apply trait probability based on gene count
                if person in have_trait:
                    joint *= prob_gene * PROBS["trait"][1][True]
                else:
                    joint *= prob_gene * PROBS["trait"][1][False]
            
            # If person has two genes
            elif person in two_genes:
                # Probability of inheriting one gene from both mother and father
                prob_gene = mother_gene * father_gene

                # Apply trait probability based on gene count
                if person in have_trait:
                    joint *= prob_gene * PROBS["trait"][2][True]
                else:
                    joint *= prob_gene * PROBS["trait"][2][False]

            # If person has zero genes
            else:
                # Probability of inheriting no genes from both parents
                prob_gene = (1 - mother_gene) * (1 - father_gene)
                
                # Apply trait probability based on gene count
                if person in have_trait:
                    joint *= prob_gene * PROBS["trait"][0][True]
                else:
                    joint *= prob_gene * PROBS["trait"][0][False]

    return joint

    
    # joint = 1
    
    # for guy in people:
        
        
    #     if people[guy]['mother'] is None:
    #         if guy in one_gene:
    #             if guy in have_trait:
    #                 #Prob of trait with one gene
    #                 joint *= PROBS['gene'][1] * PROBS["trait"][1][True]
    #             else:
    #                 joint *=  PROBS['gene'][1] * PROBS["trait"][1][False]
    #         elif guy in two_genes:
    #             if guy in have_trait:
    #                 joint *= PROBS['gene'][2] * PROBS["trait"][2][True]
    #             else:
    #                 joint *= PROBS['gene'][2] * PROBS["trait"][2][False]
    #         else:
    #             if guy in have_trait:
    #                 #Here we check the probability of a person having the trait whilo not having any genes
    #                 joint *= PROBS['gene'][0] * PROBS["trait"][0][True]
    #             else: 
    #                 #Here we calculate the probability of a person not having any gene nor the trait.
    #                 joint *= PROBS['gene'][0] * PROBS["trait"][0][False]

    #     #This section is for people with parents
    #     mother_gene = 0
    #     father_gene = 0
        
    #     if people[guy]['mother'] is not None:
    #         if guy in one_gene:
    #             if people[guy]['mother'] in one_gene:
    #                 mother_gene = 0.50
    #             elif people[guy]['mother'] in two_genes:
    #                 mother_gene = 1-PROBS["mutation"]
    #             else:
    #                 mother_gene = PROBS["mutation"]
    #             if people[guy]['father'] in one_gene:
    #                 father_gene = 0.50
    #             elif people[guy]['father'] in two_genes:
    #                 father_gene = 1-PROBS["mutation"]
    #             else:
    #                 father_gene = PROBS["mutation"]
    #             if guy not in have_trait:
    #                 joint *= mother_gene*father_gene + PROBS["mutation"]*PROBS["mutation"]*PROBS["trait"][1][False]
    #             else:
    #                 joint *= (mother_gene*father_gene + PROBS["mutation"]*PROBS["mutation"])*PROBS["trait"][1][True]
    #         if guy in two_genes:
    #             if people[guy]['mother'] in one_gene:
    #                 mother_gene = 0.50
    #             elif people[guy]['mother'] in two_genes:
    #                 mother_gene = 1-PROBS["mutation"]
    #             else:
    #                 mother_gene = PROBS["mutation"]
    #             if people[guy]['father'] in one_gene:
    #                 father_gene = 0.50
    #             elif people[guy]['father'] in two_genes:
    #                 father_gene = 1-PROBS["mutation"]
    #             else:
    #                 father_gene = PROBS["mutation"]
    #             if guy not in have_trait:
    #                 joint *= mother_gene*father_gene + PROBS["mutation"]*PROBS["mutation"]*PROBS["trait"][2][False]
    #             else:
    #                 joint *= (mother_gene*father_gene + PROBS["mutation"]*PROBS["mutation"])*PROBS["trait"][2][True]
    #         else:
    #             if people[guy]['mother'] in one_gene:
    #                 mother_gene = 0.50
    #             elif people[guy]['mother'] in two_genes:
    #                 mother_gene = 1-PROBS["mutation"]
    #             else:
    #                 mother_gene = PROBS["mutation"]
    #             if people[guy]['father'] in one_gene:
    #                 father_gene = 0.50
    #             elif people[guy]['father'] in two_genes:
    #                 father_gene = 1-PROBS["mutation"]
    #             else:
    #                 father_gene = PROBS["mutation"]
    #             if guy not in have_trait:
    #                 joint *= mother_gene*father_gene + PROBS["mutation"]*PROBS["mutation"]*PROBS["trait"][0][False]
    #             else:
    #                 joint *= (mother_gene*father_gene + PROBS["mutation"]*PROBS["mutation"])*PROBS["trait"][0][True]
    
    # return joint



def update(probabilities, one_gene, two_genes, have_trait, p):
    for guy in probabilities:
        if guy in one_gene:
            probabilities[guy]["gene"][1] += p
        elif guy in two_genes:
            probabilities[guy]["gene"][2] += p
        else:
            probabilities[guy]["gene"][0] += p

        if guy in have_trait:
            probabilities[guy]["trait"][True] += p
        else:
            probabilities[guy]["trait"][False] += p

    


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene probabilities
        total_gene_prob = sum(probabilities[person]["gene"].values())
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= total_gene_prob
        
        # Normalize trait probabilities
        total_trait_prob = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= total_trait_prob



if __name__ == "__main__":
    main()
