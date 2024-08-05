import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29444_Private_Markets_become_undisplayed(Common):
    """
    TR_ID: C29444
    NAME: Private Markets become undisplayed
    DESCRIPTION: This test case verifies situation when Private Markets become undisplayed.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: 4. **accountFreebets?freebetTokenType=ACCESS** the request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: 5. To check updates verify 'Displayed' attribute value in  Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket  (liveservems) -> response
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on the configured event.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Your Enhanced Markets' tab is present and selected by default **for mobile/tablet**
        EXPECTED: *   'Your Enhanced Markets' section is present at the top of the page (below Hero Header) **for mobile/tablet**
        """
        pass

    def test_002_trigger_the_situation_when_event_which_has_private_market_becomes_undisplayedn_displayedn_attribute_is_set_for_the_market(self):
        """
        DESCRIPTION: Trigger the situation when event which has private market becomes undisplayedn (displayed='N' attribute is set for the market)
        EXPECTED: The event is undisplayed and is not displayed on FE in real time
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: *   Verified undisplayed private market is no more shown within 'Your Enhanced Markets' tab/section (in case there were two or more markets available)
        EXPECTED: *   'Your Enhanced Markets' tab/section is no more shown (in case verified private market was the only one to be shown)
        EXPECTED: *  'Featured' (or another tab with the highest priority in the Module Selector Ribbon list) tab is selected by default **for mobile/tablet**
        EXPECTED: * 'In-Play & Live Stream' section is displayed at the top of the page (below Hero Header) **for desktop**
        """
        pass

    def test_004_trigger_the_situation_when_event_which_has_private_market_becomes_displayedand_refresh_the_page(self):
        """
        DESCRIPTION: Trigger the situation when event which has private market becomes displayed and refresh the page
        EXPECTED: *   Verified undisplayed private market is shown again within 'Your Enhanced Markets' tab/section (in case there were two or more markets available)
        EXPECTED: *   'Your Enhanced Markets' tab/section is shown again (in case verified private market was the only one to be shown)
        EXPECTED: *   All selections are active
        """
        pass

    def test_005_repeat_steps_2_4_but_undisplaydisplay_one_of_private_markets(self):
        """
        DESCRIPTION: Repeat steps #2-4 but undisplay/display one of private markets
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_2_4_but_undisplaydisplay_all_outcomes_of_private_markets(self):
        """
        DESCRIPTION: Repeat steps #2-4 but undisplay/display all outcomes of private markets
        EXPECTED: 
        """
        pass
