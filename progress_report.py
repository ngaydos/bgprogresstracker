from datework import year_progress
from base_query import progress
from base_query import game_count

ratio = progress/year_progress

if __name__ == '__main__':
    if ratio >= 1:
        print(("Current ratio is {}, on track to finish by year end").format(ratio))
    else:
        print(("Current ratio is {}, at this rate {} games will be played out of {}").format(ratio, (round(ratio * game_count, 0)), game_count))