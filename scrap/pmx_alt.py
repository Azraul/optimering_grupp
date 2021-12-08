# Original conde: https://www.uio.no/studier/emner/matnat/ifi/INF3490/h16/exercises/inf3490-sol2.pdf

def pmx(parent1, parent2, cross1, cross2):
    
    def pmx_child(parent1, parent2, crosspoint1, crosspoint2):
        # Generate empty child
        child = [None]*len(parent1)
        # Copy a slice from parent1:
        child[crosspoint1:crosspoint2] = parent1[crosspoint1:crosspoint2]

        # Map the same slice in parent2 to child using indices from parent1:
        for i,p in enumerate(parent2[crosspoint1:crosspoint2]):
            i += crosspoint1
            if p not in child:
                while child[i] != None:
                    i = parent2.index(parent1[i])       # Get the index in parent2 where the value from parent1 is
                child[i] = p                            # Add the value not in child to the index position

        # Copy over the rest from parent2
        for i,c in enumerate(child):
            if c == None:
                child[i] = parent2[i]

        return child

    child1 = pmx_child(parent1, parent2, cross1, cross2)
    child2 = pmx_child(parent2, parent1, cross1, cross2)

    return child1, child2