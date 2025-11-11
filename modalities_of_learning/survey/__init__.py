from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )

    education_level = models.StringField(
        choices=[['No Degree', 'No Degree'], ['Associate', 'Associate'], ['Bachelor', 'Bachelor'], ['Master', 'Master'], ['Doctoral', 'Doctoral'], ['Professional', 'Professional']],
        label='What is the highest degree of education recieved?',
        widget=widgets.RadioSelect,
    )

    metadata_strat = models.LongStringField(
        label='''
        What was your strategy to approaching each maze (if any)?'''
    )

    metadata_help = models.BooleanField(
        label='''
        Did you use any external resources?
        '''
    )
    metadata_diffnocue = models.IntegerField(
        label='''
        On a scale of 1 - 10, where 1 is super easy and 10 is impossible, how difficult was the no cue maze?
        ''',
        min=1,
        max=10
    )

    metadata_diffauditory = models.IntegerField(
        label='''
        On a scale of 1 - 10, where 1 is super easy and 10 is impossible, how difficult was the auditory cue maze?
        ''',
        min=1,
        max=10
    )

    metadata_diffvisual = models.IntegerField(
        label='''
        On a scale of 1 - 10, where 1 is super easy and 10 is impossible, how difficult was the visual cue maze?
        ''',
        min=1,
        max=10
    )

    metadata_preferred = models.StringField(
        choices=[['Auditory', 'Auditory'], ['Visual', 'Visual'], ['No Cue', 'No Cue']],
        label='Which type of cue do you prefer the most?',
        widget=widgets.RadioSelect,
    )

    metadata_giveup = models.LongStringField(
        label='''
        If you gave up, why? Leave this blank if you did not give up.
        ''',
        blank=True)


# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education_level']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['metadata_strat', 'metadata_help', 'metadata_diffnocue', 'metadata_diffauditory', 'metadata_diffvisual', 'metadata_preferred', 'metadata_giveup']

class Finish(Page):
    pass

page_sequence = [Demographics, CognitiveReflectionTest, Finish]
