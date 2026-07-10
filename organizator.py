"""
Este script é desenvolvido pela Next Level Software Studio.
Ele serve para automaticamente organizar as use flags, de um sistema que use o Portage. 
"""


from pathlib import Path
import re, sys, os, shutil
if os.getuid() != 0:
    print("Este script precisa ser executado como root.")
    sys.exit(1)

rule1 = r"^([^./\\, ]+)\/([^./\\, ]+) ([a-zA-Z0-9_+\-]+(?: (?:-[a-zA-Z0-9_+\-]+|[a-zA-Z0-9_\-]+[a-zA-Z0-9_+\-]*))*)$" # LINHA CORRETA
rule2 = r"^([^./\\, ]+)\/([^./\\, ]+) " #correto sem use flags
lista = []
usedir = Path("/etc/portage/package.use")

if usedir.exists and usedir.is_dir():
    for j in usedir.glob("*"):
        print(f"Processando o ficheiro: {j}")
        with open(j, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip() or line.strip().startswith("#"):
                    continue  # Ignora linhas vazias ou comentários.

                elif re.fullmatch(pattern=rule2, string=line.strip()):
                    print(f'A linha "{line.strip()}", do ficheiro "{j}" não contém flags de USE. Ignorando.')
                    continue  # Ignora linhas sem use flags

                elif re.fullmatch(pattern=rule1, string=line.strip()):
                    processado = line.split(" ", maxsplit=1)
                    use = processado[1].strip()
                    package = processado[0]

                    lista.append((package, use))

    itens = [lista[i][1] for i in lista]
    vistos = set()
    repetidos = set()
    for y in itens:
        if y in vistos:
            repetidos.add(y)
        else:
            vistos.add(y)

    for p in repetidos:
        for 

    shutil.rmtree(usedir)
    usedir.mkdir(parents=True, exist_ok=True)

    for k in lista:
        filepath = Path(f"/etc/portage/package.use/{k}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(file=filepath) as f:
            f.write(f"{lista[k][1]} {lista[k][2]}")