import discord
from discord.ext import commands
from collections import OrderedDict

class Math:
    '''
    Just some math stuff.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def calc(self, ctx):
        '''
        Calculator!
        '''
        message = message_string_parser(ctx.message.content)
        calc(message)

def setup(bot):
    bot.add_cog(Math(bot))

def message_string_parser(message):
    return(message[message.find(' ')+1:])

#reverse order of operations
#I didn't have to use an OrderedDict, but it's cute
operations = OrderedDict([
    ("+", lambda x, y: x + y),
    ("-", lambda x, y: x - y),
    ("/", lambda x, y: x / y),
    ("*", lambda x, y: x * y),
    ("^", lambda x, y: x ^ y)
])

symbols = operations.keys()

def lex(expr):
    """
    seperates numbers from symbols, recursively nests parens
    """
    tokens = []
    while expr:
        char, *expr = expr
        #char is equal to the first charecter of the expression, expr is equal
        #to the rest of it
        if char == "#":
            #the rest of the line is a comment
            break
        if char == "(":
            try:
                paren, expr = lex(expr)
                tokens.append(paren)
                #expr is what's after the end of the paren, we'll just continue
                #lexing after that''
            except ValueError:
                raise Exception("paren mismatch")
        elif char == ")":
            return tokens, expr
            #returns the tokens leading up to the to the paren and the rest of
            #the expression after it
        elif char.isdigit() or char == ".":
            #number
            try:
                if tokens[-1] in symbols:
                    tokens.append(char) #start a new num
                elif type(tokens[-1]) is list:
                    raise Exception("parens cannot be followed by numbers")
                    #no support for 5(1+1) yet
                else:
                    tokens[-1] += char #add to last num
            except IndexError:
                #if tokens is empty
                tokens.append(char) #start first num
        elif char in symbols:
            tokens.append(char)
        elif char.isspace():
            pass
        else:
            raise Exception("invalid charecter: " + char)
    return tokens

def evaluate(tokens):
    for symbol, func in operations.items():
        #try to find an operation to eval in order
        try:
            pos = tokens.index(symbol)
            #split the tokens by the operation and eval that
            leftTerm = evaluate(tokens[:pos])
            rightTerm = evaluate(tokens[pos + 1:])
            return func(leftTerm, rightTerm)
            #incidentially, return immediatly breaks all loops within the
            # function
        except ValueError:
            pass
            #index raises ValueError when it's not found
    if len(tokens) is 1:
        try:
            #it must be a number
            return float(tokens[0])
        except TypeError:
            #if it's not a number
            return evaluate(tokens[0])
    else:
        raise Exception("bad expression: " + tokens)

def calc(expr):
    return evaluate(lex(expr))
