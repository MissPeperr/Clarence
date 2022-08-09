""" helper methods """
affection_phrases = ('I LOVE YOU CLARENCE', 'GOOD JOB CLARENCE', 'GREAT JOB CLARENCE', 'THANK YOU CLARENCE', 'GOOD BOY CLARENCE', 'FANTASTIC JOB CLARENCE')

game_list = {
    'Among Us': {'emoji': '<:dead_amongus:756981702642892870>', 'tag': '<@&754391827540344933>'},
    'Animal Crossing': {'emoji': '🍑', 'tag': '<@&711290370859860019>'},
    'Deep Rock Galactic': {'emoji': '⚒️', 'tag': '<@&734179758132297831>'},
    'Fall Guys': {'emoji': '<a:sadcatbean:855483700733280297>', 'tag': '<@&742910472562540554>'},
    'Golf with Your Friends': {'emoji': '⛳','tag': '<@&554840253832101889>'},
    'Jackbox': {'emoji': '<:jackbox:928087064010960936>', 'tag': '<@&898712386037493790>'},
    'Minecraft': {'emoji': '<:minecraft_block:928083240307265568>', 'tag': '<@&481595122660933632>'},
    'Overwatch': {'emoji': '<:ow:928085482112421888>', 'tag': '<@&498225245895917568>'},
    'Rocket League': {'emoji': '⚽', 'tag': '<@&539965913269796864>'},
    'Sea Of Thieves': {'emoji': '🏴‍☠️', 'tag': '<@&782339263386615818>'},
    'Siege': {'emoji': '🥖', 'tag': '<@&427979363598860288>'},
    'Valheim': {'emoji': '<a:bear_knife:855480916603174942>', 'tag': '<@&809220924334932028>'}
}
                
game_names = {
    'Siege': 'Tom Clancy\'s Rainbow Six Siege'
}

# TODO:
def is_server_owner(user):
    return user


async def check_role_reactions(client):
    test_channel = client.get_channel(927285137371201596)
    clarence = client.get_user(600096634558218315)
    # check for the msg in the test channel
    messages = await test_channel.history(limit=1).flatten()
    
    if messages:
        if messages[0].author == clarence:
            role_msg = messages[0]
            print(role_msg)