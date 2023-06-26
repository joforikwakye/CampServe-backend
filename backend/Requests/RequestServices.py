from flask import jsonify, Blueprint, request
from flask_cors import CORS
from Requests.RequestsModel import Requests



request_services_route = Blueprint("request_services_route", __name__)
CORS(request_services_route)



@request_services_route.route('/book_services', methods=['POST'])
def book_services():
    from app import session

    data = request.get_json()

    provider_id = data['provider_id']
    user_id = data['user_id']
    location = data['location']
    payment_mode = data['paymentMode']
    agreed_price = data['price']
    scheduled_datetime = data['scheduledDateTime']
    subcategory = data['subcategory']

   
    try:
        new_request = Requests(
            provider_id=provider_id,
            user_id=user_id,
            location=location,
            payment_mode=payment_mode,
            agreed_price=agreed_price,
            scheduled_datetime=scheduled_datetime,
            subcategory = subcategory,
            status_comp_inco="no action",
            status_acc_dec="no action"
        )

        # Add the new_request to the session and commit to the database
        session.add(new_request)
        session.commit()

        return jsonify({'message': 'Request added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

#for shwoing the requests for a particular provider when they log in to their account
@request_services_route.route('/get_specific_provider_requests/<provider_id>', methods=['GET'])
def get_provider_requests(provider_id):
    from app import session
    try:
        requests = session.query(Requests).filter(Requests.provider_id == provider_id).all()

        if not requests:
            return jsonify({'message': 'No requests at the moment.'})

        
        for request in requests:
            request_data = {
                'agreed_price': request.agreed_price,
                'location': request.location,
                'scheduled_datetime': request.scheduled_datetime,
                'payment_mode': request.payment_mode
               
            }
            
        return jsonify(request_data)
    except Exception as e:
        return jsonify({'error': str(e)})

