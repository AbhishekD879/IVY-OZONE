import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C29013_Removing_Single_Selections_From_Bet_Slip(Common):
    """
    TR_ID: C29013
    NAME: Removing Single Selections From Bet Slip
    DESCRIPTION: This test case verifies removing of <Sport> selections from Bet Slip.
    PRECONDITIONS: 1.  User can be logged in or logged out
    PRECONDITIONS: 2.  A few single bets should be placed in the Bet Slip
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapsport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: - <Sport> Landing Page is opened
        EXPECTED: - 'Today' tab is opened by default
        """
        pass

    def test_003_make_a_few_single_selections_from_the_sport_landing_page(self):
        """
        DESCRIPTION: Make a few single selections from the <Sport> Landing Page
        EXPECTED: 
        """
        pass

    def test_004_go_to_the_bet_slip_and_enter_stakes_for_added_selections(self):
        """
        DESCRIPTION: Go to the Bet Slip and enter Stakes for added selections
        EXPECTED: - Bet Slip page is opened.
        EXPECTED: - Selections are displayed in Bet Slip
        EXPECTED: - Stakes are entered
        """
        pass

    def test_005_remove_one_of_the_selections_via_x_button_within_selection_section(self):
        """
        DESCRIPTION: Remove one of the selections via 'x' button within selection section
        EXPECTED: 1.  Bet is removed from the Bet Slip
        EXPECTED: 2.  The counter in the 'Single' section header is decremented by 1
        EXPECTED: 3.  The betslip counter in the Global Header is decremented by 1
        EXPECTED: 4.  The 'Total Stake' field is decremented by stake defined in the bet removed
        EXPECTED: 5.  The 'Total Est. Returns' field is decremented by the estimated return in bet removed
        """
        pass

    def test_006_unselect_one_of_the_selections_from_the_event_page___go_to_the_betslip(self):
        """
        DESCRIPTION: Unselect one of the selections from the event page -> go to the Betslip
        EXPECTED: 1.  Bet is no more displayed on the Bet Slip
        EXPECTED: 2.  Your Selections] section header is decremented by 1
        EXPECTED: 3.  The betslip counter in the Global Header is decremented by 1
        EXPECTED: 4.  The 'Total Stake' field is decremented by stake defined in the bet removed
        EXPECTED: 5.  The 'Total Est. Returns' field is decremented by the estimated return in bet removed
        """
        pass

    def test_007_remove_all_selections_via_x_button_within_each_selection_section(self):
        """
        DESCRIPTION: Remove all selections via 'x' button within each selection section
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  Betslip Overlay is closed (**for Mobile**)
        EXPECTED: 3.  The following message is displayed on the Betslip widget (**for Tablet and Mobile**): ***'You have no selections in the slip.'***
        """
        pass

    def test_008_add_only_one_bet_to_the_betslip(self):
        """
        DESCRIPTION: Add ONLY one bet to the betslip
        EXPECTED: 
        """
        pass

    def test_009_go_to_the_bet_slip___remove_selection_via_x_button(self):
        """
        DESCRIPTION: Go to the Bet Slip -> remove selection via 'x' button
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  Betslip Overlay is closed (**for Mobile**)
        EXPECTED: 3.  The following message is displayed on the Betslip widget (**for Tablet and Mobile**): ***'You have no selections in the slip.'***
        """
        pass

    def test_010_add_selection_to_the_bet_slip_from_the_event_details_page(self):
        """
        DESCRIPTION: Add selection to the Bet Slip from the event details page
        EXPECTED: Selection is added
        """
        pass

    def test_011_repeat_steps__4___9(self):
        """
        DESCRIPTION: Repeat steps № 4 - 9
        EXPECTED: 
        """
        pass

    def test_012_navigate_to_in_play_pageadd_several_selections_from_different_events(self):
        """
        DESCRIPTION: Navigate to In-Play page
        DESCRIPTION: Add several selections from different events
        EXPECTED: 
        """
        pass

    def test_013_open_and_close_bet_slip(self):
        """
        DESCRIPTION: Open and close Bet Slip
        EXPECTED: 
        """
        pass

    def test_014_on_in_play_page_click_on_the_same_selections_again_to_remove_them_from_bet_slip(self):
        """
        DESCRIPTION: On In-Play page click on the same selections again to remove them from Bet Slip
        EXPECTED: 
        """
        pass

    def test_015_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  The following message is displayed on the Betslip: ***'You have no selections in the slip.'***
        """
        pass
