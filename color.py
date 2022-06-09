#COLORS
#=====================
pref = "\033["
reset = f"{pref}0m"
colors ={
    "black" : "30m",
    "red" : "31m",
    "green" : "32m",
    "yellow" : "33m",
    "blue" : "34m",
    "magenta" : "35m",
    "cyan" : "36m",
    "white" :"37m"
}
# Alternative to print, uses white color by default but accepts any color 
# from the Colors class. Name it as you like.
def coloredText(text, color=colors["white"], is_bold=False):
    print(f'{pref}{1 if is_bold else 0};{colors[color]}' + text + reset)


def get_coloredText(text, color=colors["white"], is_bold=False):
    return f'{pref}{1 if is_bold else 0};{colors[color]} {text} {reset}'
