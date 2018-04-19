import groupy
from creds import groupme_key
from progress_report import ratio
from datework import year_progress
from base_query import game_count
from base_query import progress

client = groupy.Client.from_token(groupme_key)
groups = list(client.groups.list_all())

if ratio >= 1:
    progress_message = ("Progress on Nick's Board Game Challenge Update: Currently, the progress ratio is {} and we are on track to finish by year end").format(round(ratio, 3))
else:
    progress_message = ("Progress on Nick's Board Game Challenge Update: Currently, the progress ratio is {} at this rate {} games will be played out of {}").format(round(ratio, 3), (round(ratio * game_count, 0)), game_count)

if __name__ == '__main__':
    for group in groups:
        if group.name == 'Board Game Chats':
            group.post(progress_message)