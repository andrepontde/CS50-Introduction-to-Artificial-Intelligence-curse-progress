import os
import random
import math
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = corpus
    
    remaining = 1 - damping_factor
    
    probability = {}
    all_sites = {}
    
    if len(pages[page]) == 0:
        percentage = round(1 / len(pages.keys()), 5)
        for site in pages.keys():
            probability[site] = percentage
        return probability

    else:
        for site in pages.keys():
            all_sites[site] = 0.0
            if len(pages[site]) > 1:
                for item in pages[site]:
                    all_sites[item] = 0.0
        for site in pages[page]:
            probability[site] = 0.0
        percentage = round(damping_factor/len(probability.keys()),5)
        remaining = round(remaining/len(all_sites.keys()),5)
        for site in probability.keys():
            probability[site] = round(percentage+remaining,5)
        for site in all_sites:
            all_sites[site] = remaining
            
        all_sites.update(probability)
        return all_sites
    
    
    
    
    '''
    Failed attempt
    
    
    if page in pages.keys():
        for site in pages[page]:
            probability[site] = 0.0
        percentage = damping_factor/len(probability.keys())
        remaining = remaining/(len(probability.keys())+1)
        for site in probability.keys():
            probability[site] = percentage+remaining
        probability[page] = remaining
        return probability
    else:
        percentage = 1 / (len(pages.keys())+1)
        probability[page] = percentage
        for site in pages.keys():
            probability[site] = percentage
        return probability
    '''
    #     1. Determinar si está en el corpus la key de la pagina en la que estamos
    #     2. Si si esta la pagina, dividir porcentajes en partes iguales dentro de los items - damping factor
    #     3. Si no está la pagina, regresar porcentajes iguales entre todas las paginas.
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = corpus
    ran = random.choice(list(pages.keys()))
    results = []
    sample = transition_model(corpus, ran, damping_factor)
    
    for x in range(n):
        keys = list(sample.keys())
        probability = list(sample.values())
        random_choice = random.choices(keys, weights=probability, k=1)[0]
        results.append(random_choice)
        sample = transition_model(corpus, random_choice, damping_factor)
        
    full_sample = {}
    for site in pages.keys():
        count = results.count(site)
        percentage = (count/n)
        full_sample[site] = percentage
    
    return full_sample
        
        
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = corpus
    N = len(pages)

    # Initialize pagerank values
    page_rank = {page: 1 / N for page in pages}
    
    keepTrying = True
    while keepTrying:
        new_rank = {}
        # Calculate new rank values based on the current ranks
        for page in pages:
            rank_sum = 0
            for possible_page in pages:
                if page in pages[possible_page]:
                    rank_sum += page_rank[possible_page] / len(pages[possible_page])
                if not pages[possible_page]:  # If a page has no links
                    rank_sum += page_rank[possible_page] / N
            new_rank[page] = (1 - damping_factor) / N + damping_factor * rank_sum

        # Check convergence
        keepTrying = False
        for page in pages:
            if not math.isclose(new_rank[page], page_rank[page], abs_tol=0.001):
                keepTrying = True
            page_rank[page] = new_rank[page]

    return page_rank




if __name__ == "__main__":
    main()



