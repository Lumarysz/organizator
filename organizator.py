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