from time import time
from flask_cors import CORS
from flask import jsonify, Blueprint, request
from Users.UserModel import User
from Providers.ProviderModel import Providers
from Ratings.RatingsModel import Ratings


ratings_route = Blueprint("ratings_route", __name__)
CORS(ratings_route)


@ratings_route.route('/store_ratings', methods=['POST'])
def store_ratings():
    from app import session

    try:
        data = request.get_json()


        user_id = data['id']
        provider_id = data['provider_id']
        no_of_stars = data['ratings']
        comments = data['review']
        timestamp = data['timestamp']
        subcategory = data['subcategory']

        ratings = Ratings(
            user_id=user_id,
            provider_id=provider_id,
            no_of_stars=no_of_stars,
            comments=comments,
            timestamp=timestamp,
            subcategory=subcategory
           
        )
        session.add(ratings)
        session.commit()
        return jsonify({'message': 'Ratings stored successfully.'})

    except Exception as e:
        return jsonify({'error': str(e)})


@ratings_route.route('/get_ratings', methods=['POST'])
def get_ratings():
    try:
        from app import session

        data = request.get_json()

        provider_id = data['provider_id']
        subcategory = data['subcategory']

        # Fetch ratings and user details for the given provider_id
        ratings = session.query(Ratings, User).join(User, Ratings.user_id == User.user_id)\
            .filter(Ratings.provider_id == provider_id, Ratings.subcategory == subcategory).all()
        
        rating_details = []

        for rating, user in ratings:
            rating_details.append({
                'id':rating.rating_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'stars': rating.no_of_stars,
                'review': rating.comments,
                'timestamp':rating.timestamp,
                'subcategory': rating.subcategory
            })
        
        return jsonify(rating_details)

    except Exception as e:
        return jsonify({'error': 'could not retrieve the information'})