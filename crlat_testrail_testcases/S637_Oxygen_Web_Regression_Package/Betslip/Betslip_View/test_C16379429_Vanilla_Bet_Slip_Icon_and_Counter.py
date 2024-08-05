import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C16379429_Vanilla_Bet_Slip_Icon_and_Counter(Common):
    """
    TR_ID: C16379429
    NAME: [Vanilla] 'Bet Slip' Icon and Counter
    DESCRIPTION: This scenario verifies functionality of Bet slip icon which is shown after a user has added a selection to the Bet Slip
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-11597 UI FEEDBACK - Header
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_verify_betslip_icon(self):
        """
        DESCRIPTION: Verify Betslip icon
        EXPECTED: *   'Bet Slip' icon consists Bet Slip counter bubble
        EXPECTED: *   If no selections added to Bet Slip, Betslip counter bubble shows '0'
        """
        pass

    def test_003_tap_sportrace_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport>/<Race> icon from the Sports Menu Ribbon
        EXPECTED: <Sport>/<Races> landing page is opened
        """
        pass

    def test_004_open_event_details_page(self):
        """
        DESCRIPTION: Open Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_tap_priceodds_button_for_outcome(self):
        """
        DESCRIPTION: Tap Price/Odds button for outcome
        EXPECTED: 'Bet Slip' bubble is present and it displays 1
        """
        pass

    def test_006_tap_the_bet_slip_icon(self):
        """
        DESCRIPTION: Tap the 'Bet Slip' icon
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_007_go_back_to_the_event_details_page___unselect_just_selected_priceodds_button(self):
        """
        DESCRIPTION: Go back to the Event details page -> unselect just selected Price/Odds button
        EXPECTED: 'Bet Slip' bubble shows '0'
        """
        pass

    def test_008_add_2_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 2 selections to the Bet Slip
        EXPECTED: 'Bet Slip' bubble displays the figure '2'
        """
        pass

    def test_009_unselect_one_just_selected_priceodds_button(self):
        """
        DESCRIPTION: Unselect one just-selected Price/Odds button
        EXPECTED: 'Bet Slip' bubble is decreased by 1
        """
        pass

    def test_010_add_maximum_quantity_of_selections_to_the_bet_slip_which_is_set_in_cms_system_configuration__structure__bet_slip(self):
        """
        DESCRIPTION: Add maximum quantity of selections to the Bet Slip, which is set in CMS (System Configuration-> Structure ->Bet Slip)
        EXPECTED: 'Bet Slip' bubble displays the maximum numbers of selections
        """
        pass

    def test_011_add_one_more_selection(self):
        """
        DESCRIPTION: Add one more selection
        EXPECTED: *   Warning message is shown and consist of:
        EXPECTED: - header - 'Betslip Full'
        EXPECTED: - message 'Maximum number of selections allowed on betslip is 20'
        EXPECTED: *   'Bet Slip' bubble is not changed
        """
        pass

    def test_012_remove_all_selection_from_betslip_and_log_out(self):
        """
        DESCRIPTION: Remove all selection from Betslip and log out
        EXPECTED: User is logged out
        """
        pass

    def test_013_verify_betslip_icon(self):
        """
        DESCRIPTION: Verify Betslip icon
        EXPECTED: * Betslip icon is not displayed (only for IOS native app)
        EXPECTED: * For Mobile WEB browsers (Safari, Chrome), Android app betslip icon (bubble) is displayed - regarding to BMA-48643
        """
        pass

    def test_014_add_a_few_selections_to_betslip(self):
        """
        DESCRIPTION: Add a few selections to Betslip
        EXPECTED: *   Selections are added
        EXPECTED: *   Betslip icon is present
        """
        pass

    def test_015_log_in_and_verify_betslip_icon(self):
        """
        DESCRIPTION: Log in and verify Betslip icon
        EXPECTED: *   Betslip icon is present
        EXPECTED: *   Betslip bubble diplays number of selections added on step №14
        """
        pass
