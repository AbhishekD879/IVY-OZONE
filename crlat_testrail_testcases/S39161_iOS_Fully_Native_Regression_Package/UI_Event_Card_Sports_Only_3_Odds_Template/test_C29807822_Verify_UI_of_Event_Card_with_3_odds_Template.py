import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.native
@vtest
class Test_C29807822_Verify_UI_of_Event_Card_with_3_odds_Template(Common):
    """
    TR_ID: C29807822
    NAME: Verify UI of Event Card with 3 odds Template
    DESCRIPTION: This test case verifies the UI of Event Card with 3 odds Template
    DESCRIPTION: Should be verified on the following platforms:
    DESCRIPTION: * iOS
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default
    PRECONDITIONS: * Pre-Match event card with 3 odds Template is available
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes: https://zpl.io/ad1NwYl
    PRECONDITIONS: https://zpl.io/a8J3PAd
    PRECONDITIONS: Coral:  https://zpl.io/V1pyeOX
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_card_with_3_odds_template(self):
        """
        DESCRIPTION: Navigate to the Event Card with 3 odds Template
        EXPECTED: - user is viewing an Event
        EXPECTED: - 3 odds boxes are displayed
        """
        pass

    def test_002_verify_ui_of_event_card_with_3_odds_template(self):
        """
        DESCRIPTION: Verify UI of Event Card with 3 odds Template
        EXPECTED: Event Card must contain the following information:
        EXPECTED: - Header (Home Draw Away for Sports apart from Cricket Test Matches which is 1 x 2)
        EXPECTED: - Competition name
        EXPECTED: - Event Name (if Team name is too long must truncate text E.G New York Yankees = New York Y....)
        EXPECTED: - Start Time
        EXPECTED: - Live (if the event will be traded in-play)
        EXPECTED: - Watch & Watch Live (if applicable)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39897)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/39903)
        """
        pass
