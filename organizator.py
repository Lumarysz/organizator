from pathlib import Path
import re, sys, os
if os.getuid() != 0:
    print("Este script precisa ser executado como root.")
    sys.exit(1)
if Path("/etc/portage/package.use").is_dir():
    listacompleta = []

    for i in Path("/etc/portage/package.use").glob("*"):
        if (i.is_file()) and (i.suffixes == []):
            listacompleta.append(i)

    for j in listacompleta:
        print(f"Processando o ficheiro: {j}")
        with open(j, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip() or line.strip().startswith("#"):
                    continue  # Ignora linhas vazias ou comentários.

                print(f"Processando a linha: {line}")
                if (" " in line) and ("/" in line):
                    processado = line.split(" ", maxsplit=1)
                    use = processado[1].strip()
                    classe = processado[0].split("/", maxsplit=1)[0]
                    package = processado[0].split("/", maxsplit=1)[1]

                elif (("/" in line) and (" " not in line)) or (("/" in line) and (" " not in line)):
                    
                

                filepath = f"/etc/portage/package.use/{classe}/{package}"


                if Path(filepath).exists() and Path(filepath).is_file(): # se não for pasta e sim um ficheiro, valida se tem sintaxe de use correta para organizar
                    rule = r"^([^./\\, ]+)\/([^./\\, ]+) ([a-zA-Z0-9_+\-]+(?: (?:-[a-zA-Z0-9_+\-]+|[a-zA-Z0-9_\-]+[a-zA-Z0-9_+\-]*))*)$"

                    with open(filepath, 'r', encoding='utf-8') as f2:
                        lines = f2.readlines()
                    for k in lines:
                        if k.strip().startswith("#") or k.strip() == "":
                            continue  # Ignora linhas de comentário
                    
                        elif re.fullmatch(pattern=rule, string=k.strip()):
                            count = 0
                            while True:
                                if Path(f"{filepath}{count}").exists() is False:
                                    Path(filepath).replace(target=f"{filepath}{count}")
                                    listacompleta.append(Path(f"{filepath}{count}"))
                                    break
                                else:
                                    count += 1
                                    continue

                        elif not re.fullmatch(pattern=rule, string=k.strip()):
                            print(f'Erro de sintaxe no ficheiro: {filepath}.')
                            print(f'A linha "{k.strip()}" não corresponde à regra esperada.')
                            pergunta = int(input('Escolha uma opção: [1] Eliminar, [2] Sair: '))
                            match pergunta:
                                case 1:
                                    Path(filepath).unlink(missing_ok=True)
                                    print(f"Ficheiro {filepath} foi removido.")
                                case 2:
                                    print("Saindo do programa.")
                                    sys.exit(0)
                                
                        else:
                            print("Algo correu mal, recomendação: verifique manualmente os ficheiros.")

                Path(filepath).parent.mkdir(parents=True, exist_ok=True)
                print(f"Processando o pacote: {classe}/{package} com use: {use}")
                texto_a_escrever = f"{classe}/{package} {use}"
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f2:
                        existing_content = f2.read().strip()
                except FileNotFoundError:
                    existing_content = ""
                
                if existing_content != texto_a_escrever:
                    with open(filepath, 'w', encoding='utf-8') as f2:
                        print(f"Escrevendo no ficheiro: {filepath}: {use}")
                        f2.write(f"{texto_a_escrever}\n")