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
    

start_text = escape_msg(f"""
*Eu sou a Nova, um bot criado por alunos da Unicamp!*

Estou aqui para te ajudar a obter informações sobre os ônibus da moradia e os restaurantes da Unicamp de forma rápida e fácil.

Clique no botão abaixo ou digite /help para conhecer alguns dos comandos que você pode utilizar.
""")

help_text = escape_msg("""
Aqui estão os comandos que você pode usar para interagir comigo:

🚍 *Ônibus da Moradia*:
- /onibus: Veja todos os comandos disponíveis para os ônibus da moradia.

🍽️ *Restaurantes*:
- /bandejao: Veja todos os comandos disponíveis para os restaurantes.

📋 *Outros Comandos*:
- /tudo: Liste todos os comandos disponíveis.

Se precisar de mais ajuda, não hesite em me chamar! Estou aqui para ajudar você a aproveitar ao máximo os serviços da Unicamp.

*Dica*: Você pode clicar nos comandos acima para executá-los diretamente!
""")

onibus_text = escape_msg("""
🚍 *Ônibus da Moradia*:
- /onibus: Veja todos os comandos disponíveis para os ônibus da moradia.
- /oProx (número): Veja os próximos X ônibus de ida e de volta.
- /oFoto: Veja a imagem oficial todos os horários de ônibus.
- /oTodos: Veja todos os horários de ônibus do dia.
""")

bandejao_text = escape_msg("""
🍽️ *Comandos de Restaurantes*:
Geral:
- /bHoras: Veja os horários de funcionamento dos três restaurantes.
- /bCardapio: Veja o cardápio de almoço e jantar.
- /bJaPode: Veja quais refeições estão sendo servidas no momento.

Restaurantes Específicos:
- /ru: Informações sobre o Restaurante Universitário (RU).
- /rs: Informações sobre o Restaurante da Saturnino (RS).
- /ra: Informações sobre o Restaurante da Administração (RA).
""")

cardapio_text = escape_msg("""
🍽️ *Comandos de Cardápio*:
- /bTradicional: Veja o cardápio tradicional.
- /bVegano: Veja o cardápio vegano.
""")