# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2020 fetchai
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

"""
This module contains the classes required for default dialogue management.

- DefaultDialogue: The dialogue class maintains state of a dialogue and manages it.
- DefaultDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, FrozenSet, Type, cast

from aea.mail.base import Address
from aea.protocols.base import Message
from aea.protocols.default.message import DefaultMessage
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues


class DefaultDialogue(Dialogue):
    """The default dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES = frozenset(
        {DefaultMessage.Performative.BYTES, DefaultMessage.Performative.ERROR}
    )
    TERMINAL_PERFORMATIVES = frozenset(
        {DefaultMessage.Performative.BYTES, DefaultMessage.Performative.ERROR}
    )
    VALID_REPLIES = {
        DefaultMessage.Performative.BYTES: frozenset(
            {DefaultMessage.Performative.BYTES, DefaultMessage.Performative.ERROR}
        ),
        DefaultMessage.Performative.ERROR: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a default dialogue."""

        AGENT = "agent"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a default dialogue."""

        SUCCESSFUL = 0
        FAILED = 1

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        agent_address: Address,
        role: Dialogue.Role,
        message_class: Type[DefaultMessage] = DefaultMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param agent_address: the address of the agent for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :return: None
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            agent_address=agent_address,
            role=role,
        )


class DefaultDialogues(Dialogues, ABC):
    """This class keeps track of all default dialogues."""

    END_STATES = frozenset(
        {DefaultDialogue.EndState.SUCCESSFUL, DefaultDialogue.EndState.FAILED}
    )

    def __init__(
        self,
        agent_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[DefaultDialogue] = DefaultDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param agent_address: the address of the agent for whom dialogues are maintained
        :return: None
        """
        Dialogues.__init__(
            self,
            agent_address=agent_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=DefaultMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
