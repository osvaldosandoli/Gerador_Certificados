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
}</br>


Possiveis Erros e suas Correções: </br>
<h3>ERRO GERADO DURANTE A INICIALIZAÇÃO DO CONTAINER DE certificado_worker em algumas maquinas: </h3></br>
certificado_worker  | /usr/bin/env: ‘bash\r’: No such file or directory </br>
certificado_worker  | /usr/bin/env: use -[v]S to pass options in shebang lines </br>
</br>
Correção. Executar o seguinte comando no GIT BASH no diretorio ../wait-script </br>
Comando:  sed -i 's/\r//' wait-for-it.sh

</br>
<h3>Erro em Mac: Gerado na execução do comando docker-compoose up </h3>
</br>
services.mysql Additional property plataform is not allowed
</br>
Correcao: No arquivo docker-compose.yml alterar o servico do MySQL para: </br>
mysql: </br>
    image: mysql:8 </br>
    container_name: mysql </br>
    environment: </br>
      MYSQL_ROOT_PASSWORD: senha </br>
      MYSQL_DATABASE: certificados_db </br>
    ports: </br>
      - "3306:3306" </br>
    volumes: </br>
      - ./Database/ddl.sql:/docker-entrypoint-initdb.d/ddl.sql </br>
    networks: </br>
      - certificado_network </br>
    platform: linux/arm64/v8 </br>
    </br>



