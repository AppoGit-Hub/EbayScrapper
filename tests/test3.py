

def thing(d, e, f):
    pass

def another(a, b, c): thing(a, b, {
    "g" : c 
})
    
another(1, 2, 3)

def other(type: object, value):
    print(type(value))

other(int, "12")