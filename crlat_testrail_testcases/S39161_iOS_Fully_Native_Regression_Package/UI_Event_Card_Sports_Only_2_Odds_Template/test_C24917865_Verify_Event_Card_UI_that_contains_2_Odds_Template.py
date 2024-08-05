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
class Test_C24917865_Verify_Event_Card_UI_that_contains_2_Odds_Template(Common):
    """
    TR_ID: C24917865
    NAME: Verify Event Card UI that contains 2 Odds Template
    DESCRIPTION: This test case verifies UI of 2 Odds Template and information displayed on card when user is viewing an Event
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default
    PRECONDITIONS: * Pre-Match event card with 2 odds Template is available
    PRECONDITIONS: Scope
    PRECONDITIONS: IN
    PRECONDITIONS: - All Sports
    PRECONDITIONS: - Event Cards
    PRECONDITIONS: - 2 Odds
    PRECONDITIONS: - Sign-Posting
    PRECONDITIONS: - iPhone Only
    PRECONDITIONS: OUT
    PRECONDITIONS: - Horse Racing
    PRECONDITIONS: - Greyhounds
    PRECONDITIONS: - Outrights
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_that_contains_2_odds_template(self):
        """
        DESCRIPTION: Navigate to the Event that contains 2 Odds Template
        EXPECTED: User is viewing an Event with market displayed that contains 2 odds
        """
        pass

    def test_002_verify_information_displayed_on_the_card(self):
        """
        DESCRIPTION: Verify Information displayed on the Card
        EXPECTED: Event card contains the following information:
        EXPECTED: - Header (1 2 for Sports listed in ticket)
        EXPECTED: - Event Name
        EXPECTED: - Competition Name
        EXPECTED: - Start Time
        EXPECTED: - Player serving (if applicable - Blue dot next to player name)
        EXPECTED: - Live (if event will be traded in-play)
        EXPECTED: - Watch & Watch Live (if applicable)
        EXPECTED: Ladbrokes:
        EXPECTED: in-play
        EXPECTED: ![](index.php?/attachments/get/42433)
        EXPECTED: ![](index.php?/attachments/get/42434)
        EXPECTED: Coral:
        EXPECTED: in-play
        EXPECTED: ![](index.php?/attachments/get/42435)
        EXPECTED: ![](index.php?/attachments/get/42436)
        """
        pass
