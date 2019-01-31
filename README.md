# Extração de Indicadores Estruturados e Não-Estruturados e sua Aplicação no Processo de Recomendação de Recursos Urbanos

Código-fonte desenvolvido para implementação da parte prática referente dissertação apresentada como requisito parcial
para a obtenção do grau de Mestre em Ciência da Computação.

```sh
$ pip3 install -r requirements.txt
$ python3 main.py
```

| Arquivo | Descrição |
| ------ | ------ |
| [main][mainfile] | arquivo principal onde realizam-se as chamadas aos demais métodos que compõe o *pipeline* de execução|
| [webscraping][webscrapingfile] | *script* desenvolvido de modo *ad-hoc* para coleta de dados provenientes da fonte utilizada (Foursquare)|
| [preprocess][preprocessfile] | *script* de pré-processamento dos dados |
| [process][processfile] | *script* de processamento dos dados a serem analisados |
| [analyser][analyserfile] | *script* desenvolvido para análise de dados do *dataset* de moda extrair indicadores a serem utilizados no processo de recomendação |
| [recommendation][recommendationfile] | *script* onde são aplicados os algoritmos de recomendação utilizando a biblioteca [surprise][surpriselib] |
| [ontology][ontologyfile] | *script* de população automazida da [ontologia][onto] a partir do conjunto de dados atual|

[mainfile]: <https://github.com/brendasalenave/dissertacao/blob/master/main.py>
[webscrapingfile]: <https://github.com/brendasalenave/dissertacao/blob/master/webscraping.py>
[preprocessfile]: <https://github.com/brendasalenave/dissertacao/blob/master/preprocess.py>
[processfile]: <https://github.com/brendasalenave/dissertacao/blob/master/process.py>
[analyserfile]: <https://github.com/brendasalenave/dissertacao/blob/master/analyser.py>
[recommendationfile]: <https://github.com/brendasalenave/dissertacao/blob/master/recommendation.py>
[ontologyfile]: <https://github.com/brendasalenave/dissertacao/blob/master/ontology.py>
[onto]: <https://github.com/brendasalenave/dissertacao/blob/master/ontology.py>
[surpriselib]: <http://surpriselib.com>
