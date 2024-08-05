import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C28636309_Verify_Event_Card_UI_that_contains_1_Odd_Template(Common):
    """
    TR_ID: C28636309
    NAME: Verify Event Card UI that contains 1 Odd Template
    DESCRIPTION: This test case verifies UI of 1 Odds Template and information displayed on the card when the user is viewing an Event
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - Pre-Match event card with 1 odds Template is available
    PRECONDITIONS: Design
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://zpl.io/aN5DeAZ
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://zpl.io/29ze7KA
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_card_that_contains_1_odd_template(self):
        """
        DESCRIPTION: Navigate to the Event Card that contains 1 Odd Template
        EXPECTED: User is viewing an Event with market displayed that contains 1 odd
        """
        pass

    def test_002_verify_information_displayed_on_the_card(self):
        """
        DESCRIPTION: Verify Information displayed on the Card
        EXPECTED: The event card must contain the following information:
        EXPECTED: - Competition/Type name
        EXPECTED: - Selection Name (if the name is too long must wrap onto the next line.)
        EXPECTED: - Start Time
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/2824259)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/2824260)
        """
        pass
