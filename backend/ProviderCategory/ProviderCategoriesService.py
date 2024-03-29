from flask_cors import CORS
from flask import jsonify, Blueprint, request
from ProviderCategory.ProviderCategoriesModel import ProviderCategories
from sqlalchemy import func
from Providers.ProviderModel import Providers
from Ratings.RatingsModel import Ratings
from sqlalchemy import and_
from Requests.RequestsModel import Requests


provider_categories_route = Blueprint("provider_categories_route", __name__)
CORS(provider_categories_route)



# @provider_categories_route.route("/get_all_services", methods=['GET'])
# def get_services():
#     from app import session

#     rated_providers_query = session.query(Ratings.provider_id).filter(Ratings.no_of_stars.isnot(None)).distinct().subquery()

#     data = session.query(
#         Providers.provider_id,
#         Providers.user_id,
#         Providers.provider_contact,
#         Providers.business_name,
#         Providers.bio,
#         ProviderCategories.main_categories,
#         ProviderCategories.sub_categories,
#         ProviderCategories.subcategories_description,
#         ProviderCategories.subcategory_image,
#         ProviderCategories.number_of_visits,
#         Ratings.no_of_stars
#     ).join(ProviderCategories, Providers.user_id == ProviderCategories.user_id)\
#      .outerjoin(Ratings, and_(Providers.provider_id == Ratings.provider_id, ProviderCategories.sub_categories == Ratings.subcategory))\
#      .join(rated_providers_query, Providers.provider_id == rated_providers_query.c.provider_id, isouter=True)\
#      .all()

#     result = {
#         'data': []
#     }

#     for provider_id, user_id, provider_contact, business_name, bio, main_categories, sub_categories, subcategories_description, subcategory_image, number_of_visits, no_of_stars in data:
#         found = False
#         for item in result['data']:
#             if item['provider_id'] == provider_id and item['sub_categories'] == sub_categories:
#                 item['no_of_stars'].append(no_of_stars)
#                 found = True
#                 break

#         if not found:
#             result['data'].append({
#                 'provider_id': provider_id,
#                 'user_id': user_id,
#                 'provider_contact': provider_contact,
#                 'business_name': business_name,
#                 'bio': bio,
#                 'main_categories': main_categories,
#                 'sub_categories': sub_categories,
#                 'subcategories_description': subcategories_description,
#                 'subcategory_image': subcategory_image,
#                 'number_of_visits': number_of_visits,
#                 'no_of_stars': [] if no_of_stars is None else [no_of_stars]
#             })

#     return jsonify(result)


@provider_categories_route.route("/get_all_services", methods=['GET'])
def get_services():
    from app import session

    rated_providers_query = session.query(
        Ratings.provider_id,
        Ratings.subcategory,  # Include the subcategory column in the subquery
        func.array_agg(Ratings.no_of_stars).filter(Ratings.no_of_stars.isnot(None)).label("no_of_stars")
    ).group_by(Ratings.provider_id, Ratings.subcategory).subquery()

    data = session.query(
        Providers.provider_id,
        Providers.user_id,
        Providers.provider_contact,
        Providers.business_name,
        Providers.bio,
        ProviderCategories.main_categories,
        ProviderCategories.sub_categories,
        ProviderCategories.subcategories_description,
        ProviderCategories.subcategory_image,
        ProviderCategories.number_of_visits,
        rated_providers_query.c.no_of_stars,
        func.count(Requests.request_id).label("request_count")
    ).join(ProviderCategories, Providers.user_id == ProviderCategories.user_id)\
     .outerjoin(Ratings, and_(Providers.provider_id == Ratings.provider_id, ProviderCategories.sub_categories == Ratings.subcategory))\
     .join(rated_providers_query, and_(Providers.provider_id == rated_providers_query.c.provider_id, ProviderCategories.sub_categories == rated_providers_query.c.subcategory), isouter=True)\
     .outerjoin(Requests, and_(Providers.provider_id == Requests.provider_id, ProviderCategories.sub_categories == Requests.subcategory))\
     .group_by(
        Providers.provider_id,
        Providers.user_id,
        Providers.provider_contact,
        Providers.business_name,
        Providers.bio,
        ProviderCategories.main_categories,
        ProviderCategories.sub_categories,
        ProviderCategories.subcategories_description,
        ProviderCategories.subcategory_image,
        ProviderCategories.number_of_visits,
        rated_providers_query.c.no_of_stars
    ).all()

    result = {
        'data': []
    }

    for provider_id, user_id, provider_contact, business_name, bio, main_categories, sub_categories, subcategories_description, subcategory_image, number_of_visits, no_of_stars, request_count in data:
        found = False
        for item in result['data']:
            if item['provider_id'] == provider_id and item['sub_categories'] == sub_categories:
                item['no_of_stars'].extend(no_of_stars)
                item['request_count'] = request_count
                found = True
                break

        if not found:
            result['data'].append({
                'provider_id': provider_id,
                'user_id': user_id,
                'provider_contact': provider_contact,
                'business_name': business_name,
                'bio': bio,
                'main_categories': main_categories,
                'sub_categories': sub_categories,
                'subcategories_description': subcategories_description,
                'subcategory_image': subcategory_image,
                'number_of_visits': number_of_visits,
                'no_of_stars': [] if no_of_stars is None else no_of_stars,
                'request_count': request_count
            })

    return jsonify(result)
