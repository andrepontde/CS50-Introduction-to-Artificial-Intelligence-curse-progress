import pagerank as pr

# tester = pr.crawl("corpus2")

# tester = pr.transition_model("corpus0",'2.html',0.85)

# tester = pr.sample_pagerank("corpus0",.85,10000)

tester = pr.iterate_pagerank("corpus1",.85)

# tester = {'Test': 4}

print(tester)