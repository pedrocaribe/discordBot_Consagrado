# Import main modules
import discord, random, asyncio, time

# Import secondary modules
from discord.ext import commands
from googlesearch import search
from datetime import datetime
# from googletrans import Translator

# Import variables and standard functions from local file
from var_Reuse import *


# Define class
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    '''Commands defined in this cog are general purpose commands
    mostly fun and useful commands for users to enjoy.

    cog_generalCommands v3.05'''


    # Google search using googlesearch API
    @commands.command(name='pesquisa', aliases = ['google', 'search', 'procurar', 'achar', 'pesquisar'], help='Uso: /pesquisa "Termo" qtDeLinks (de 1 a 10)')
    async def pesquisa(self, ctx, term: str, am: int):

        # Trigger typing decorator
        await ctx.trigger_typing()

        # Search for words specified by user and return the amounts of results requested by the user
        for j in search(term, tld='co.in', num=am, stop=am, pause=2):
            await ctx.send(j)

    
    # Simple arbitrage betting system
    @commands.command(name='aposta', help='Uso: ValorParaAposta (ou número 0) M1_do_Site1 M2_do_Site1 M1_do_Site2 M2_do_Site2 LucroDesejado (ou número 0)\n\nSe o número 0 foi usado em ValorParaAposta, deve haver um número para o LucroDesejado que não seja 0\nE vice-versa.')
    async def bet(self, ctx, bet: float, a: float, a_: float, b: float, b_: float, c: float):

        # Limit arbitrage simulations to happen in FORUMs channel
        if ctx.channel.category.name != '--FORUMS--': 
            return await ctx.reply(f'Faz o seguinte, **{random.choice(fraseMeio)}**... Entra no fórum ali na esquerda chamado "__APOSTAS__". Se não tiver um Tópico aberto com seu nome, abre um e me chama de lá.\nSe já tiver, é só entrar no seu tópico e me chamar também.')
        
        # Initialize variables
        winner_1 = winner_2 = bet_winner_1 = bet_winner_2 = None

        # Compare odds between sites and declare winner for each
        winner_1 = a if a > b else b
        winner_2 = a_ if a_ > b_ else b_

        # Apply arbitrage algorithm to winners
        calc = round((((1 / winner_1) + (1 / winner_2)) * 100), 2)

        arbVal = None

        # Check whether arbitrage is valid or not and produce the beginning of response to user
        if calc > 100:
            arbVal = ':x: Arbitragem inválida! __NÃO APOSTAR__ :x:\n\n\tCálculo abaixo:\n\n'
        elif calc < 100:
            arbVal = ':white_check_mark: Arbitragem válida! :white_check_mark:\n\t\tCálculo abaixo:\n\n'
        else:
            await ctx.reply(':no_entry:  Arbitragem nula, não apostar :no_entry:')
            return

        # Reply to user if arbitrage is valid and which Site and Odds to bet
        await ctx.reply(f'{arbVal}Melhor % no Site A -> `{str(winner_1)}`\nMelhor % no Site B -> `{str(winner_2)}`\nArbitragem -> `{str(calc)}%`')

        # Calculate how much to bet on each odd if user decided a goal
        if c != 0 and bet == 0:
            calc_1 = round((c / winner_1), 2)
            calc_2 = round((c / winner_2), 2)
            invest = round((calc_1 + calc_2), 2)
            luc = round((c - invest), 2)

            await ctx.send(f'>> Apostar em `{str(winner_1)}%` o total de: __`{str(calc_1)}`__\n>> Apostar em `{str(winner_2)}%` o total de: __`{str(calc_2)}`__\n\nTotal investido para alcançar objetivo (`{str(c)}`): `{str(invest)}`\nLucro Total: `{str(luc)}`')
        
        # Calculate how much the profit would be betting on each winner
        elif c == 0 and bet != 0:
            calc_1 = round((winner_1 * bet) / 100, 2)
            calc_2 = round((winner_2 * bet) / 100, 2)

            await ctx.send(f'>> Apostando `{str(bet)}` o lucro em __`{str(winner_1)}%`__ será `{str(calc_1)}` reais.\n>> Apostando `{str(bet)}` reais  o lucro em __`{str(winner_2)}%`__ será `{str(calc_2)}` reais.')

    
    # Flip coin
    @commands.command(name = 'moeda', aliases = ['flipcoin', 'coin', 'coinflip', 'caracoroa', 'caraoucoroa'], help = 'Jogue a moeda rapidamente. Uso: %moeda')
    async def coin(self, ctx):
        a = random.random()

        if a < 0.50:
            return await ctx.reply('**Coroa!**')
        else:
            return await ctx.reply('**Cara!**')
    
    # Roll dices
    @commands.command(name = 'dados', aliases = ['dice', 'dices', 'dado', 'rolldice', 'rolar', 'rolardados', 'roll'], help = 'Role os dados rapidamente. Uso: %dados 1(num de 1 a 3 representando a quantidade de dados)')
    async def dice(self, ctx, *, diceNum = 1):
        if diceNum > 3: return await ctx.reply(f'Hoje só estamos rolando até 3 dados, **{random.choice(fraseMeio)}**.')
        
        await ctx.reply(f'Rolando {diceNum} dados...') if diceNum > 1 else await ctx.reply(f'Rolando dado...')

        async with ctx.message.channel.typing():
            for i in range (1, diceNum + 1):
                r = random.randint(1, 6)
                await ctx.reply(f'Dado __{i}__... **{r}**.')
    
    # Greater than or smaller than 6 faced dices
    @commands.command(name = 'dd', help = 'Role dados de mais ou menos de 6 faces rapidamente. Uso: %dd 1(num íntegro representando a quandidade de faces do dado)')
    async def dice(self, ctx, faces: int):

        await ctx.reply(f'Rolando dado DD de {faces} faces...')
        async with ctx.message.channel.typing():
            r = random.randint(1, faces)

            await ctx.reply(f'Resultado: **{r}**')

    # Ping Pong - Ping command
    @commands.command(name = 'ping', help = 'Ping, Pong')
    async def pingPong(self, ctx):
        lat = round(self.bot.latency * 1000)
        await ctx.reply(f'Pong!\n\n`Bot ping {lat} ms`')

    @commands.command(name = 'pong', help = 'Pong, Ping')
    async def pongPing(self, ctx):
        await ctx.reply('Ping!')


    # Google translate using googletranslator API -  XX deprecated due to incompatibility for hhtpx between youtubesearchpython (used in Music cog) and googletrans XX
    @commands.command(name = 'translate', aliases = ['traduzir'], help = 'Uso: %traduzir Sua Frase Aqui // LinguaDestino(Opcional - padrão PTBR)\nAcentuação importa.')
    async def translate(self, ctx, *, args = None):
        
        return await ctx.reply('Comando temporariamente indisponivel.')
        # # Usage of Googletrans api to translate portions of text to desired language
        # translator = Translator()

        # # If no text provided by user, return
        # if not args: return await ctx.reply(f'Como vou traduzir, se você não me passou um texto, **{random.choice(fraseMeio)}**?\nLembrando que a acentuação durante o comando importa!')

        # # Default declarations
        # text = args
        # lang = 'pt'

        # # If custom translation language desired
        # if '//' in args:
        #     args_p = args.split('//')
        #     text = args_p[0]
        #     lang_o = translator.translate(args_p[1])
        #     lang = lang_o.text

        # else:
        #     text = args

        # transText = translator.translate(text, dest = lang)

        # org_lang = transText.extra_data['original-language']

        # for i in range(len(languages)):
        #     if org_lang in languages[i]:
        #         org_lang = languages[i][1]

        # transConf = translator.detect(text)

        # embed = discord.Embed(title = f'Ta na mão sua tradução, **{random.choice(fraseMeio)}**:', description = '', colour = discord.Color.purple())
        # embed.add_field(name = 'Frase original:', value = text, inline = False)
        # embed.add_field(name = 'Lingua origem identificada:', value = org_lang.upper(), inline = False)
        # embed.add_field(name = 'Frase traduzida:', value = transText.text, inline = False)
        # embed.add_field(name = 'Lingua destino:', value = lang.upper(), inline = False)
        # embed.add_field(name = 'Percentual de certeza na detecção de lingua origem:', value = f'{round((transConf.confidence * 100), 2)}%', inline = False)
        # await ctx.send(ctx.message.author.mention)
        # await ctx.send(embed = embed)
        # await ctx.message.delete()

    
    # Retrieve large user's avatar image
    @commands.command(name = 'avatar', aliases = ['fotinha', 'fotinho'], help = 'Uso: %avatar @NomeDoUsuario\nO nome de usuário é opcional. Se não inseri-lo, o bot retornará seu próprio avatar num tamanho maior')
    async def avatar(self, ctx, member : discord.Member = None):

        # If requested user does not have an avatar
        if member.avatar.url == None:
            return await ctx.reply(f'Esse usuário não tem um avatar.')

        # If user did not specify another user to retrieve the avatar from, retrieve his own avatar
        if member == None:
            member = ctx.message.author
        
        url = member.avatar.url
        name = await ctx.bot.fetch_user(member.id)

        # Create embed to reply to user
        embed = discord.Embed(title = '', description = '')
        embed.set_author(name = name, icon_url = url)
        embed.set_image(url = url)
        embed.set_footer(text = f'Solicitado por {ctx.message.author}.')
        
        return await ctx.reply(embed = embed)

    
    # Timer command to remind user in X minutes of Y reason
    @commands.command(name = 'timer', aliases = ['lembrar', 'despertador', 'despertar'], help = 'Uso %timer # (Opcional colocar uma descrição para o timer).\nO tempo deve ser em minutos\nEx.: %timer 120 Lembrar de boostar o servidor!') 
    async def timer(self, ctx, minutes: int, *, reason=None):
        
        # Let user know we've received his request
        await ctx.message.add_reaction(emoji_id)
        resp = (f'Ok, **{random.choice(fraseMeio)}**, vou te lembrar em {minutes} minutos')

        # If a reason was given, append to response
        if reason != None:
            resp += f' de __"{reason}"__.'
        await ctx.reply(f'{resp}')

        # async sleep the requested amount of minutes
        await asyncio.sleep(minutes * 60)

        # Let user know the timer is done
        new_resp = f'Apenas para te lembrar que o timer finalizou, **{random.choice(fraseMeio)}**.'

        # If a reason was given, append to response
        if reason != None:
            new_resp += f' **Descrição**: "{reason}".'
        
        # Send response to user
        await ctx.reply(f'{new_resp}')

    # More elaborated arbitrage system considering more than 2 sources and more than 2 odd options (Ex.: win, draw, lose)
    @commands.command(name = 'arbitragem', aliases = ['aposta2'], help = f'{arbitragem}')
    async def aposta_arbitragem(self, ctx):
        
        # Command will only be available from FORUMs in order to keep betting simulation history
        if ctx.channel.category.name != '--FORUMS--': 
            return await ctx.reply(f'Faz o seguinte, **{random.choice(fraseMeio)}**... Entra no fórum ali na esquerda chamado "__APOSTAS__". Se não tiver um Tópico aberto com seu nome, abre um e me chama de lá.\nSe já tiver, é só entrar no seu tópico e me chamar também.')
        
        try:
            member = ctx.author

            embed = discord.Embed(title = f'__APOSTA POR ARBITRAGEM__ - {datetime.now().strftime("%d/%m - %H:%M:%S")}', description = '```json\nQuantas opções de arbitragem vamos analisar?```\n\n**Ex.:** Ganhar/Empate/Perder (**__3__**)', colour = 0x01ffff)
            embed.set_footer(text = 'Responda todas as perguntas em números.')

            # Default response to values not inputted correctly
            incomp = f'O mínimo de Sites (fontes) e Odds para o cálculo de arbitragem é **__2__**.\n\nVou explicar:\n\n{arbitragem}\n\nApostando em somente um Site *a casa sempre sai ganhando*.\n\nDa uma ohada no video abaixo pra mais detalhes: Arbitrage Betting Explained -> https://www.youtube.com/watch?v=TGinzvSDayU&t=387s.'

            orig = await ctx.reply(embed = embed)
            odds = await self.bot.wait_for('message', check = lambda message: message.author == member, timeout = 60.0)
            try:
                odds.content = int(odds.content)
            except:
                return await ctx.reply(incomp)

            if int(odds.content) == 1: return await ctx.reply(incomp)
            
            embed.description = '```diff\nQuantos sites analisaremos?\nEx.: Site 1 e Site 2 (2)```---'
            embed.add_field(name = f'Opções de Arbitragem: `{odds.content}`', value = '---')

            # Delete last sent user message
            await discord.Message.delete(odds) 
            
            # Send new embed
            await discord.Message.edit(orig, embed = embed) 

            sites = await self.bot.wait_for('message', check = lambda message: message.author == member, timeout = 60.0)
            
            if int(sites.content) == 1: return await ctx.reply(incomp)

            embed.add_field(name = f'Sites: `{sites.content}`', value = '---')

            def_odds = list()

            # Delete last sent user message
            await discord.Message.delete(sites) 
            
            counter = 1

            # Gather odds from user
            for site in range(int(sites.content)):
                for odd in range(int(odds.content)):
                    while True:
                        try:
                            if counter == 1: embed.add_field(name = '\u200b', value = '\u200b', inline = False) 

                            embed.description = f'```diff\n-> Insira a odd {odd + 1} do Site {site + 1} -- Ex.: {round(random.uniform(1.5, 3.5), 2)} <-```---'
                            
                            # Send new embed
                            await discord.Message.edit(orig, embed = embed) 

                            message = await self.bot.wait_for('message', check = lambda message: message.author == member, timeout = 60.0)
                            
                            def_odds.append({'site':site, 'odd':float(message.content)})

                            embed.add_field(name = f'Site {site + 1} - Odd {odd + 1}:', value = f'`{float(message.content)}`')
                            await discord.Message.delete(message)
                            counter += 1
                            break
                        
                        # If error
                        except ValueError as error:
                            await discord.Message.delete(message)
                            error_reply = await discord.Message.edit(orig, embed = embed, content = f':bangbang: Acho que você inseriu o número errado. Você realmente quis dizer {message.content}? :bangbang:\n')
                            
                            await discord.Message.delete(error_reply, delay = 60)

                embed.add_field(name = '\u200b', value = '\u200b', inline = False)
            
            # Edit last sent message
            await discord.Message.edit(orig, embed = embed)
            await ctx.reply(f'Vou seguir com minha mágica e já retorno o resultado.')
            await ctx.trigger_typing()
            
            embed.remove_footer()

            winners = list()
            
            # For each odd
            for odd in range(int(odds.content)):
                curr_odd = odd
                
                # For next odd in defined odds decide the winner
                for next_odd in range(odd + int(odds.content), len(def_odds), int(odds.content)):
                    if len(winners) <= odd: 
                        winners.append(def_odds[curr_odd])
                    if winners[curr_odd]['odd'] < def_odds[next_odd]['odd']:
                        winners[curr_odd] = def_odds[next_odd]


        # For each winner, apply arbitrage algorithm

            calc = 0

            for winner in range(len(winners)):
                calc += (1/winners[winner]['odd'])
            
            # Round results
            calc = round(calc * 100, 2)

            arVal = None

            # Check whether arbitrage is valid or not and produce the beginning of response to user
            if calc > 100:
                tit = ':x: Arbitragem inválida! :x:'
                desc = '```json\n\t\t>> NÃO APOSTAR <<\n\nCálculo abaixo:\n\n'
            elif calc < 100:
                tit = ':white_check_mark: Arbitragem válida! :white_check_mark:'
                desc = '```json\n\t\tPODE APOSTAR\n\nCálculo abaixo:\n\n'
            else:
                tit = ':no_entry:  Arbitragem nula, não apostar :no_entry:'
            
            final_embed = discord.Embed(title = tit, description = f'{desc}', color = discord.Colour.green())

            for i in reversed(range(len(winners))):
                final_embed.description += f'Melhor % no Site {winners[i]["site"] + 1} -> {str(winners[i]["odd"])} %\n'
            final_embed.description += f'\nArbitragem -> {str(calc)}```'

            calcs = list()

            # Ask user what is the objective to achieve
            bet_msg = await ctx.reply('Qual objetivo quer alcançar? (__Número sem pontos ou vírgulas__)')

            aposta = await self.bot.wait_for('message', check = lambda message: message.author == member, timeout = 60.0)
            
            invest = 0
            
            for i in range(int(odds.content)):
                temp = round((int(aposta.content) / winners[i]["odd"]), 2)
                calcs.append({winners[i]['site']:winners[i]['odd'], f'calc_{i}':temp})
                invest += temp
            invest = round(invest, 2)
            luc = round((int(aposta.content) - invest), 2)

            f = discord.Embed(title = '__APOSTA POR ARBITRAGEM__', description = '```json\nCálculo por objetivo.\n\n', colour = discord.Colour.green())

            for i in reversed(calcs):
                counter = 0
                for key, value in i.items():
                    if counter == 0: f.description += f'>> Apostar em {value} % o total de: '
                    else: f.description += f'{value}\n'
                    counter += 1

            f.description += f'\n\nTotal investido para alcançar objetivo de ({int(aposta.content)}): {invest}\nLucro Total: {luc}```'
        
            # Reply to user if arbitrage is valid and which Site and Odds to bet
            await discord.Message.delete(aposta)
            await ctx.send(embed = final_embed)
            await ctx.send(embed = f)
            
        except:
            pass



# Define setup function for Cog
def setup(bot):
    bot.add_cog(General(bot))