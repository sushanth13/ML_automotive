import urllib.request
import json

def test_predict(data):
    req = urllib.request.Request(
        'http://127.0.0.1:8002/predict', 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    print(urllib.request.urlopen(req).read().decode('utf-8'))

print('Low Intent:')
test_predict({
    'vehicle_segment': 'Mid-Size SUV', 
    'shopper_intent_decile': 1, 
    'powertrain_focus': 'ICE', 
    'days_since_last_brand_engagement': 50, 
    'intent_engagement_score': 10.0
})

print('High Intent:')
test_predict({
    'vehicle_segment': 'Luxury Sedan', 
    'shopper_intent_decile': 10, 
    'powertrain_focus': 'EV', 
    'days_since_last_brand_engagement': 1, 
    'intent_engagement_score': 99.0
})
