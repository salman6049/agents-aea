# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""This package contains integration test for the aries_alice skill and the aries_faber skill."""
import random
import string
import subprocess  # nosec
from random import randint  # nosec

import pytest

from aea.test_tools.test_cases import AEATestCaseMany

from packages.fetchai.connections.p2p_libp2p.connection import (
    LIBP2P_SUCCESS_MESSAGE,
    P2PLibp2pConnection,
)
from packages.fetchai.skills.aries_alice import PUBLIC_ID as ALICE_SKILL_PUBLIC_ID
from packages.fetchai.skills.aries_faber import PUBLIC_ID as FABER_SKILL_PUBLIC_ID


def _rand_seed():
    return "".join(
        random.choice(string.ascii_uppercase + string.digits)  # nosec
        for _ in range(32)
    )


README = """
To start with test:
`pip install aries-cloudagent` acaPY is required

## VON Network

In the first terminal move to the `von-network` directory and run an instance of `von-network` locally in docker.

This <a href="https://github.com/bcgov/von-network#running-the-network-locally" target="_blank">tutorial</a> has information on starting (and stopping) the network locally.

``` bash
./manage build
./manage start 172.17.0.1,172.17.0.1,172.17.0.1,172.17.0.1 --logs
```

172.17.0.1 - is ip address of the docker0 network interface, can be used  any address assigned to the host except 127.0.0.1
"""


