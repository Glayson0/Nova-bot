def escape_msg(output: str) -> str:
    """Escape special chars:  . ! | ( ) - _ + #"""
    for char in (".", "!", "|", "(", ")", "-", "_", "+", "#", "<", ">"):
        output = output.replace(char, rf"\{char}")

    return output


def format_msg(msg: str, formatting_marker: str) -> str:
    """Formats the message with the formatting marker.
    Example:
        msg = "Hello, World!"
        formatting_marker = "*"

        return: "*Hello, World!*" (bold format)
    """
    return formatting_marker + msg + formatting_marker


START_SHORT_TEXT = '*👋 Olá, {first_name}\! Como vai?\nSeja bem\-vindo\!\n*'

START_TEXT = escape_msg("""
*Eu sou a Nova, um bot criado por alunos da Unicamp!*

Estou aqui para facilitar o acesso a informações sobre os *ônibus* da moradia e os *restaurantes* da Unicamp de maneira rápida e prática.

Clique no botão abaixo ou digite /home para conhecer os comandos principais disponíveis.
""")


MENU_SHORT_TEXT = escape_msg('Entendido! Aqui está uma lista com os comandos principais:')

MENU_TEXT = escape_msg("""
📋 *Comandos Principais*:

🚌 *Ônibus da Moradia*:
- /onibus: Comandos relacionados aos ônibus da moradia.
- /oProx: Próximos X ônibus de ida e volta.

🍽️ *Restaurantes*:
- /bandejao: Comandos relacionados aos restaurantes.
- /bCardapio: Cardápio de almoço e jantar.

🔍 *Outros Comandos*:
- /tudo: Lista todos os comandos disponíveis.

Se precisar de mais ajuda, não hesite em me chamar! Estou aqui para ajudar você a aproveitar ao máximo os serviços da Unicamp.

💡 *Dica*: Clique nos comandos acima para executá-los diretamente!
""")


BUS_SHORT_TEXT = escape_msg('Okay! Aqui estão os comandos para os ônibus da moradia:')

BUS_TEXT = escape_msg("""
🚌 *Ônibus da Moradia*:
- /onibus: Comandos relacionados aos ônibus da moradia.
- /oProx (número): Próximos X ônibus de ida e volta.
- /oFoto: Imagem oficial com todos os horários de ônibus.
- /oTodos: Todos os horários de ônibus do dia.
""")


BANDEJAO_SHORT_TEXT = escape_msg('Okay! Aqui estão os comandos relacionados ao bandejão:')

BANDEJAO_TEXT = escape_msg("""
🍽️ *Comandos de Restaurantes*:
Geral:
- /bHoras: Horários de funcionamento dos três restaurantes.
- /bCardapio: Cardápio de almoço e jantar.
- /bJaPode: Refeições sendo servidas no momento.

Restaurantes Específicos:
- /ru: Informações sobre o Restaurante Universitário (RU).
- /rs: Informações sobre o Restaurante da Saturnino (RS).
- /ra: Informações sobre o Restaurante da Administração (RA).
""")


UNKNOWN_SHORT_TEXT = escape_msg('Hmmm, eu não conheço esse comando.')

UNKNOWN_TEXT = escape_msg('Experimente usar o comando /home para ver uma lista com os principais comandos.')

ERROR_MESSAGE = escape_msg('Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.')


ALL_COMMANDS_TEXT = escape_msg("""
🚌 *Ônibus da Moradia*:
- /onibus: Comandos relacionados aos ônibus da moradia.
- /oProx (número): Próximos X ônibus de ida e volta.
- /oFoto: Imagem oficial com todos os horários de ônibus.
- /oTodos: Todos os horários de ônibus do dia.
                          
🍽️ *Comandos de Restaurantes*:
Geral:
- /bHoras: Horários de funcionamento dos três restaurantes.
- /bCardapio (número): Cardápio de almoço e jantar de um dos menus.
  0 (padrão) -> ambos, 1 -> Tradicional, 2 -> Vegano
- /bJaPode: Refeições sendo servidas no momento.

Restaurantes Específicos:
- /ru: Informações sobre o Restaurante Universitário (RU).
- /rs: Informações sobre o Restaurante da Saturnino (RS).
- /ra: Informações sobre o Restaurante da Administração (RA).
                          
🔍 *Outros Comandos*:
- /start: Mensagem de boas-vindas do bot.
- /tudo: Lista todos os comandos disponíveis.
""")