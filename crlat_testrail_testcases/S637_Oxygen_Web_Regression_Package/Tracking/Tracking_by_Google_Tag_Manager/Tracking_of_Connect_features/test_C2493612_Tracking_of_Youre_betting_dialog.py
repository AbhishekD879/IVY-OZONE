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
class Test_C2493612_Tracking_of_Youre_betting_dialog(Common):
    """
    TR_ID: C2493612
    NAME: Tracking of 'You're betting' dialog
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-34349 Pi12: Football Bet Filter Popup
    PRECONDITIONS: Select 'Connect' from header sports ribbon -> Connect landing page is opened
    PRECONDITIONS: Tap Football Bet Filter -> 'You're betting' CTA is shown
    """
    keep_browser_open = True

    def test_001_tap_online(self):
        """
        DESCRIPTION: Tap 'Online'
        EXPECTED: In-shop football bet filter page is opened
        """
        pass

    def test_002_open_browser_console___enter_datalayer_in_console___expand_last_object(self):
        """
        DESCRIPTION: Open browser console -> enter 'dataLayer' in Console -> expand last Object
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'bet filter',
        EXPECTED: 'eventAction' : 'you're betting',
        EXPECTED: 'eventLabel' : 'online'
        EXPECTED: });
        """
        pass

    def test_003_get_back_to_connect_landing_page___tap_football_bet_filter___in_shop(self):
        """
        DESCRIPTION: Get back to Connect landing page -> Tap Football Bet Filter -> In-shop
        EXPECTED: Online football bet filter page is opened
        """
        pass

    def test_004_open_browser_console___enter_datalayer_in_console___expand_last_object(self):
        """
        DESCRIPTION: Open browser console -> enter 'dataLayer' in Console -> expand last Object
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'bet filter',
        EXPECTED: 'eventAction' : 'you're betting',
        EXPECTED: 'eventLabel' : 'in-shop'
        EXPECTED: });
        """
        pass
