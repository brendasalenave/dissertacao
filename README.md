# Extração de Indicadores Estruturados e Não-Estruturados e sua Aplicação no Processo de Recomendação de Recursos Urbanos

Código-fonte desenvolvido para implementação da parte prática referente dissertação apresentada como requisito parcial
para a obtenção do grau de Mestre em Ciência da Computação.

#### Execução
Para a correta execução do código, devem ser instalas as bibliotecas auxiliares utilizadas no desenvolvimento. A instalação destas pode ser feita através do seguinte comando:

```sh
$ pip3 install -r requirements.txt
```

Execução da aplicação via terminal:

```sh
$ python3 main.py
```

| Arquivo | Descrição |
| ------ | ------ |
| [main][mainfile] | arquivo principal onde realizam-se as chamadas aos demais métodos que compõe o *pipeline* de execução|
| [webscraping][webscrapingfile] | *script* desenvolvido de modo *ad-hoc* para coleta de dados provenientes da fonte utilizada (Foursquare)|
| [preprocess][preprocessfile] | *script* de pré-processamento dos dados |
| [process][processfile] | *script* de processamento dos dados a serem analisados |
| [analyser][analyserfile] | *script* desenvolvido para análise de dados do *dataset* de modo a extrair indicadores a serem utilizados no processo de recomendação |
| [recommendation][recommendationfile] | *script* onde são aplicados os algoritmos de recomendação utilizando a biblioteca [surprise][surpriselib] |
| [ontology][ontologyfile] | *script* de população automazida da [ontologia][onto] a partir do conjunto de dados atual|


***


# Extraction of Structured and Non-Structured Indicators and their Application in the Urban Resources Recommendation Process

Source code developed for implementation of the practical part referring to the dissertation presented as a partial requirement to obtain a Master's degree in Computer Science.

#### Execution
For the correct execution of the code, the auxiliary libraries used in the development must be installed. The installation of these can be done through the following command:

```sh
$ pip3 install -r requirements.txt
```

Execution of the application via the terminal:

```sh
$ python3 main.py
```

| File | Description |
| ------ | ------ |
| [main][mainfile] | the main file where the invocationcalls to the other methods that compose the execution pipeline are made|
| [webscraping][webscrapingfile] | script developed ad-hoc mode for collecting data from the used data source (Foursquare) |
| [preprocess][preprocessfile] | preprocessing data script |
| [process][processfile] |  script for processing the data to be analyzed |
| [analyser][analyserfile] | script developed for data analysis of dataset in order to extract indicators to be used in the recommendation process |
| [recommendation][recommendationfile] |  script where the recommendation algorithms are applied using the [surprise][surpriselib] library |
| [ontology][ontologyfile] | script for automated population of the [ontology] [onto] from the current data set|


[mainfile]: <https://github.com/brendasalenave/dissertacao/blob/master/main.py>
[webscrapingfile]: <https://github.com/brendasalenave/dissertacao/blob/master/webscraping.py>
[preprocessfile]: <https://github.com/brendasalenave/dissertacao/blob/master/preprocess.py>
[processfile]: <https://github.com/brendasalenave/dissertacao/blob/master/process.py>
[analyserfile]: <https://github.com/brendasalenave/dissertacao/blob/master/analyser.py>
[recommendationfile]: <https://github.com/brendasalenave/dissertacao/blob/master/recommendation.py>
[ontologyfile]: <https://github.com/brendasalenave/dissertacao/blob/master/ontology.py>
[onto]: <https://github.com/brendasalenave/dissertacao/tree/master/ontology>
[surpriselib]: <http://surpriselib.com>

