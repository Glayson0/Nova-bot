def escape_msg(output: str) -> str:
    """Escape special chars:  . ! | ( ) - _ + #"""
    for char in (".", "!", "|", "(", ")", "-", "_", "+", "#"):
        output = output.replace(char, rf"\{char}")

    return output

start_text = f"""
Eu me chamo Nova e sou um bot criado por alunos da Unicamp\!

Meu objetivo é fornecer informações dos ônibus da moradia e dos restaurantes da Unicamp de forma rápida e fácil\.

Clique no botão abaixo ou digite /help para conhecer alguns dos comandos que você pode utilizar\.
"""
help_text = """
Esses são os principais comandos para você usar\. Com eles, você consegue listar os comandos
para cada área que você deseja\.

\- /onibus: Ver comandos para os ônibus da moradia

\- /bandejao: Ver os comandos para o bandejao

\- /tudo: Listar todos os comandos
"""
onibus_text = """
\- /oProx: Ver os próximos 2 ônibus de ida e de volta

\- /oTodos: Ver foto com todos os horários de ônibus

\- /oTodosIda: Ver todos os horários de ônibus de IDA do dia \(Moradia \-\> Unicamp\)

\- /oTodosVolta: Ver todos os horários de ônibus de VOLTA dia \(Unicamp \-\> Moradia\)
"""
bandejao_text = """
Geral
\- /bHoras: Ver os horários dos três restaurantes

\- /bCardapio: Ver o cardápio de almoço e jantar

\- /bJaPode: Ver refeições em andamento

Restaurantes
\- /ru: Ver informações do RU

\- /rs: Ver informações do RS

\- /ra: Ver informações do RA
"""
cardapio_text = """
\- /bTradicional: Cardápio tradicional

\- /bVegano: Cardápio vegano
"""