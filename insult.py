import random
import discord

insults = {
    'descriptor_list': ['pokey', 'artless',
        'bawdy',
        'beslubbering',
        'bootless',
        'churlish',
        'cockered',
        'clouded',
        'craven',
        'currish',
        'dankish',
        'dissembling',
        'droning',
        'errant',
        'fawning',
        'fobbing',
        'froward',
        'frothy',
        'gleeking',
        'goatish',
        'gorbellied',
        'impertinent',
        'infectious',
        'jarring',
        'loggerheaded',
        'lumpish',
        'mammering',
        'mangled',
        'mewling',
        'paunchy',
        'pribbling',
        'puking',
        'puny',
        'qualing',
        'rank',
        'reeky',
        'roguish',
        'ruttish',
        'saucy',
        'spleeny',
        'spongy',
        'surly',
        'tottering',
        'unmuzzled',
        'vain',
        'venomed',
        'vallainous',
        'warped',
        'wayword',
        'weedy',
        'yeasty'],
    'verb_list': ['little', 'base-court',
        'bat-fowling',
        'beef-witted',
        'beetle-headed',
        'boil-brained',
        'clapper-clawed',
        'clay-brained',
        'common-kissing',
        'crook-pated',
        'dismal-dreaming',
        'dizzy-eyed',
        'doghearted',
        'dread-bolted',
        'earth-vexing',
        'elf-skinned',
        'fat-kidneyed',
        'fen-sucked',
        'flap-mouthed',
        'fly-bitten',
        'folly-fallen',
        'fool-born',
        'full-gorged',
        'guts-griping',
        'half-faced',
        'hasty-witted',
        'hedge-born',
        'hell-hated',
        'idle-headed',
        'ill-breeding',
        'ill-nurtured',
        'knotty-pated',
        'milk-livered',
        'motley-minded',
        'onion-eyed',
        'plume-plucked',
        'pottle-deep',
        'pox-marked',
        'reeling-ripe',
        'rough-hewn',
        'rude-growing',
        'rump-fed',
        'shard-borne',
        'sheep-biting',
        'spur-galled',
        'swag-bellied',
        'tardy-gaited',
        'tickle-brained',
        'toad-spotted',
        'unchin-snouted',
        'weather-bitten'],
    'noun_list': ['flab-biscuit', 'clotpole',
        'coxcomb',
        'codpiece',
        'death-token',
        'dewberry',
        'flap-dragon',
        'flax-wench',
        'flirt-gill',
        'foot-licker',
        'fustilarian',
        'giglet',
        'gudgeon',
        'haggard',
        'harpy',
        'hedge-pig',
        'horn-beast',
        'hugger-mugger',
        'joithead',
        'lewster',
        'lout',
        'maggot-pie',
        'malt-worm',
        'mammet',
        'measle',
        'minnow',
        'miscreant',
        'moldwarp',
        'mumble-news',
        'nut-hook',
        'pigeon-egg',
        'pignut',
        'puttock',
        'pumpion',
        'ratsbane',
        'scut',
        'skainsmate',
        'strumpet',
        'varlot',
        'vassal',
        'whey-face',
        'wagtail']
}

def random_insult_for_user(user):
    first_word = insults['descriptor_list'][random.randrange(0,41)]
    if type(user) == discord.member.Member and hasattr(user, 'nick'):
        if first_word.startswith(('a', 'e', 'i', 'o', 'u')):
            return f'{user.nick} is an {first_word}, {insults["verb_list"][random.randrange(0,41)]}, {insults["noun_list"][random.randrange(0,41)]}.'
        else:
            return f'{user.nick} is a {first_word}, {insults["verb_list"][random.randrange(0,41)]}, {insults["noun_list"][random.randrange(0,41)]}.'
    else:
        return f'{user} is a {first_word}, {insults["verb_list"][random.randrange(0,41)]}, {insults["noun_list"][random.randrange(0,41)]}.'

def random_insult_for_me():
    return f'You {insults["descriptor_list"][random.randrange(0,41)]}, {insults["verb_list"][random.randrange(0,41)]}, {insults["noun_list"][random.randrange(0,41)]}.'