@pytest.mark.unstable
@pytest.mark.integration
class TestAriesSkillsDemo(AEATestCaseMany):
    """Test integrated aries skills."""

    @classmethod
    def get_port(cls) -> int:
        """Get next tcp port number."""
        cls.port += 1  # type: ignore
        return cls.port  # type: ignore

    @classmethod
    def setup_class(cls) -> None:
        """Setup test case."""
        check_acapy = subprocess.run("aca-py", shell=True, capture_output=True)  # nosec
        assert b"usage: aca-py" in check_acapy.stdout, "aca-py is not installed!"

        cls.port = 10001  # type: ignore
        super(TestAriesSkillsDemo, cls).setup_class()
        cls.alice = "alice"  # type: ignore
        cls.alice_soef_id = "intro_alice" + str(  # type: ignore
            randint(1000000, 99999999999999)  # nosec
        )
        cls.alice_seed = _rand_seed()  # type: ignore
        cls.faber = "faber"  # type: ignore

        cls.faber_seed = _rand_seed()  # type: ignore
        cls.controller = "controller"  # type: ignore
        cls.fetch_agent("fetchai/aries_alice", cls.alice, is_local=True)  # type: ignore
        cls.fetch_agent("fetchai/aries_faber", cls.faber, is_local=True)  # type: ignore
        cls.create_agents(cls.controller,)  # type: ignore

        cls.set_agent_context(cls.controller)  # type: ignore
        cls.add_item("connection", "fetchai/p2p_libp2p")

        addr = f"127.0.0.1:{cls.get_port()}"
        p2p_config = {  # type: ignore
            "delegate_uri": None,  # f"127.0.0.1:{cls.get_port()}",
            "entry_peers": [],
            "local_uri": addr,
            "public_uri": addr,
        }
        cls.nested_set_config(
            "vendor.fetchai.connections.p2p_libp2p.config", p2p_config
        )
        cls.generate_private_key("fetchai", "fetchai.key")
        cls.add_private_key("fetchai", "fetchai.key")
        cls.add_private_key("fetchai", "fetchai.key", connection=True)
        cls.run_cli_command("build", cwd=cls._get_cwd())
        cls.run_cli_command("issue-certificates", cwd=cls._get_cwd())
        r = cls.run_cli_command(
            "get-multiaddress",
            "fetchai",
            "-c",
            "-i",
            str(P2PLibp2pConnection.connection_id),
            "-u",
            "public_uri",
            cwd=cls._get_cwd(),
        )
        peer_addr = r.stdout.strip()
        for agent_name in [cls.alice, cls.faber]:  # type: ignore
            cls.set_agent_context(agent_name)
            p2p_config = {
                "delegate_uri": None,  # f"127.0.0.1:{cls.get_port()}",
                "entry_peers": [peer_addr],
                "local_uri": f"127.0.0.1:{cls.get_port()}",
                "public_uri": None,
            }
            cls.generate_private_key("fetchai", "fetchai.key")
            cls.add_private_key("fetchai", "fetchai.key")
            cls.add_private_key(
                "fetchai", "fetchai.key", connection=True,
            )
            cls.nested_set_config(
                "vendor.fetchai.connections.p2p_libp2p.config", p2p_config
            )

            cls.run_cli_command("build", cwd=cls._get_cwd())
            cls.run_cli_command("issue-certificates", cwd=cls._get_cwd())

        cls.set_agent_context(cls.alice)  # type: ignore
        cls.set_config(
            "vendor.fetchai.skills.aries_alice.models.strategy.args.seed",
            cls.alice_seed,  # type: ignore
        )
        cls.set_config(
            "vendor.fetchai.skills.aries_alice.models.strategy.args.service_data.value",
            cls.alice_soef_id,  # type: ignore
        )
        cls.set_config(
            "vendor.fetchai.skills.aries_alice.models.strategy.args.admin_host",
            "127.0.0.1",
        )
        cls.set_config(
            "vendor.fetchai.skills.aries_alice.models.strategy.args.admin_port",
            "8031",
            "int",
        )

        cls.set_config(
            "vendor.fetchai.connections.webhook.config.webhook_port", "8032", "int"
        )
        cls.set_config(
            "vendor.fetchai.connections.webhook.config.webhook_address", "127.0.0.1"
        )
        cls.set_config(
            "vendor.fetchai.connections.webhook.config.target_skill_id",
            str(ALICE_SKILL_PUBLIC_ID),
        )
        cls.set_config(
            "vendor.fetchai.connections.webhook.config.webhook_url_path",
            "/webhooks/topic/{topic}/",
        )

        cls.set_agent_context(cls.faber)  # type: ignore
        cls.set_config(
            "vendor.fetchai.skills.aries_faber.models.strategy.args.seed",
            cls.faber_seed,  # type: ignore
        )

        cls.set_config(
            "vendor.fetchai.skills.aries_faber.models.strategy.args.search_query.search_value",
            cls.alice_soef_id,  # type: ignore
        )
        cls.set_config(
            "vendor.fetchai.skills.aries_faber.models.strategy.args.admin_host",
            "127.0.0.1",
        )
        cls.set_config(
            "vendor.fetchai.skills.aries_faber.models.strategy.args.admin_port",
            "8021",
            "int",
        )

        cls.set_config(
            "vendor.fetchai.connections.webhook.config.target_skill_id",
            str(FABER_SKILL_PUBLIC_ID),
        )
        cls.set_config(
            "vendor.fetchai.connections.webhook.config.webhook_port", "8022", "int"
        )
        cls.set_config(
            "vendor.fetchai.connections.webhook.config.webhook_address", "127.0.0.1"
        )
        cls.set_config(
            "vendor.fetchai.connections.webhook.config.webhook_url_path",
            "/webhooks/topic/{topic}/",
        )

        cls.extra_processes = [  # type: ignore
            subprocess.Popen(  # nosec
                [
                    "python3",
                    "-m",
                    "aries_cloudagent",
                    "start",
                    "--auto-ping-connection",
                    "--auto-respond-messages",
                    "--auto-store-credential",
                    "--auto-accept-invites",
                    "--auto-accept-requests",
                    "--debug-credentials",
                    "--debug-presentations",
                    "--debug-connections",
                    "--admin",
                    "127.0.0.1",
                    "8031",
                    "--admin-insecure-mode",
                    "--inbound-transport",
                    "http",
                    "0.0.0.0",
                    "8030",
                    "--outbound-transp",
                    "http",
                    "--webhook-url",
                    "http://127.0.0.1:8032/webhooks",
                    "-e",
                    "http://192.168.1.43:8030",
                    "--genesis-url",
                    "http://localhost:9000/genesis",
                    "--wallet-type",
                    "indy",
                    "--wallet-name",
                    "alice" + str(randint(10000000, 999999999999)),  # nosec
                    "--wallet-key",
                    "walkey",
                    "--seed",
                    cls.alice_seed,  # type: ignore
                    "--recreate-wallet",
                    "--wallet-local-did",
                    "--auto-provision",
                    "--label",
                    "alice",
                ]
            ),
            subprocess.Popen(  # nosec
                [
                    "python3",
                    "-m",
                    "aries_cloudagent",
                    "start",
                    "--auto-ping-connection",
                    "--auto-respond-messages",
                    "--auto-accept-invites",
                    "--auto-accept-requests",
                    "--debug-credentials",
                    "--debug-presentations",
                    "--debug-connections",
                    "--admin",
                    "127.0.0.1",
                    "8021",
                    "--admin-insecure-mode",
                    "--inbound-transport",
                    "http",
                    "0.0.0.0",
                    "8020",
                    "--outbound-transport",
                    "http",
                    "--webhook-url",
                    "http://127.0.0.1:8022/webhooks",
                    "-e",
                    "http://192.168.1.43:8020",
                    "--genesis-url",
                    "http://localhost:9000/genesis",
                    "--wallet-type",
                    "indy",
                    "--wallet-name",
                    "faber" + str(randint(10000000, 999999999999)),  # nosec
                    "--wallet-key",
                    "walkey",
                    "--seed",
                    cls.faber_seed,  # type: ignore
                    "--recreate-wallet",
                    "--wallet-local-did",
                    "--auto-provision",
                    "--label",
                    "faber",
                ]
            ),
        ]

    def test_alice_faber_demo(self):
        """Run demo test."""
        self.set_agent_context(self.controller)
        controller_process = self.run_agent()
        self.extra_processes.append(controller_process)

        check_strings = (
            "Starting libp2p node...",
            "Connecting to libp2p node...",
            "Successfully connected to libp2p node!",
            LIBP2P_SUCCESS_MESSAGE,
        )

        missing_strings = self.missing_from_output(
            controller_process, check_strings, timeout=30, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in controller output.".format(missing_strings)

        self.set_agent_context(self.faber)
        faber_process = self.run_agent()
        self.extra_processes.append(faber_process)

        self.set_agent_context(self.alice)
        alice_process = self.run_agent()
        self.extra_processes.append(alice_process)

        missing_strings = self.missing_from_output(
            alice_process, ["Connected to Faber"], timeout=80, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in alice output.".format(missing_strings)

        missing_strings = self.missing_from_output(
            faber_process, ["Connected to Alice"], timeout=80, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in faber output.".format(missing_strings)

    @classmethod
    def teardown_class(cls) -> None:
        """Tear down test case."""
        super(TestAriesSkillsDemo, cls).teardown_class()
        for proc in cls.extra_processes:  # type: ignore
            proc.kill()
            proc.wait(10)


if __name__ == "__main__":
    pytest.main([__file__])
