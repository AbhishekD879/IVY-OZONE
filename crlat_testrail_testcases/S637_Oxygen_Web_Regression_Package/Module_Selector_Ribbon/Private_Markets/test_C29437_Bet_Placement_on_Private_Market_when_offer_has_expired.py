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
class Test_C29437_Bet_Placement_on_Private_Market_when_offer_has_expired(Common):
    """
    TR_ID: C29437
    NAME: Bet Placement on Private Market when offer has expired
    DESCRIPTION: This test case verifies Bet Placement on Private Market when the offer has expired.
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

    def test_002_add_selection_from_private_market_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from private market to the Betslip
        EXPECTED: *   Selection is added
        EXPECTED: *   Betslip counter is increased **for mobile/tablet**
        """
        pass

    def test_003_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: *   Betslip page is opened
        EXPECTED: *   Added selection is displayed
        """
        pass

    def test_004_trigger_the_situation_of_expiring_private_market_offer_from_step_21_set_offer_end_date2_set_entry_expiration_date_for_the_offer3_set_access_token_expiration_date4_wait_some_time_so_all__3_dates_from_points_above_are_set_in_the_past5_make_sure_that_all_dates_that_could_be_found_in_the_offer_are_set_in_the_past___so_after_that_offer_could_be_called_as_expired_changing_time_in_offer_does_not_count(self):
        """
        DESCRIPTION: Trigger the situation of expiring private market offer from step #2:
        DESCRIPTION: 1. Set offer end date
        DESCRIPTION: 2. Set Entry expiration Date for the offer
        DESCRIPTION: 3. Set Access token expiration date
        DESCRIPTION: 4. Wait some time so all  3 dates from points above are set in the past;
        DESCRIPTION: 5. Make sure that all dates that could be found in the offer are set in the past - so after that offer could be called as expired (changing time in offer does not count)
        EXPECTED: Private market offer becomes expired
        """
        pass

    def test_005_enter_stake_in_stake_field(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field
        EXPECTED: 
        """
        pass

    def test_006_clicktap_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Now' button
        EXPECTED: *   Error message that informs about expired private market offer is displayed
        EXPECTED: *   Impossible to place a bet on outcome from expired private market
        """
        pass
