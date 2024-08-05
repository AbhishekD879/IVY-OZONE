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
class Test_C85299_TO_BE_ARCHIVED_Tracking_of_click_on_Bet_Receipt_banner(Common):
    """
    TR_ID: C85299
    NAME: [TO BE ARCHIVED] Tracking of click on Bet Receipt banner
    DESCRIPTION: This test case verifies tracking of click on Bet Receipt banner
    DESCRIPTION: Check CMS configuration for AEM bet receipt banner
    DESCRIPTION: https://{host}/banners/receipt/mobile
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Test case should be run on Mobile devices
    PRECONDITIONS: 4. User has enough funds to place a bet
    PRECONDITIONS: 5. Leagues and Bet Receipt Banners are created in CMS (Link to DEV CMS: https://invictus.coral.co.uk/keystone/ )
    """
    keep_browser_open = True

    def test_001_place_a_bet_on_event_from_created_in_cms_league(self):
        """
        DESCRIPTION: Place a bet on event from created in CMS league
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed
        EXPECTED: - Bet Receipt clickable banner is shown in the footer
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_003_expand_few_last_objects(self):
        """
        DESCRIPTION: Expand few last objects
        EXPECTED: There is no object for tracking of click by Bet Receipt banner
        """
        pass

    def test_004_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: 
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window.
        """
        pass

    def test_006_expand_the_second_last_object(self):
        """
        DESCRIPTION: Expand the second last Object
        EXPECTED: The next static parameters are present:
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'banner',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : '<< BANNER TITLE >>', (name of banner in CMS)
        EXPECTED: 'location' : 'Bet Receipt',
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', (VIP level of logged in user)
        EXPECTED: 'position' : '1'
        EXPECTED: }
        """
        pass
