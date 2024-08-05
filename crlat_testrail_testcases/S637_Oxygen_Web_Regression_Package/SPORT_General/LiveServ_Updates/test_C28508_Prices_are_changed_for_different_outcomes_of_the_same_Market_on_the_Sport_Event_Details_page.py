import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28508_Prices_are_changed_for_different_outcomes_of_the_same_Market_on_the_Sport_Event_Details_page(Common):
    """
    TR_ID: C28508
    NAME: Prices are changed for different outcomes of the same Market on the <Sport> Event Details page
    DESCRIPTION: Prices are changed for different outcomes of the same Market on the <Sport> Event Details page
    PRECONDITIONS: **Updates are received via push notifications**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_open_sport_event_details_page(self):
        """
        DESCRIPTION: Open <Sport> Event Details page
        EXPECTED: 
        """
        pass

    def test_004_trigger_price_change_for_several_outcomes_of_the_same_market_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for several outcomes of the same market from the current page
        EXPECTED: Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds and they change their colors to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        """
        pass
