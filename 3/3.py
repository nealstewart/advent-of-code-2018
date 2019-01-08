from typing import NamedTuple
import numpy as np
import re
import matplotlib.pyplot as plt

class Claim(NamedTuple):
    claim_id: int
    x: int
    y: int
    width: int
    height: int

regular_expression = re.compile(r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")
def create_claim(line: str):
    return Claim(*[int(match) for match in regular_expression.findall(line)[0]])

def get_claims():
    with open('input.csv') as f:
        return [create_claim(line) for line in f]
    
def get_right_side(claim: Claim):
    return claim.x + claim.width

def get_bottom(claim: Claim):
    return claim.y + claim.height

def claim_is_free(claim: Claim, claim_counts: np.ndarray):
    claim_area = claim_counts[claim.x:get_right_side(claim), claim.y:get_bottom(claim)]
    return np.sum(claim_area) == claim.width * claim.height

def do_task():
    claims = get_claims()
    max_x = max([get_right_side(claim) for claim in claims])
    max_y = max([get_bottom(claim) for claim in claims])

    claim_counts = np.zeros(shape=(max_x + 1, max_y + 1))

    for claim in claims:
        claim_counts[claim.x:get_right_side(claim), claim.y:get_bottom(claim)] += 1

    plt.imshow(claim_counts, cmap='hot', interpolation='nearest')

    claim = next((claim for claim in claims if claim_is_free(claim, claim_counts)), None)
    if (claim):
        print("yay", claim.claim_id)
    else:
        print("boo didn't find it")
    plt.savefig('heatmap.png')


do_task()