import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58449388_Featured_Module__Bet_Placement_of_Virtual_Sports_Verification_for_Horse_racing_Greyhounds_by_Race_TypeID(Common):
    """
    TR_ID: C58449388
    NAME: Featured Module - Bet Placement of Virtual Sports Verification for Horse racing/Greyhounds by <Race> TypeID
    DESCRIPTION: This test case verifies bet placement on Virtual Horses/Greyhounds from Featured module.
    PRECONDITIONS: Login with user account that has positive balance.
    """
    keep_browser_open = True

    def test_001_load_application_and_reach_featured_module_on_the_home_page(self):
        """
        DESCRIPTION: Load application and reach "Featured module" on the Home Page.
        EXPECTED: 
        """
        pass

    def test_002_find_virtual_horsesgreyhounds_event_and_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Find Virtual Horses/Greyhounds event and add selection to the Betslip.
        EXPECTED: Selected 'Price/Odds' buttons are highlighted in green
        EXPECTED: Betslip counter is increased.
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selections with bet details are displayed in the Betlsip
        EXPECTED: Selections are present in Section 'Singles (2)'
        EXPECTED: 'Multiples(1)' section contains multiples calculated based on added selections
        """
        pass

    def test_004_set_stake_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Set "Stake" and tap 'Place Bet' button
        EXPECTED: Bet is placed
        EXPECTED: Bet receipt appears in Betslip
        EXPECTED: 'Reuse selections' and 'Go Betting' buttons are present in footer.
        """
        pass
