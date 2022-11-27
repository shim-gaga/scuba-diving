from gensim.summarization import keywords

text = 'Compatibility of systems of linear constraints over the set of natural numbers. ' \
       'Criteria of compatibility of a system of linear Diophantine equations, strict inequations,and nonstrict inequations are considered.' \
       'Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types systems are given. ' \
       'These criteria and the corresponding algorithms for constructing a minimal' \
       'supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.'

print(keywords(text, scores=True, lemmatize=True))