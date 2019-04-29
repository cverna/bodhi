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
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
The "greenwave handler".

This module is responsible for listening for messages from greenwave.
It then updates the policies of the build that greenwave checked.
"""

import logging

import fedora_messaging

from bodhi.server.models import Build
from bodhi.server.models import Update
from bodhi.server.logging import setup as setup_logging

log = logging.getLogger(__name__)


class GreenwaveHandler:
    """
    The Bodhi Greenwave Handler.

    A fedora-messaging listener waiting for messages from greenwave about enforced policies.
    """

    def __init__(self):
        """Initialize the GreenwaveHandler."""
        setup_logging()

    def __call__(self, message: fedora_messaging.api.Message):
        """Handle messages arriving with the configured topic."""
        msg = message.body['msg']
        subject_identifier = msg['subject_identifier']
        build = Build.get(subject_identifier)
        update = Update
        update = build.update
        update.update_test_gating_status()
        log.info("Update of test_gating_status for: %s" % (update.alias))
