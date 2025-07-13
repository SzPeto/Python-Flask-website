# Example decorator definition
def decorator(func):
    def wrapper():
        print("Before the original function")
        func()  # Calls the original 'greet'
        print("After the original function")
    return wrapper

@decorator
def greet():
    print("Hello!")

# Now, calling greet() actually calls the wrapper:
# greet = decorator(greet)  Replaces 'greet' with the wrapper function returned by 'decorator'
greet()  # Outputs:
         # Before the original function
         # Hello!
         # After the original function