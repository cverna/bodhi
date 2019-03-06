import mock

from bodhi.tests.server import base
from fedora_messaging.api import Message
from bodhi.server.consumers import messaging_callback


class TestConsumers(base.BaseTestCase):
    """Test class for the messaging_callback function """

    @mock.patch('bodhi.server.consumers.ComposerHandler')
    def test_messaging_callback_composer(self, handler):
        msg = Message(
            topic="org.fedoraproject.prod.bodhi.masher.start",
            body={}
        )
        messaging_callback(msg)
        handler.assert_called_once_with()

    @mock.patch('bodhi.server.consumers.SignedHandler')
    def test_messaging_callback_signed(self, handler):
        msg = Message(
            topic="org.fedoraproject.prod.buildsys.tag",
            body={}
        )
        messaging_callback(msg)
        handler.assert_called_once_with()

    @mock.patch('bodhi.server.consumers.UpdatesHandler')
    def test_messaging_callback_updates_testing(self, handler):
        msg = Message(
            topic="org.fedoraproject.prod.bodhi.update.request.testing",
            body={}
        )
        messaging_callback(msg)
        handler.assert_called_once_with()

    @mock.patch('bodhi.server.consumers.UpdatesHandler')
    def test_messaging_callback_updates_edit(self, handler):
        msg = Message(
            topic="org.fedoraproject.prod.bodhi.update.edit",
            body={}
        )
        messaging_callback(msg)
        handler.assert_called_once_with()
