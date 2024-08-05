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
class Test_C2303109_Tracking_of_Connect_Feature_Items(Common):
    """
    TR_ID: C2303109
    NAME: Tracking of Connect Feature Items
    DESCRIPTION: This test case verifies sending GA tracking for Connect Feature Items
    PRECONDITIONS: Note:
    PRECONDITIONS: Connect features are represented in 3 places:
    PRECONDITIONS: * header ribbon -> CONNECT
    PRECONDITIONS: * header ribbon -> ALL SPORTS -> CONNECT section
    PRECONDITIONS: * Right Hand Menu -> CONNECT section
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Log in with In-shop user
    """
    keep_browser_open = True

    def test_001_select_connect_from_header_ribbon(self):
        """
        DESCRIPTION: Select 'Connect' from header ribbon
        EXPECTED: Connect Landing page is opened
        """
        pass

    def test_002_tap_use_connect_online_item(self):
        """
        DESCRIPTION: Tap 'Use Connect Online' item
        EXPECTED: GA tracking is sent: Console: dataLayer.push({'event': 'trackEvent', 'eventCategory': 'navigation', 'eventAction': 'my account', 'eventLabel': 'Use Connect Online'})
        """
        pass

    def test_003_tap_shop_exclusive_promos_item(self):
        """
        DESCRIPTION: Tap 'Shop Exclusive Promos' item
        EXPECTED: GA tracking is sent: Console: dataLayer.push({'event': 'trackEvent', 'eventCategory': 'navigation', 'eventAction': 'my account', 'eventLabel': 'Shop Promos'})
        """
        pass

    def test_004_tap_shop_bet_tracker_item(self):
        """
        DESCRIPTION: Tap 'Shop Bet Tracker' item
        EXPECTED: GA tracking is sent: Console: dataLayer.push({'event': 'trackEvent', 'eventCategory': 'navigation', 'eventAction': 'my account', 'eventLabel': 'Shop Bet Tracker'})
        """
        pass

    def test_005_tap_football_bet_filter(self):
        """
        DESCRIPTION: Tap 'Football Bet Filter'
        EXPECTED: GA tracking is sent: Console: dataLayer.push({'event': 'trackEvent', 'eventCategory': 'navigation', 'eventAction': 'my account', 'eventLabel': 'Football Bet Filter'})
        """
        pass

    def test_006_tap_saved_bet_filter_results(self):
        """
        DESCRIPTION: Tap 'Saved Bet Filter Results'
        EXPECTED: GA tracking is sent: Console: dataLayer.push({'event': 'trackEvent', 'eventCategory': 'navigation', 'eventAction': 'my account', 'eventLabel': 'Saved Bet Filter Results'})
        """
        pass

    def test_007_tap_shop_locator(self):
        """
        DESCRIPTION: Tap 'Shop locator'
        EXPECTED: GA tracking is sent: Console: dataLayer.push({'event': 'trackEvent', 'eventCategory': 'navigation', 'eventAction': 'my account', 'eventLabel': 'Shop Locator'})
        """
        pass

    def test_008_open_all_sports_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Open 'All-Sports' and repeat steps #2-7
        EXPECTED: 
        """
        pass

    def test_009_open_rhm_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Open RHM and repeat steps #2-7
        EXPECTED: 
        """
        pass
