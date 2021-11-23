# Fuzzy Handler

This handler uses Fuzzy Logic (skfuzzy lib) to classify a Mobile Operator depending on input params. See more in:  http://www.classificadoroperadoras.com.br

## Como funciona o deploy?
Este código é distribuído através do serverless framework e AWS Lambda Functions.
Follow https://www.serverless.com/blog/serverless-python-packaging to get deploy instructions


#### ~~Alerta de gabiarra extrema pro deploy~~:
* Não conseguimos ter um pacote muito grande (até 270MB) para AWS Lambda.
* Para conseguir fazer o deploy como uma Lambda Function na AWS, tirei o `Matplotlib`.
* Até porque ele nem é usado aqui... Somente é uma dependencia do `skfuzzy`.
* Se der merda, ir em `venv/lib/__init__.py` e criar uma função aleatória nesse modulo, como se fosse mockar a dependência não utlizada.
* Fazer a mesma coisa pros outros submodulos do Matplotlib
* Pra rodar localmente não precisa da gambiarra :)

