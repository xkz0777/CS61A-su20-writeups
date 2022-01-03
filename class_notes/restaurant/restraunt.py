def search(query, ranking=lambda r: -r.stars):
    results = [r for r in Restaurant.all if query in r.name]
    return sorted(results, key=ranking)

def reviewed_both(r, s):
    "Return how many people reviewed both"
    "both list are sorted"
    def sorted_overlap(s, t):
        "s and t are both sorted, return the common terms"
        i, j, count = 0, 0, 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                count += 1
                i, j = i + 1, j + 1
            elif s[i] < t[j]:
                i = i + 1
            else:
                j = j + 1
        return count
    return sorted_overlap(r.reviewers, s.reviewers)

class Restaurant:
    all = []
    def __init__(self, name, stars, reviewers):
        self.name = name
        self.stars = stars
        self.reviewers = reviewers
        Restaurant.all.append(self)

    def similar(self, k, similarity=reviewed_both):
        "Return the k most similar restaurants to self"
        others = list(Restaurant.all)
        others.remove(self)
        return sorted(others, key=lambda r: -similarity(self, r))[:k]

    def __repr__(self):
        return '<' + self.name + '>'

import json

reviewers_for_restaurants =  {}

for line in open('reviews.json'):
    r = json.loads(line)
    biz = r['business_id']
    if biz not in reviewers_for_restaurants:
        reviewers_for_restaurants[biz] = []
    reviewers_for_restaurants[biz].append(r['user_id'])

for line in open('restaurants.json'):
    r = json.loads(line)
    reviewers = reviewers_for_restaurants.get(r['business_id'], [])
    Restaurant(r['name'], r["stars"], sorted(reviewers))

while True:
    print('>', end = ' ')
    results = search(input().strip())
    for r in results:
        print(r, 'share reviewers with', r.similar(5))


