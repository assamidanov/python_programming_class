def hypothenuse(adjacent, opposite):
    # square root of sum of squares of the triangle legs
    # [2] Pythagoras, Geometry of Euclid
    return (adjacent**2 + opposite**2)**0.5


def hypothenuse(adjacent: float, opposite: float) -> float:
    """
    Calculate length of the hypothenuse of the right triangle.
    Look here: Pythagoras, Geometry of Euclid.
    
    param adjacent: length of the first triangle leg
    param opposite: length of the other triangle leg
    return: lenth of the hypothenuse


    """
    length = (adjacent**2 + opposite**2)**0.5
    assert length == (adjacent**2 + opposite**2)**0.5, "OUCH!!! Pythagorean theorom doesn't work!"
    return length 

# def divide(a,b):
#     assert b != 0, "The divisor must not be zero"
#     result = a/b
#     return result

def sqrt(x):
    """Calculate the square root of a non-negatice x"""
    #Precondition
    assert x>= 0, "Precondition failed: x must be non-negative"
    # Functional Implementation
    result = x ** 0.5
    # Postconditions
    assert result >= 0, "Post condition failed: result should be non-negative"
    return result 




def main():
    x,y = [float(a) for a in input().split()]
    print('Hypothenuse is ', hypothenuse(x,y))
    #divide(x,y)

if __name__ == "__main__":
    #assert 2+2 == 5, "Joke!"
    main()

