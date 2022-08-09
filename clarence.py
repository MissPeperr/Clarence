import asyncio
import discord
import json
from itertools import groupby
from operator import itemgetter
from channels import test
from channels import weeb
from channels import bot_testing
from giphy import surprise
from giphy import fun_times
from insult import random_insult_for_me
from insult import random_insult_for_user
from helpers import affection_phrases
from helpers import game_list
from helpers import check_role_reactions
from anime_database import insert_media
from anime_database import get_all_media
from anime_database import get_single_media
from anime_database import check_if_rec_by_exists
from anime_database import get_media_with_rec_by
from anime_database import insert_rec_by
from anime_database import delete_media

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # add a method here for checking the role msg for any reactions
    await check_role_reactions(client)


@client.event
async def on_message(message):
    clarence = client.get_user(600096634558218315)
    test_channel = client.get_channel(test)
    weeb_channel = client.get_channel(weeb)
    bot_testing_channel = client.get_channel(bot_testing)
    # for roles
    if message.author == clarence and message.channel == test_channel:
        messages = await test_channel.history(limit=1).flatten()

         # get the message and react with all the emojis to it
        if messages:
            role_msg = messages[0]
            if role_msg.author == clarence:
                # loop through each of the emojis and add it to the message
                reactions = [role_msg.add_reaction(value['emoji']) for key, value in game_list.items()]
                await asyncio.wait(reactions)

    elif message.content:
        content = message.content.upper().split(' ')
        mentions = message.mentions
        command = content[0]
        prefix = json.load(open('config.json', 'r'))['prefix']
        is_valid = True if prefix == message.content[0] else False
        available_commands = ('HELP', 'HELLO', 'PING', 'INSULT', 'SURPRISE', 'FUNTIMES', 'EGG')

        # if the author was clarence
        if message.author == client.user:
            return

        # valid commands
        if is_valid:
            if f'{command}' == f'{prefix}HELP' and message.channel.id != weeb_channel.id:
                await message.channel.send('Here is the list of available commands:\n◽ .help\n◽ .hello\n◽ .ping\n◽ .insult `me` | `@someone` | `name`\n◽ .surprise `me` | `@someone` | `name`\n◽ .rolehelp')

            if command == f'{prefix}HELLO':
                await message.channel.send('Hello! 👋')
        
            if command == f'{prefix}PING':
                # print(message.author)
                print(client.get_user(message.author.id))
                await message.channel.send('Pong! 🏓')

            # Insult people using old timey insults
            if command.startswith(f'{prefix}INSULT'):
                if ' '.join(content) == f'{prefix}INSULT ME':
                    await message.channel.send(random_insult_for_me())
                else:
                    if mentions and content[1] in mentions[0].mention:
                        await message.channel.send(random_insult_for_user(mentions[0]))
                    else:
                        person = " ".join(message.content.split(" ")[1:])
                        if person:
                            await message.channel.send(random_insult_for_user(person))
                        else:
                            await message.channel.send(f'{random_insult_for_me()} You forgot to insult someone.')
            
            #  Dumb Surprise
            if command.startswith(f'{prefix}SURPRISE'):
                if ' '.join(content) == f'{prefix}SURPRISE ME':
                    await message.channel.send(f'Are you surprised, {message.author.nick}? {surprise()}')
                elif mentions and content[1] in mentions[0].mention:
                    await message.channel.send(f'Are you surprised, {mentions[0].nick if hasattr(mentions[0], "nick") else mentions[0].name}? {surprise()}')
                else:
                    await message.channel.send(f'Are you surprised, {" ".join(message.content.split(" ")[1:])}?\n{surprise()}')
            
            # Recommend and anime or a Manga to the Weeb channel 
            if message.channel.id == weeb_channel.id or message.channel.id == bot_testing_channel.id:
                if f'{command}' == f'{prefix}HELP':
                  await message.channel.send('Here are the commands for the weebshit channel: \n◽ .help: how you got this message\n◽ .listrecs: list the current recommendations\n◽ .recommend {`anime` | `manga`} `name`: recommend an anime or a manga\n◽ .remove {`anime` | `manga`} `name`: removes the specified anime or manga from the recommendations')  
                command_index = None
                if ' '.join(content).__contains__(f'{prefix}RECOMMEND'):
                    try:
                        command_index = content.index(f'{prefix}RECOMMEND')
                        media_type = content[command_index + 1].upper()
                        media = content[content.index(media_type) + 1:]
                        media_full_name = ' '.join(media)

                        if media_type == "ANIME":
                            found_media = get_single_media(media_full_name)
                            if not found_media:
                                new_media = insert_media({'name': media_full_name, 'type_id': 2})
                                # with the new media, create a rec_by row
                                insert_rec_by({'discord_id': message.author.id, 'media_id': new_media['id']})
                                await message.channel.send(f"{new_media['name']} was added to recommendations!")
                            else:
                                if check_if_rec_by_exists(discord_id=message.author.id, media_id=found_media['id']):
                                    await message.channel.send('You have already recommended this!')
                                else:
                                    insert_rec_by({'discord_id': message.author.id, 'media_id': found_media['id']})
                                    await message.channel.send(f'{media_full_name} was recommended by {found_media["recommended_count"]} other {"person." if found_media["recommended_count"] == 1 else "people."}')
                        elif media_type == "MANGA":
                            found_media = get_single_media(media_full_name)
                            if not found_media:
                                new_media = insert_media({'name': media_full_name,'type_id': 3})
                                insert_rec_by({'discord_id': message.author.id, 'media_id': new_media['id']})
                                await message.channel.send(f"{new_media['name']} was added to recommendations!")
                            else:
                                if check_if_rec_by_exists(discord_id=message.author.id, media_id=found_media['id']):
                                    await message.channel.send('You have already recommended this!')
                                else:
                                    insert_rec_by({'discord_id': message.author.id, 'media_id': found_media['id']})
                                    await message.channel.send(f'{media_full_name} was recommended by {found_media["recommended_count"]} other {"person." if found_media["recommended_count"] == 1 else "people."}')

                    except Exception as e:
                        raise e

                elif ' '.join(content).__contains__(f'{prefix}LIST'):
                    try:
                        all_media = get_media_with_rec_by()
                        # groupby type and sort the media by title
                        sorted_media = sorted(all_media, key=itemgetter('type_name', 'name'))
                        grouped_media = groupby(sorted_media, key=itemgetter('type_name'))
                        
                        grouped_dict = {}
                        # gotta turn the groupby into a useful dict
                        for key, value in grouped_media:
                            if key not in grouped_dict:
                                value = list(value)
                                grouped_dict[key] = value
                      
                        new_msg = ''
                        grouped_dict_copy = grouped_dict
                        # build the string to be sent back to discord
                        for k in grouped_dict.keys():
                            if k != "Test Type":
                                # if the key is the first key in the dict, don't add a newline
                                if k is list(grouped_dict_copy)[0]:
                                    new_msg += f'{k}: '
                                else:
                                    new_msg += f'\n{k}: '
                                for v in grouped_dict[k]:
                                        new_msg += f'\n     ◽ {v["name"]} -- {v["recommended_count"]} {"person recommends" if v["recommended_count"] == 1 else "people recommend"}'
                        if new_msg:
                            await message.channel.send(new_msg)
                    except Exception as e:
                        raise e
                    
                elif ' '.join(content).__contains__(f'{prefix}REMOVE'):
                    try:
                        command_index = content.index(f'{prefix}REMOVE')
                        media_type = content[command_index + 1].upper()
                        media = content[content.index(media_type) + 1:]
                        media_full_name = ' '.join(media)
                        if media_type == "ANIME":
                            found_anime = get_single_media(media_full_name)
                            if found_anime:
                                delete_media(found_anime['id'])
                                await message.channel.send(f"{media_full_name} was removed from the recommendations.")
                            else:
                                await message.channel.send(f'The {media_type} {media_full_name} does not exist.')
                        elif media_type == "MANGA":
                            found_manga = get_single_media(media_full_name)
                            if found_manga:
                                delete_media(found_manga['id'])
                                await message.channel.send(f"{media_full_name} was removed from the recommendations.")
                            else:
                                await message.channel.send(f'The {media_type} {media_full_name} does not exist.')
                    except IndexError:
                        raise ValueError("Could not find command: recommend")


            # Funtimes
            if command == f'{prefix}FUNTIMES':
                await message.channel.send(fun_times())

            #  EGG!!
            if command.startswith(f'{prefix}EGG'):
                await message.channel.send(f'EGG!! 🥚')

            # Setting up role channel
            test_channel = client.get_channel(927285137371201596)
            # have clarence assign you roles for games that you have or want to be pinged for
            if command.startswith(f'{prefix}SETUPROLES'):
                # await message.channel.send('Here is the list of available commands:\n◽ .role help \n◽ .assign `@role name` \n◽ ')
                 
                #  assign roles based on emoji reactions?
                # everytime clarence starts, clarence needs to check if he's already sent this message to the correct channel, and if it isn't there, go ahead and send it:
                
                messages = await test_channel.history(limit=1).flatten()

                if messages:
                    if messages[0].author == clarence:
                       await message.channel.send('Clarence has already sent the role help in the testing channel')
                else:
                    # Siege, Overwatch, Rocket League, Golf with Your Friends, Animal Crossing, Deep Rock Galactic (aka tiny miners), Fall Guys
                    # Among Us, Sea of Theives (aka set sail), Valheim (aka vikings), Jackbox, Minecraft
                    # NOT GAME RELATED: Fellow Movie Goers (for watching a movie/show), Surivor specific tag
                    
                    
                    await test_channel.send('So you want to play a game, eh? Choose a game below, and react to this message with that game\'s corresponding emoji to get added to the @ for that game:\n\n <:dead_amongus:756981702642892870>  -  Among us (`@among us`)\n\n :peach:  -  Animal Crossing (`@acnh`)\n\n :hammer_pick:  -  Deep Rock Galactic (`@tiny miners`)\n\n <a:sadcatbean:855483700733280297>  -  Fall Guys (`@fall guys`)\n\n :golf:  -  Golf with Your Friends (`@Golf`)\n\n <:jackbox:928087064010960936>  -  Jackbox (`@Jackbox`)\n\n <:minecraft_block:928083240307265568>  -  Minecraft (`@Minecraft`)\n\n <:ow:928085482112421888>  -  Overwatch (`@OW`)\n\n :soccer:  -  Rocket League (`@RL`)\n\n :pirate_flag:  -  Sea Of Thieves (`@set sail`)\n\n :french_bread: - Tom Clancy\'s Rainbow Six Siege (`@Siege`)\n\n <a:bear_knife:855480916603174942>  -  Valheim (`@vikings`)\n\n If you would like to be tagged for movies/shows: :movie_camera:')
            
            
            if command.startswith(f'{prefix}ROLEHELP'):
                await message.channel.send('Here\'s i\'ve got for roles so far: \n .rolehelp')
                
            # check if someone adds/removes a reaction to his post in the testing channel
            

        # if you want to give clarence affection
        if message.content.upper() in affection_phrases:
            await message.channel.send('Thank you! I\'m trying my best! ♥')


# @client.event
# async def on_raw_reaction_add(payload):
#     reaction = payload.emoji
#     user = payload.member
#     role_channel = client.get_channel(927285137371201596)
#     # if is_custom_emoji(reaction):
        
#     if reaction.message.channel.id == role_channel:
#         clarence = client.get_user(600096634558218315)
#         print(f'{user} reacted with {reaction}!')
#         print('clarence heard that reaction')
#         if user.bot and user.bot != clarence:
#             return
#         # add else for when clarence needs to add more emojis to the message
#         elif user.bot == clarence:
#             print('Clarence added a reaction')
            
        # will also to check if users are already in that role (for when they click on it and they're already in the role but there's no emoji yet)
        # then a check for if they already have an emoji but would like to remove the role
        # WILL NEED ON_REACTION_REMOVE (or whatever it's called)


client.run(json.load(open('config.json', 'r'))['token'])
