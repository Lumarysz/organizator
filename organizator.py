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

if usedir.exists() and usedir.is_dir():
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

    itens = [lista[i][0] for i in lista]
    vistos = set()
    repetidos = set()
    for y in itens:
        if y in vistos:
            repetidos.add(y)
        else:
            vistos.add(y)
    nao_repetidos = list(vistos - repetidos)
    nao_repetidos_final = [tuple(h, lista[h]) for h in nao_repetidos]

    hello = {}

    for p in repetidos:
        for a, b in lista: # use = b, pacote = a
            if a == p:
                if a in hello:
                    hello[a] = hello[a] + b # valor antigo + o atual
                elif a not in hello:
                    hello[a] = b
    
    clean_list = []

    for v in hello:
        g = hello.get(v)
        clean_list.append((v, g))
    clean_list = clean_list + nao_repetidos_final

    shutil.rmtree(usedir)
    usedir.mkdir(parents=True, exist_ok=True)

    for k in clean_list:
        filepath = Path(f"/etc/portage/package.use/{k[1]}/{k[2]}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(file=filepath, mode='w', encoding='utf-8') as f:
            f.write(f"{clean_list[k][1]} {clean_list[k][2]}")