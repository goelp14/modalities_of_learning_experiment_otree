from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # age = models.IntegerField(label='What is your age?', min=13, max=125)
    # gender = models.StringField(
    #     choices=[['Male', 'Male'], ['Female', 'Female']],
    #     label='What is your gender?',
    #     widget=widgets.RadioSelect,
    # )

    consent = models.BooleanField(
        label='Do you consent to collecting data for this experiment?',
    )


# FUNCTIONS

# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['consent']




page_sequence = [Introduction]
