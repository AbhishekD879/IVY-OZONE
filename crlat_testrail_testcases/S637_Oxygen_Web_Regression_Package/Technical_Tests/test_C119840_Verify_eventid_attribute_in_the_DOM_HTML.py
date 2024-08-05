import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C119840_Verify_eventid_attribute_in_the_DOM_HTML(Common):
    """
    TR_ID: C119840
    NAME: Verify 'eventid' attribute in the DOM/HTML
    DESCRIPTION: This Test Case verified 'eventid' attribute in the DOM/HTML.
    PRECONDITIONS: *JIRA Ticket*
    PRECONDITIONS: BMA-17291 EventID Exposure for Evergage Campaigns
    PRECONDITIONS: Open Dev Tools ->Elements -> Select an element in the page to inspect it
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_sport_landing_page(self):
        """
        DESCRIPTION: Open <Sport> Landing page
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_verify_eventid_attribute_in_the_dev_tools__elements(self):
        """
        DESCRIPTION: Verify 'eventid' attribute in the Dev Tools ->Elements
        EXPECTED: 'eventid' attribute is shown for each <Sport> Event
        """
        pass

    def test_004_repeat_step_3_for(self):
        """
        DESCRIPTION: Repeat step 3 for:
        EXPECTED: * <Sport> Landing pages
        EXPECTED: * <Race> Landing pages
        EXPECTED: * Featured tab
        EXPECTED: * Next Races tab (widget)
        EXPECTED: * In-Play tab (widget)
        EXPECTED: * In-Play page
        EXPECTED: * Live Stream tab (widget)
        EXPECTED: * Enhanced Multiples tab
        EXPECTED: * Favourites page (widget)
        EXPECTED: * Jackpot
        EXPECTED: * Cashout page (widget)
        EXPECTED: * Open Bets tab (widget)
        EXPECTED: * Bet History tab (widget)
        EXPECTED: * My Bets tab on Event Details page
        """
        pass
