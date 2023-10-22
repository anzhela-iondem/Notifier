from flask import request, Response
from flask.views import MethodView

from src.infrastructure.controllers import APIController


class APIView(MethodView):

    def post(self) -> tuple[Response, int]:
        """
        Catch the POST requests and send the data to API controller.
        :return tuple with a response and a number:
        """
        event_data = request.json  # The type of received data is dictionary.
        api_controller = APIController()
        response = api_controller.process_event(event_data)
        return response
