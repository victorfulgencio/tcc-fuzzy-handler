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
    print('this is the event object -> ', event)
    body = json.loads(event['body'])
    print('this is the body object', body)

    fuzzy_controller = FuzzyClassifier()
    rating = fuzzy_controller.get_result_for(city_coverage4G=body['city_coverage4G'],
                                             city_coverage3G=body['city_coverage3G'],
                                             city_coverage2G=body['city_coverage2G'],
                                             most_valuable_areas_coverage4G=body['most_valuable_areas_coverage4G'],
                                             most_valuable_areas_coverage3G=body['most_valuable_areas_coverage3G'],
                                             most_valuable_areas_coverage2G=body['most_valuable_areas_coverage2G'],
                                             cost=body['cost'], service=body['service'],
                                             claimed_issues=body['claimed_issues'])
    return respond(None, rating)


# Mock
# mockedEvent = {'body': json.dumps({
#     'city_coverage2G': 20,
#     'city_coverage3G': 20,
#     'city_coverage4G': 20,
#     'most_valuable_areas_coverage2G': 15,
#     'most_valuable_areas_coverage3G': 15,
#     'most_valuable_areas_coverage4G': 15,
#     'cost': 400,
#     'service': 20,
#     'claimed_issues': 800
# })}
# print(lambda_handler(mockedEvent, None))
