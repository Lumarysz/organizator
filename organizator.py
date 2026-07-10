"""
Este script é desenvolvido pela Next Level Software Studio.
Ele serve para automaticamente organizar as use flags, de um sistema que use o Portage. 
"""

from pathlib import Path
import re, sys, os, shutil

if os.getuid() != 0:
    print("Este script precisa ser executado como root.")
    sys.exit(1)

# O regex original foi mantido igual
rule1 = r"^([^./\\, ]+)\/([^./\\, ]+) ([a-zA-Z0-9_+\-]+(?: (?:-[a-zA-Z0-9_+\-]+|[a-zA-Z0-9_\-]+[a-zA-Z0-9_+\-]*))*)$" 
rule2 = r"^([^./\\, ]+)\/([^./\\, ]+)$" 
lista = []
usedir = Path("/etc/portage/package.use/want")

if usedir.exists() and usedir.is_dir():
    print(f'"{usedir}" exists.')
    for j in usedir.glob("*"):
        if j.is_file(): # Mantido o seu check de ficheiro
            print(f"Processando o ficheiro: {j}")
            with open(j, "r", encoding="utf-8") as f:
                for line in f:
                    line_clean = line.strip()
                    if not line_clean or line_clean.startswith("#"):
                        print("Saltando linha.")
                        continue  

                    elif re.fullmatch(pattern=rule2, string=line_clean):
                        print(f'A linha "{line_clean}", do ficheiro "{j}" não contém flags de USE. Ignorando.')
                        print('Saltando linha.')
                        continue  

                    elif re.fullmatch(pattern=rule1, string=line_clean):
                        processado = line_clean.split(maxsplit=1)

                        package = processado[0]
                        print(f'Pacote: {package}.')
                        use = processado[1].strip()
                        print(f'Use flags: {use}.')

                        lista.append((package, use))
                        
        elif j.is_file() is False:
            continue

    itens = [item[0] for item in lista]
    vistos = set()
    repetidos = set()
    for y in itens:
        if y in vistos:
            repetidos.add(y)
        else:
            vistos.add(y)
            
    print(f'Repetidos: {repetidos}')
    nao_repetidos = list(vistos - repetidos)
    nao_repetidos_final = [par for par in lista if par[0] in nao_repetidos]
    print(f'Não repetidos: {nao_repetidos_final}')

    hello = {}

    for p in repetidos:
        for a, b in lista: 
            if a == p:
                if a in hello:
                    hello[a] = hello[a].strip() + " " + b.strip() 
                elif a not in hello:
                    hello[a] = b
    
    clean_list = []

    for v in hello:
        g = hello.get(v)
        clean_list.append((v, g))
    clean_list = clean_list + nao_repetidos_final

    print(f'Apagando e recriando pasta: {usedir}')
    shutil.rmtree(usedir)
    usedir.mkdir(parents=True, exist_ok=True)

    for k in clean_list:
        filepath = Path(f"/etc/portage/package.use/{k[0]}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(file=filepath, mode='w', encoding='utf-8') as f:
            flags_limpas = " ".join(k[1].split())
            escrever = f"{k[0]} {flags_limpas}\n"
            f.write(escrever)
            print(f'Editando {filepath}, escrevendo "{escrever.strip()}".')