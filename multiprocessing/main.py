import multiprocessing

def calculate_square(number, result, index):
    """
    Function to calculate the square of a given number.
    """
    result[index] = number * number

def calculate_cube(number, result, index):
    """
    Function to calculate the cube of a given number.
    """
    result[index] = number * number * number

def main():
    # Number to process
    number = 5

    # Create an array to store results
    result = multiprocessing.Array('i', 2)

    # Create processes
    process_square = multiprocessing.Process(target=calculate_square, args=(number, result, 0))
    process_cube = multiprocessing.Process(target=calculate_cube, args=(number, result, 1))

    # Start processes
    process_square.start()
    process_cube.start()

    # Wait for processes to complete
    process_square.join()
    process_cube.join()

    # Print results
    print(f"Square: {result[0]}")
    print(f"Cube: {result[1]}")

if __name__ == "__main__":
    main()