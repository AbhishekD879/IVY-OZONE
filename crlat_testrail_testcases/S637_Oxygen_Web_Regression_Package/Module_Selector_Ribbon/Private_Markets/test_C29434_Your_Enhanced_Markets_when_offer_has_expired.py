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
class Test_C29434_Your_Enhanced_Markets_when_offer_has_expired(Common):
    """
    TR_ID: C29434
    NAME: 'Your Enhanced Markets' when offer has expired
    DESCRIPTION: This test case verifies 'Your Enhanced Markets' when offer has expired.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
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

    def test_002_trigger_the_situation_of_expiring_one_of_the_private_markets_offer1_set_offer_end_date2_set_entry_expiration_date_for_the_offer3_set_access_token_expiration_date4_wait_some_time_so_all__3_dates_from_points_above_are_set_in_the_past5_make_sure_that_all_dates_that_could_be_found_in_the_offer_are_set_in_the_past___so_after_that_offer_could_be_called_as_expired_it_is_ob___so_non_logic_behavior_is_expected_even_if_you_think_its_ridiculous_its_ok(self):
        """
        DESCRIPTION: Trigger the situation of expiring one of the private markets offer:
        DESCRIPTION: 1. Set offer end date
        DESCRIPTION: 2. Set Entry expiration Date for the offer
        DESCRIPTION: 3. Set Access token expiration date
        DESCRIPTION: 4. Wait some time so all  3 dates from points above are set in the past;
        DESCRIPTION: 5. Make sure that all dates that could be found in the offer are set in the past - so after that offer could be called as expired (It is OB - so non-logic behavior is expected, even if you think it's ridiculous it's ok)
        EXPECTED: The private market offer becomes expired:
        """
        pass

    def test_003_verify_your_enhancedmarkets_tabsection_for_which_offer_has_expired_after_page_refresh(self):
        """
        DESCRIPTION: Verify 'Your Enhanced Markets' tab/section for which offer has expired after page refresh
        EXPECTED: *   Expired private market is no more shown within 'Your Enhanced Markets' tab/section (in case there were two or more markets available)
        EXPECTED: *   'Your Enhanced Markets' tab/section is no more shown (in case verified private market was the only one to be shown)
        EXPECTED: *  'Featured' (or other tab with highest priority in the Module Selector Ribbon list) tab is selected by default **for mobile/tablet**
        EXPECTED: * 'In-Play & Live Stream' section is displayed at the top of the page **for desktop**
        """
        pass
