"""
Este script é desenvolvido pela Next Level Software Studio.
Ele serve para automaticamente organizar as use flags, de um sistema que use o Portage. 
"""


from pathlib import Path
import re, sys, os
if os.getuid() != 0:
    print("Este script precisa ser executado como root.")
    sys.exit(1)

rule1 = r"^([^./\\, ]+)\/([^./\\, ]+) ([a-zA-Z0-9_+\-]+(?: (?:-[a-zA-Z0-9_+\-]+|[a-zA-Z0-9_\-]+[a-zA-Z0-9_+\-]*))*)$" # LINHA CORRETA
rule2 = r"^([^./\\, ]+)\/([^./\\, ]+) " #correto sem use flags


    for j in Path("/etc/portage/package.use").glob("*"):
        print(f"Processando o ficheiro: {j}")
        with open(j, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip() or line.strip().startswith("#"):
                    continue  # Ignora linhas vazias ou comentários.

                print(f"Processando a linha: {line}")
                if re.fullmatch(pattern=rule1, string=line.strip):
                    processado = line.split(" ", maxsplit=1)
                    use = processado[1].strip()
                    classe = processado[0].split("/", maxsplit=1)[0]
                    package = processado[0].split("/", maxsplit=1)[1]

                elif re.fullmatch(pattern=rule2, string=line.strip()):
                    print(f'A linha "{line.strip()}", do ficheiro "{j}" não contém flags de USE. Ignorando.')
                    continue  # Ignora linhas sem use flags
                global FILEPATH
                FILEPATH = f"/etc/portage/package.use/{classe}/{package}"

                if Path(FILEPATH).exists() and Path(FILEPATH).is_file(): # se não for pasta e sim um ficheiro, valida se tem sintaxe de use correta para organizar
                    with open(FILEPATH, 'r', encoding='utf-8') as f2:
                        lines = f2.readlines() #carrega todas as lnhas do ficheiro numa lista
                    for k in lines:
                        if k.strip().startswith("#") or k.strip() == "":
                            continue  # Ignora linhas de comentário ou em branco
                    
                        elif not re.fullmatch(pattern=rule1, string=k.strip()):
                            print(f'Erro de sintaxe no ficheiro: {FILEPATH}.')
                            print(f'A linha "{k.strip()}" não corresponde à regra esperada.')
                            print(f'')
                            pergunta = int(input('Escolha uma opção:\n[1] Saltar a linha,\n[2] Sair do programa: '))
                            match pergunta:
                                case 1:
                                    print("Saltando linha.")
                                    continue
                                case 2:
                                    print("Saindo do programa.")
                                    sys.exit(0)
                        elif re.fullmatch(pattern=rule1, string=k.strip()):
                            processado = line.split(" ", maxsplit=1)
                            use = processado[1].strip()
                            classe = processado[0].split("/", maxsplit=1)[0]
                            package = processado[0].split("/", maxsplit=1)[1]
                            with open(FILEPATH, "r") as oi:
                                oi
                        else:
                            print("Algo correu mal, recomendação: verifique manualmente os ficheiros.")

                Path(FILEPATH).parent.mkdir(parents=True, exist_ok=True)
                print(f"Processando o pacote: {classe}/{package} com use: {use}")
                texto_a_escrever = f"{classe}/{package} {use}"
                
                try:
                    with open(FILEPATH, 'r', encoding='utf-8') as f2:
                        existing_content = f2.read().strip()
                except FileNotFoundError:
                    existing_content = ""
                
                if existing_content != texto_a_escrever:
                    with open(FILEPATH, 'w', encoding='utf-8') as f2:
                        print(f"Escrevendo no ficheiro: {FILEPATH}: {use}")
                        f2.write(f"{texto_a_escrever}\n")