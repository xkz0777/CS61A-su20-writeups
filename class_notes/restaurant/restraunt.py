def search(query, ranking=lambda r: -r.stars):
    results = [r for r in Restaurant.all if query in r.name]
    return sorted(results, key=ranking)

def reviewed_both(r, s):
    "Return how many people reviewed both"
    return len([p for p in r.reviewers if p in s.reviewers])

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
        return sorted(others, key=lambda r: similarity(self, r), reverse=True)[:k]

    def __repr__(self):
        return "Restaurant('{0}', '{1}')".format(self.name, self.stars)

    def __str__(self):
        return '<' + self.name + ',' + str(self.stars) + '>'

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
    reviewers = reviewers_for_restaurants.get(r['business_id'])
    Restaurant(r['name'], r["stars"], reviewers)

results = search('Thai');
for r in results:
    print(r, 'is similar to', r.similar(3))


