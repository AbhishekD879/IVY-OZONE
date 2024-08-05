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
class Test_C29435_Your_Enhanced_Markets_tab_section_when_offer_has_already_been_redeemed(Common):
    """
    TR_ID: C29435
    NAME: 'Your Enhanced Markets' tab/section when offer has already been redeemed
    DESCRIPTION: This test case verifies 'Your Enhanced Markets' tab/section when offer has already been redeemed.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: Note: **Max bet limit for offer** - amount of placed bet on some market (e.g. Max bet limit for offer=1, user is able to place a bet on such private market only once).
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: 4. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
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
        EXPECTED: *   All eligible private markets and associated selections are shown
        """
        pass

    def test_002_reach_the_max_bet_limit_for_some_offer(self):
        """
        DESCRIPTION: Reach the max bet limit for some offer
        EXPECTED: Private markets offer becomes redeemed
        """
        pass

    def test_003_verify_private_market_section_for_which_offer_has_been_redeemed(self):
        """
        DESCRIPTION: Verify private market section for which offer has been redeemed
        EXPECTED: Privet market section is disappeared after refresh
        """
        pass

    def test_004_reach_max_bet_limit_for_all_private_markets_offers_available_for_user(self):
        """
        DESCRIPTION: Reach max bet limit for all private markets offers available for user
        EXPECTED: Private markets offers becomes redeemed
        """
        pass

    def test_005_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: *   'Your Enhanced Markets' tab/section is disappeared
        EXPECTED: *  'Featured' (or another tab with the highest priority in the Module Selector Ribbon list) tab is selected by default **for mobile/tablet**
        EXPECTED: * 'In-Play & Live Stream' section is displayed at the top of the page **for desktop**
        """
        pass
