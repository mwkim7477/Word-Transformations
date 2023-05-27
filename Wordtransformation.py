"""
Matt Kim
Word Transformations Coding Challenge
"""

import sys, Levenshtein

def dictionaryify(word):
    """
    Returns a dictionary of a string that
    contains the composition of characters
    """
    compositiondict = {}
    for char in word:
        if char not in compositiondict:
            compositiondict[char] = 1
        else:
            compositiondict[char] += 1
    return compositiondict

def minlevdist(possiblemoves, endword):
    """
    Returns the word with the min levenshtein distance against endword as well as its distance.
    If no possiblemoves is empty, return False
    """
    if possiblemoves == []:
        return False
    outword = possiblemoves[0]
    distance = Levenshtein.distance(outword, endword)
    for word in possiblemoves[1:]:
        comparelevenshtein = Levenshtein.distance(word, endword)
        if distance > comparelevenshtein:
            distance = comparelevenshtein
            outword = word
    return [outword, distance]

def addletter(currentword, wordlist, endword, currentroute):
    """
    Finds all valid words from adding one letter and
    returns the one with the lowest min levenshtein distance against endword
    """
    possiblemoves = []
    for word in wordlist:
        if len(word) == len(currentword) + 1:
            #Check alignment of letters of everything other
            #than the extra letter to confirm validity
            for i in range(0, len(currentword) + 1):
                #Ignoring the added letter, checks to confirm the word == currentword
                if word[:i] + word[i + 1:] == currentword and \
                   word not in currentroute:
                    #If the left and right are the same, append to possible moves
                    possiblemoves.append(word)

    return minlevdist(possiblemoves, endword)

def deleteletter(currentword, wordlist, endword, currentroute):
    """
    Finds all valid words from deleting a letter and
    returns the one with the lowest min levenshtein distance against endword
    """
    possiblemoves = []
    for i in range(0, len(currentword)):
        deletedoneletter = currentword[:i] + currentword[i + 1:]
        if deletedoneletter in wordlist and len(deletedoneletter) >= 3 \
           and deletedoneletter not in currentroute:
            possiblemoves.append(deletedoneletter)

    return minlevdist(possiblemoves, endword)

def changeletter(currentword, wordlist, endword, currentroute):
    """
    Finds all valid words from changing one letter and
    returns the one with the lowest min levenshtein distance against endword
    """
    possiblemoves = []
    for word in wordlist:
        if len(word) == len(currentword):
            #Check to see if a letter has been changed if
            #everything on the left side of the letter and the right is equal to the
            #left and right parts of the current word
            for i in range(0, len(currentword)):
                #Example: HE*LTH where * represents the changed letter
                # Left = HE, right = LTH
                if word[:i] == currentword[:i] and \
                   currentword[i + 1:] == word[i + 1:] and \
                   word not in currentroute:
                    #If the left and right are the same, append to possible moves
                    possiblemoves.append(word)

    return minlevdist(possiblemoves, endword)

def takeanagram(currentword, wordlist, endword, currentroute):
    """
    Finds all anagrams and returns the one with
    the lowest min levenshtein distance against endword
    """
    currentcomposition = dictionaryify(currentword)
    possiblemoves = []
    for word in wordlist:
        #Avoid the same word and words less than 3 characters
        if dictionaryify(word) == currentcomposition and len(word) >= 3 \
           and word not in currentroute:
            possiblemoves.append(word)

    return minlevdist(possiblemoves, endword)

def transformword(initialword, endword, costs):
    """
    Returns the optimal cost of transforming
    the initial word to the end word
    """
    moves = [addletter, deleteletter, changeletter]
    currentiteration = initialword
    cost = 0
    words = [word.rstrip() for word in open("mywords.txt", 'r').readlines()]
    route = [initialword]
    #Grabs smallest lev dist out of all 4 moves to find next move
    while currentiteration != endword:
        movecost = costs[3]
        LD = takeanagram(currentiteration, words, endword, route)
        nomovescheck = False
        if LD != False:
            word = LD[0]
            LD = LD[1]
            nomovescheck = True
        else:
            #For comparison
            LD = float("inf")
        #Iterate through the remaining possible move functions
        for i in range(0, len(moves)):
            compare = moves[i](currentiteration, words, endword, route)
            if compare is False:
                continue
            compareLD = compare[1]
            compareword = compare[0]
            if compareLD < LD:
                LD = compareLD
                word = compareword
                movecost = costs[i]
                nomovescheck = True
            elif compareLD == LD:
                #Prioritize move based on smaller cost
                if costs[i] <= movecost:
                    LD = compareLD
                    word = compareword
                    movecost = costs[i]
                    nomovescheck = True
        if nomovescheck is False:
            return [-1, []]
        cost += movecost
        currentiteration = word
        route.append(word)

    return [cost, route]

if __name__ == "__main__":
    standardinput = sys.stdin.readlines()
    movecosts = [int(mymovecost) for mymovecost in standardinput[0].split(" ")]
    output = transformword(standardinput[1].rstrip(), standardinput[2].rstrip(), movecosts)
    print output[0]
    print output[1]
