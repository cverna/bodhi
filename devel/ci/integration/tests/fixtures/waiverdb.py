# Copyright © 2018 Red Hat, Inc.
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

import pytest
from conu.backend.docker.container_parameters import DockerContainerParameters

from ..utils import make_db_and_user


@pytest.fixture(scope="session")
def waiverdb_container(docker_backend, docker_network, db_container):
    """Fixture preparing and yielding a WaiverDB container.

    Args:
        docker_backend (conu.DockerBackend): The Docker backend (fixture).
        docker_network (str): The Docker network ID (fixture).
        db_container(conu.DockerContainer): The PostgreSQL container (fixture).

    Yields:
        conu.DockerContainer: The WaiverDB container.
    """
    # Prepare the database
    make_db_and_user(
        db_container, "waiverdb",
        "https://infrastructure.fedoraproject.org/infra/db-dumps/waiverdb.dump.xz"
    )
    # Define the container and start it
    image_name = "bodhi-ci-integration-waiverdb"
    image = docker_backend.ImageClass(image_name)
    container = image.run_via_api(
        DockerContainerParameters(name="waiverdb")
    )
    container.start()
    docker_backend.d.connect_container_to_network(container.name, docker_network["Id"])
    # Add sample data in the database
    container.execute(["waiverdb", "db", "upgrade"])
    # we need to wait for the webserver to start serving
    container.wait_for_port(8080, timeout=-1)
    yield container
    container.kill()
    container.delete()