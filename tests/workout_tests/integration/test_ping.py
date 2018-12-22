from workout_tests.bootstrap import BaseTestCase


class PingTestCase(BaseTestCase):

    def test_ping(self):
        result = self.client.get("/ping")
        self.assert200(result)
        self.assertEqual(result.data.decode("utf-8"), "Pong!")
