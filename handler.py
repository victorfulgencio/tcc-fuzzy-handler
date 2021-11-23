"""
    Não conseguimos ter um pacote muito grande (até 270MB) para AWS Lambda
    Por isso fiz uma gambiarra meio cabulosa:
    Para consefuir colocar este código como uma Lambda Function na AWS, tirei o Matplotlib
    Até porque ele nem é usado aqui... Somente é uma dependencia do 'skfuzzy'
    Se der merda, ir em venv/lib/__init__.py e criar uma função aleatorio nesse modulo
    Fazer a mesma coisa pros outros submodulos
"""

import json
from fuzzy import FuzzyClassifier

print('Loading FuzzyClassifier Function')


def get_std_body_payload(rating):
    return json.dumps({
        'rating': rating
    })


def respond(err, res):
    return {
        'statusCode': '400' if err else '200',
        'body': 'Not supported' if err else get_std_body_payload(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    body = json.loads(event['body'])

    city_coverage = body['city_coverage']
    most_valuable_areas_coverage = body['most_valuable_areas_coverage']
    cost = body['cost']
    service = body['service']
    claimed_issues = body['claimed_issues']

    fuzzy_controller = FuzzyClassifier()
    rating = fuzzy_controller.get_result_for(city_coverage,
                                             most_valuable_areas_coverage,
                                             cost, service, claimed_issues)
    print(respond(None, rating))
    return respond(None, rating)


# Mock
mockedEvent = {'body': json.dumps({
    'city_coverage': 20,
    'most_valuable_areas_coverage': 15,
    'cost': 400,
    'service': 20,
    'claimed_issues': 800
})}
lambda_handler(mockedEvent, None)
