# Gerador_Certificados

<h1> Comandos </h1>
docker compose down --rmi all -v </br>
docker-compose up


<h1>JSON</h1>
{</br>
    "nome": "Osvaldo", </br>
    "nacionalidade": "Malasio",</br>
    "estado": "XA",</br>
    "data_nascimento": "2000-01-10",</br>
    "documento": "2222-00",</br>
    "data_conclusao": "2024-08-11",</br>
    "curso": "JAVA Starter",</br>
    "carga_horaria": 12,</br>
    "data_emissao": "2024-11-02",</br>
    "nome_assinatura": "Marcos Sem Minie",</br>
    "cargo": "Doutor",</br>
    "caminhoPDF": ""</br>
}

</br>
Possiveis Erros e suas Correções:
ERRO GERADO DURANTE A INICIALIZAÇÃO DO CONTAINER DE certificado_worker em algumas maquinas: </br>
certificado_worker  | /usr/bin/env: ‘bash\r’: No such file or directory </br>
certificado_worker  | /usr/bin/env: use -[v]S to pass options in shebang lines </br>
</br>
Correção. Executar o seguinte comando no GIT BASH no diretorio ../wait-script </br>
Comando:  sed -i 's/\r//' wait-for-it.sh

