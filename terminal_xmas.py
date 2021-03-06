import os
import random
import threading
import time

BULB_CHAR = '\N{BLACK STAR}'

mutex = threading.Lock()


def get_bulb(color_char):
    color_code = {'Y': 3, 'R': 1, 'G': 2, 'B': 4,
                  'dark': 0}[color_char]
    return f'\033[9{color_code}m{BULB_CHAR}\033[0m'


def switch_lights(picture_data, color_char, index_list):
    lights_off = True

    while True:
        for index in index_list:
            picture_data[index] = (get_bulb(color_char)
                                   if lights_off else get_bulb('dark'))

        mutex.acquire()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(''.join(picture_data))
        mutex.release()

        lights_off = not lights_off

        time.sleep(random.uniform(0.3, 0.6))


def main():

    with open('house.txt') as f:
        ascii_picture = f.read().partition('#')[0]

    picture_data = list(ascii_picture.rstrip())

    index_list_for_char = {}

    for i, char in enumerate(picture_data):
        if char in ('Y', 'R', 'G', 'B'):
            index_list_for_char.setdefault(char, []).append(i)
            picture_data[i] = BULB_CHAR

    threads = [threading.Thread(target=switch_lights,
                                args=(picture_data, color_char, index_list))
               for color_char, index_list in index_list_for_char.items()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
