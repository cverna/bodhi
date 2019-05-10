# Copyright © 2019 Red Hat, Inc.
#
# This file is part of Bodhi.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""This test suite contains tests for the bodhi.server.consumers.greenwave module."""

from unittest import mock

from fedora_messaging.api import Message

from bodhi.server import models
from bodhi.server.consumers import greenwave
from bodhi.server.config import config
from bodhi.tests.server.base import BaseTestCase


class TestGreenwaveHandlerConsume(BaseTestCase):
    """Test class for the :func:`GreenwaveHandler.consume` method."""

    def setUp(self):
        super().setUp()
        self.sample_message = Message(
            topic='',
            body={
                'i': 502,
                'timestamp': 1553865691.0,
                'source_name': 'datanommer',
                'source_version': '0.9.0',
                'msg_id': '2019-09aceb45-3360-4f83-9975-32ae6439c41c',
                'crypto': 'x509',
                'topic': 'org.fedoraproject.prod.greenwave.decision.update',
                'signature': '100% real please trust me',
                'msg': {
                    'subject_type': 'koji_build',
                    'policies_satisfied': True,
                    'decision_context': 'bodhi_update_push_testing',
                    'satisfied_requirements': [
                        {
                            'testcase': 'dist.abicheck',
                            'type': 'test-result-passed',
                            'result_id': 27968725
                        },
                        {
                            'testcase': 'dist.rpmdeplint',
                            'type': 'test-result-passed',
                            'result_id': 28670567
                        }
                    ],
                    'product_version': 'fedora-30',
                    'applicable_policies': [
                        'taskotron_release_critical_tasks_for_testing'
                    ],
                    'unsatisfied_requirements': [],
                    'subject_identifier': 'bodhi-2.0-1.fc17',
                    'subject': [
                        {
                            'item': 'bodhi-2.0-1.fc17',
                            'type': 'koji_build'
                        }
                    ],
                    'summary': 'All required tests passed',
                    'previous': {
                        'satisfied_requirements': [
                            {
                                'testcase': 'dist.abicheck',
                                'type': 'test-result-passed',
                                'result_id': 27968725
                            },
                            {
                                'testcase': 'dist.rpmdeplint',
                                'type': 'test-result-passed',
                                'result_id': 28666088
                            }
                        ],
                        'summary': 'All required tests passed',
                        'policies_satisfied': True,
                        'unsatisfied_requirements': [],
                        'applicable_policies': [
                            'taskotron_release_critical_tasks_for_testing'
                        ],
                    }
                }
            },
        )
        self.handler = greenwave.GreenwaveHandler()

    @mock.patch('bodhi.server.consumers.greenwave.setup_logging')
    def test___init___sets_up_logging(self, setup_logging):
        """Assert that __init__() sets up logging."""
        greenwave.GreenwaveHandler()
        setup_logging.assert_called_once_with()

    @mock.patch.dict(config, [('greenwave_api_url', 'http://domain.local')])
    @mock.patch('bodhi.server.initialize_db', mock.MagicMock())
    def test_update_test_gating_status(self):
        """Assert that messages marking the build as signed updates the database"""

        with mock.patch('bodhi.server.models.util.greenwave_api_post') as mock_greenwave:
            with mock.patch('bodhi.server.transactional_session_maker',
                            return_value=mock.MagicMock()):
                greenwave_response = {
                    'policies_satisfied': "zsdasd",
                    'summary': ""
                }
                mock_greenwave.return_value = greenwave_response
                self.handler(self.sample_message)

        build = self.db.query(models.Build).filter_by(nvr="bodhi-2.0-1.fc17").first()
        assert build.update.test_gating_status == models.TestGatingStatus.passed
