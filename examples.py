from psm import *

class Statistics(SchemaModel, allow_unknowns=False):
    level = IntegerField(required=True, nullable=False, _min=0, _max=60)
    xp_collected = IntegerField(required=True, nullable=False)
    time_played = FloatField(required=False, nullable=True)
    achievements = ListField(
        type_mapping = [
            StringField(
                required=True,
                nullable=False,
                allowed=[
                    'first wave',
                    'lord of goats',
                    'smeller of cheese'
                ]
            )
        ],
        required=True,
        nullable=False,
        max_length=50
    )
    infractions = DictField(
        key_type = StringField(required=True, nullable=False),
        value_type = IntegerField(required=True, nullable=False),
        required = True,
        nullable = True
    )

class BotStatistics(Statistics):
    servers_visited = IntegerField(required=True, nullable=False)

class Account(SchemaModel):
    username = StringField(required=True, nullable=False, forbidden=['intxparts', 'bob'])
    stats = ObjectField(Statistics, required=True, nullable=False)

class Player(SchemaModel):
    email = StringField(required=True, nullable=False)
    accounts = ListField(
        type_mapping=[ObjectField(Account, required=True, nullable=False)],
        required=True,
        nullable=False
    )


def create_new_player(email, username):
    new_player_stats = Statistics(
        level = 0,
        xp_collected = 0,
        time_played = 0.0,
        achievements = [],
        infractions = None
    )

    new_player_account = Account(
        username = username,
        stats = new_player_stats
    )

    new_player = Player(
        email = email,
        accounts = [new_player_account]
    )

    return new_player

new_player = create_new_player('John Doe', 'django')

new_player_str = serialize(new_player)
print(new_player_str)

new_player_stats_str = serialize(new_player.accounts[0].stats)

# {"level": 0, "xp_collected": 0, "time_played": 0.0, "achievements": [], "infractions": null}
print(new_player_stats_str)

