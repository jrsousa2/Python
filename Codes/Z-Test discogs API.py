import discogs_client

# CALLS THE DISCOGS OBJECT (NEEDS USER TOKEN)
my_user_token = "ilGcsgSAIoyCVAFmJfFZIqmcmJFynUFVCtbHaiAM"
d = discogs_client.Client('ExampleApplication/0.1', user_token=my_user_token)

release = d.release(1293022)
print(release.title)

release2 = d.release(13814)
print(release2.title)

release3 = d.master(13814)
print(release3.title)

artists = release.artists

import timeit

strings = ['foo', 'bar', 'baz'] * 1000000  # Create a list with 3 million strings
target = 'baz'

# Measure execution time of using for loop
def search_using_for_loop():
    for string in strings:
        if target in string:
            return True
    return False

for_loop_time = timeit.timeit(search_using_for_loop, number=100)

# Measure execution time of using any with generator expression
def search_using_any_generator_expression():
    return any(target in string for string in strings)

any_generator_expression_time = timeit.timeit(search_using_any_generator_expression, number=100)

# Measure execution time of using any with list comprehension
def search_using_any_list_comprehension():
    return any([target in string for string in strings])

any_list_comprehension_time = timeit.timeit(search_using_any_list_comprehension, number=100)

print(f'Time taken using for loop: {for_loop_time:.6f} seconds')
print(f'Time taken using any with generator expression: {any_generator_expression_time:.6f} seconds')
print(f'Time taken using any with list comprehension: {any_list_comprehension_time:.6f} seconds')
