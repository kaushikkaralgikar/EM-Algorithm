import numpy
import random
import requests
import json

get_link = 'https://24zl01u3ff.execute-api.us-west-1.amazonaws.com/beta'

draws = []

for i in range(30):
    #load data for 30 draws from the API
    response = requests.get(get_link)
    if response.ok:
        json_data = json.loads(response.content)
        flip = json_data["body"]
        draws.append(flip)
    else:
        print("Cannot get the draws of the coins")

#initialize the biases at random
theta_1 = random.random()
theta_2 = random.random()
print("Initial theta_1 = %.3f theta_2 = %.3f " %(theta_1, theta_2)) 


def calcuate_probabilty(flip, theta_1, theta_2):
    # P(A | B)
    no_of_heads = flip.count("1")
    likelihood_1 = pow(theta_1, no_of_heads) * pow(1-theta_1,len(flip)-no_of_heads)
    likelihood_2 = pow(theta_2, no_of_heads) * pow(1-theta_2,len(flip)-no_of_heads)
    prob_1 = likelihood_1 / (likelihood_1 +likelihood_2)
    prob_2 = likelihood_2 / (likelihood_1 +likelihood_2)
    return prob_1, prob_2

def expectation(draws, theta_1, theta_2):
    
    """Produce the expected value for heads_1, tails_1, heads_2, tails_2 
    over the draws given the coin biases"""

    heads_1, tails_1, heads_2, tails_2 = 0,0,0,0

    for flip in draws:                                  

        prob_1, prob_2 = calcuate_probabilty(flip,theta_1,theta_2)

        heads_1 += prob_1*flip.count("1")
        tails_1 += prob_1*flip.count("0")
        heads_2 += prob_2*flip.count("1")
        tails_2 += prob_2*flip.count("0")

    return heads_1, tails_1, heads_2, tails_2

def maximization(heads_1, tails_1, heads_2, tails_2):
    
    """Produce the values for theta that maximize the expected number of heads/tails"""

    theta_1 = heads_1/(heads_1+tails_1)
    theta_2 = heads_2/(heads_2+tails_2)
    return theta_1, theta_2

iterations = 10                                                  #randomize the number of iterations

if draws!=[]:
    print("Running EM Algorithm")
    for i in range(iterations):
        heads_1, tails_1, heads_2, tails_2 = expectation(draws, theta_1, theta_2)  #expectation step
        theta_1, theta_2 = maximization(heads_1, tails_1, heads_2, tails_2)        #maximization step
        print("theta_1 = %.3f theta_2 = %.3f " %(theta_1, theta_2))                    #final values