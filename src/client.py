import requests
import sys
from http import HTTPStatus

# Remember to change the next two lines.
URL_PLACES = 'https://some.end.point.amazonaws.com/default/places'
URL_SCORES = 'https://some.end.point.amazonaws.com/default/scores'

def request_place(place=None):
    result = requests.get(
        URL_PLACES,
        params={'place': place} if place else None,
    )
    status_code = result.status_code
    body = result.json()
    if status_code == HTTPStatus.OK.value:
        return body
    else:
        raise RuntimeError(f'Status code { status_code }', body)

def request_starting_place_name():
    for p in request_place():
        if p['place'].startswith('__'):
            return p['place']
    raise RuntimeError("No place name with '__' prefix found.")

def convert_int_to_letter(i):
    return chr(ord('A') + i)

def convert_letter_to_int(c):
    return ord(c) - ord('A')

def convert_to_string_if_boolean(x):
    if type(x) == bool:
        return 'Yes' if x else 'No'
    else:
        return x

def print_options(options):
    for i, option in enumerate(options):
        letter = convert_int_to_letter(i)
        text = convert_to_string_if_boolean(option['text'])
        print(f'{ letter }. { text }')
    print('Q. Quit program')

def quit():
    sys.exit(0)

def create_list_of_options(size):
    return [convert_int_to_letter(e) for e in range(size)]

def valid_input(user_input, options):
    return user_input != '' and user_input[0] in options + ['Q']

def read_selection(size):
    print()
    options = create_list_of_options(size)
    while True:
        user_input = input('> ').upper()
        if valid_input(user_input, options):
            user_choice = user_input[0]
            if user_choice == 'Q':
                quit()
            else:
                print()
                return convert_letter_to_int(user_choice)
        else:
            max_letter = options[-1]
            print('You must select a letter between A and '
                  f'{ max_letter }.')
            print('Or Q to quit the program.')

def line():
    print('~' * 60)

def game_over(points):
    line()
    print(f'Your score is: { points }')
    line()
    print('G A M E   O V E R')
    line()

def update_scores(score):
    print()
    initials = input('Input your initials: ')
    initials = initials[:3].upper() # Must be 3 uppercase characters or less.
    result = requests.post(
        URL_SCORES,
        json={ 'initials': initials,
               'score': score
        })
    status_code = result.status_code
    body = result.json()
    if status_code != HTTPStatus.CREATED.value:
        raise RuntimeError(f'Status code { status_code }', body)

def print_scores():
    result = requests.get(URL_SCORES)
    status_code = result.status_code
    body = result.json()
    if status_code != HTTPStatus.OK.value:
        raise RuntimeError(f'Status code { status_code }', body)
    print()
    print('SCORES')
    print('-' * 30)
    for item in body:
        print(f'{item["initials"]:<3}{item["score"]:>4} on {item["timestamp"]}')
    print('-' * 30)

def main():
    next_place_name = request_starting_place_name()
    score = 0
    while True:
        place = request_place(next_place_name)
        statement = place['statement']
        score += place.get('points', 0)
        print(statement)
        if 'options' in place:
            options = place['options']
            print_options(options)
            selection = read_selection(len(options))
            next_place_name = options[selection]['target']
            line()
        else:
            game_over(score)
            if score > 0:
                update_scores(score)
            print_scores()
            break

if __name__ == '__main__':
    main()
