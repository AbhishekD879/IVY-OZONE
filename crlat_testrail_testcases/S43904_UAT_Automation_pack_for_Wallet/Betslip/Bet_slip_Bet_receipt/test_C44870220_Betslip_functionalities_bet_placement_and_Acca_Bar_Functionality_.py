import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870220_Betslip_functionalities_bet_placement_and_Acca_Bar_Functionality_(Common):
    """
    TR_ID: C44870220
    NAME: "Betslip functionalities bet placement and Acca Bar Functionality "
    DESCRIPTION: 
    PRECONDITIONS: Customer can view the Bet slip logged in or logged out
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: User can able to launch the app
        """
        pass

    def test_002_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: User must be displayed Quick bet Pop up
        EXPECTED: -User sees Add to bet slip and Login and place a bet buttons
        EXPECTED: For desktop: the selection is added to the betslip.
        """
        pass

    def test_003_verify_bet_slip_icon(self):
        """
        DESCRIPTION: Verify Bet slip icon
        EXPECTED: -'Bet Slip' icon consists Bet Slip counter bubble
        EXPECTED: -If no selections added to Bet Slip, Bet slip bubble is not shown at all
        """
        pass

    def test_004_tap_the_bet_slip_icon_add_a_few_selections_to_bet_slip(self):
        """
        DESCRIPTION: Tap the 'Bet Slip' icon ,Add a few selections to Bet slip
        EXPECTED: Bet Slip is opened,
        EXPECTED: -Selections are added
        EXPECTED: -Bet slip icon is present
        """
        pass

    def test_005_remove_all_selection_from_bet_slip_and_log_outverify_bet_slip_icon(self):
        """
        DESCRIPTION: Remove all selection from Bet slip and log out,Verify Bet slip icon
        EXPECTED: User is logged out ,Verify Bet slip icon and Bet slip icon is not displayed
        """
        pass

    def test_006_add_any_selection_from_a_sport_to_the_bet_slip(self):
        """
        DESCRIPTION: Add any selection from a sport to the Bet Slip
        EXPECTED: Bet Slip counter is 1
        """
        pass

    def test_007_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: The 'Your Selections (1)' section is shown with "REMOVE ALL" next to it
        EXPECTED: Added selection is displayed
        """
        pass

    def test_008_add_one_more_selection_from_another_sport_races_event(self):
        """
        DESCRIPTION: Add one more selection from another Sport ,Races event
        EXPECTED: Bet Slip counter is 2
        """
        pass

    def test_009_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: 'Your Selections (2)' section is shown with  "REMOVE ALL" next to it
        EXPECTED: 'All single stakes' label and edit box appears in Singles section
        EXPECTED: The 'Multiples' section is shown under the selections. available multiples bets is shown
        """
        pass

    def test_010_add_one_more_selections_from_another_sports_races_event(self):
        """
        DESCRIPTION: Add one more selections from another Sports, Races event
        EXPECTED: Bet Slip counter is 3
        """
        pass

    def test_011_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: 'All single stakes' label and edit box appears in Singles section
        EXPECTED: The Multiples section is displayed and contains (e.g. Treble 1, Double 3, Trixie 4 & Patent 7)
        """
        pass

    def test_012_user_is_able_to_place_a_bet_for_single_multiples_from_pre_playin_play_tricast_hrgh_and_forecasthrgh(self):
        """
        DESCRIPTION: User is able to place a bet for single, multiples (from pre play,In play), Tricast (HR/GH) and forecast(HR/GH)
        EXPECTED: User Successfully placed bets
        """
        pass

    def test_013_acca_bar_functionality__applicable_for_mobile_onlyload_coral_siteapp_and_add_one_selection_to_bet_slip_and_check_that_acca_price_price_bar_is_not_displayedx(self):
        """
        DESCRIPTION: Acca Bar Functionality : Applicable for mobile only.
        DESCRIPTION: Load Coral site/app and Add one selection to bet slip and check that Acca Price price bar is not displayedx
        EXPECTED: User is displayed Coral site/app then Selection is added to bet slip, no special feature observed
        """
        pass

    def test_014_add_more_selections_to_bet_slip_and_observe_each_time_if_acca_price_price_bar_is_displayed(self):
        """
        DESCRIPTION: Add more selections to bet slip and observe each time if Acca Price price bar is displayed
        EXPECTED: Acca Price price bar is displayed as soon as the second selection is added, and is updated each time a new selection is added
        """
        pass

    def test_015_navigate_in_site_to_observe_acca_price_bar_displayed(self):
        """
        DESCRIPTION: Navigate in site to observe Acca Price Bar displayed
        EXPECTED: Acca price bar will show during navigation to pages that have odds on them
        """
        pass

    def test_016_verify_the_acca_price_price_bar_shows_correct_data_and_updates_accordingly_when_adding_selection(self):
        """
        DESCRIPTION: Verify the Acca Price price bar shows correct data and updates accordingly when adding selection
        EXPECTED: User must see:
        EXPECTED: - bet type: Double, Treble..
        EXPECTED: - number of selections for Acca
        EXPECTED: - updated odds, in fractions by default
        EXPECTED: - potential returns for a £1 stake
        EXPECTED: - for SP - N/A
        """
        pass

    def test_017_verify_the_acca_price_price_bar_shows_correct_data_and_updates_accordingly_when_deleting_selection(self):
        """
        DESCRIPTION: Verify the Acca Price price bar shows correct data and updates accordingly when deleting selection
        EXPECTED: User must see:
        EXPECTED: - bet type: Double, Treble..
        EXPECTED: - number of selections in brackets for Acca
        EXPECTED: - updated odds, in fractions by default
        EXPECTED: - potential returns for a £1 stake
        EXPECTED: - for SP - N/A
        """
        pass
