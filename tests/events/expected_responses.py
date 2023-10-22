class ExpectedResults:
    """
    Class is created to be used while testing controllers.
    """

    @property
    def get_result_new_publication(self):
        expected_list_new_publication = [
            ({"status": "success", "message": "Slack message is sent."}, 200),
            ({"status": "failed", "error": "Invalid event type."}, 400),
            ({"status": "failed", "error": "Invalid message body"}, 400),
            ({"status": "failed", "error": "Invalid message body"}, 400)
        ]
        return expected_list_new_publication

    @property
    def get_result_approved_publication(self):
        expected_result_new_publication = [
            ({"status": "success", "message": "Email is sent."}, 200),
            ({"status": "failed", "error": "Invalid event type."}, 400),
            ({"status": "failed", "error": "Invalid message body"}, 400),
            ({"status": "failed", "error": "Invalid email address."}, 400),
            ({"status": "failed", "error": "Invalid message body"}, 400)
        ]
        return expected_result_new_publication
