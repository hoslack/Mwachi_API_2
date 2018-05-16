from flask.views import MethodView
from flask import jsonify, request
from app.models.models import Order
from app.decorators.decorators import token_required, admin_only
from app.custom_http_responses.responses import Success, Error
from app.helpers.helpers import Helpers
from . import orders_blueprint


class OrdersView(MethodView):
    """This is for handling order requests"""
    def __init__(self):
        super().__init__()
        self.success = Success()
        self.error = Error()
        self.helpers = Helpers()

    @token_required
    def post(self, user_id):
        """For adding order to database"""
        json_data = request.get_json(force=True)
        name = json_data.get('name')
        email = json_data.get('email')
        phone_number = json_data.get('phone_number')
        problem_statement = json_data.get('problem_statement')
        leading_channel = json_data.get('leading_channel')
        project_type = json_data.get('project_type')
        preferred_software = json_data.get('preferred_software')
        description = json_data.get('description')

        try:
            if not name or not email or not phone_number or not problem_statement or not leading_channel \
                    or not project_type or not preferred_software or not description:
                return self.error.bad_request('Please enter all fields')
            if not self.helpers.email_valid(email=email):
                return self.error.bad_request('Invalid email')
            order = Order(name=name, email=email, phone_number=phone_number, problem_statement=problem_statement,
                          leading_channel=leading_channel,
                          project_type=project_type, preferred_software=preferred_software, description=description)
            order.save()
            return jsonify({'message': 'Success', 'id': order.id}), 201
        except Exception as e:
            return self.error.internal_server_error('Error occurred {}'.format(e))

    def get(self):
        """This is a method for getting all orders from the database"""
        try:
            orders = Order.query.all()
            order_data = []

            #  make the data json serializable
            for order in orders:
                order_data.append({'id': order.id, 'name': order.name, 'email': order.email,
                                   'phone_number': order.phone_number, 'problem_statement': order.problem_statement,
                                   'leading_channel': order.leading_channel, 'project_type':order.project_type,
                                   'preferred_software': order.preferred_software, 'description':order.description})
            return jsonify({'data': order_data}), 200
        except Exception as e:
            return self.error.internal_server_error('Error occurred'.format(e))


orders_view = OrdersView.as_view('orders_view')
orders_blueprint.add_url_rule('/orders/', view_func=orders_view, methods=['GET', 'POST'])
