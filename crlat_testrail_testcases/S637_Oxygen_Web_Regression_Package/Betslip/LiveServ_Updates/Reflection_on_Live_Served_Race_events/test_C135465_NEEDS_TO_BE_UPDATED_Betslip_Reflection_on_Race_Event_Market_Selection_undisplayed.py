import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C135465_NEEDS_TO_BE_UPDATED_Betslip_Reflection_on_Race_Event_Market_Selection_undisplayed(Common):
    """
    TR_ID: C135465
    NAME: [NEEDS TO BE UPDATED] Betslip Reflection on <Race> Event/Market/Selection undisplayed
    DESCRIPTION: This test case verifies betslip reflection on <Race> Event/Market/Section undisplayed
    DESCRIPTION: Please review and update according to the
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-54399
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    PRECONDITIONS: User is logged in with user account with positive balance
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports ribbon
        EXPECTED: * <Race> landing page is opened
        EXPECTED: * 'Today' tab is selected
        EXPECTED: * Events for current day are displayed
        """
        pass

    def test_003_open_any_event_details_page(self):
        """
        DESCRIPTION: Open any event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_make_a_single_selection(self):
        """
        DESCRIPTION: Make a single selection
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_005_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: The selection is shown in the Betslip
        """
        pass

    def test_006_open_ob_backoffice_and_undisplay_the_event_to_which_the_selection_belongs_save(self):
        """
        DESCRIPTION: Open OB Backoffice and undisplay the event, to which the selection belongs, save
        EXPECTED: The event becomes undisplayed in OB Backoffice
        """
        pass

    def test_007_check_betslip(self):
        """
        DESCRIPTION: Check Betslip
        EXPECTED: The selection is still displayed in the Betslip
        """
        pass

    def test_008_enter_stake_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake and tap "Bet Now" button
        EXPECTED: The bet is placed successfully
        EXPECTED: Bet receipt with all information regarding the bet appears in the Betslip
        """
        pass

    def test_009_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'Reuse selection'
        EXPECTED: Betslip is opened
        EXPECTED: 'Your Betslip is empty. Please add one or more selections to place a bet' message is shown
        EXPECTED: For Mobile, 'Go Betting' button is shown
        """
        pass

    def test_010_go_to_a_race_landing_page_and_add_a_few_selections_from_different_active_events_in_order_to_form_a_multiples_sectionopen_betslip(self):
        """
        DESCRIPTION: Go to a <Race> landing page and add a few selections from different active events in order to form a 'Multiples' section
        DESCRIPTION: Open Betslip
        EXPECTED: 'Multiples' section is shown in the Betslip
        """
        pass

    def test_011_open_ob_backoffice_and_undisplay_the_event_to_which_the_selection_belongsclick_save(self):
        """
        DESCRIPTION: Open OB Backoffice and undisplay the event, to which the selection belongs
        DESCRIPTION: Click "Save"
        EXPECTED: The event becomes undisplayed in OB Backoffice
        """
        pass

    def test_012_without_refreshing_check_the_betslip(self):
        """
        DESCRIPTION: **Without refreshing**, check the Betslip
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: * No error messages appear
        EXPECTED: * The selection, which became undisplayed, is still visible in the Betslip
        """
        pass

    def test_013_go_to_tomorrow_tab(self):
        """
        DESCRIPTION: Go to 'Tomorrow' tab
        EXPECTED: Tomorrow events are displayed
        """
        pass

    def test_014_repeat_steps_3_12(self):
        """
        DESCRIPTION: Repeat steps 3-12
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_10_11_and_refresh_the_pagecheck_the_betslip(self):
        """
        DESCRIPTION: Repeat steps 10-11 **and refresh the page**
        DESCRIPTION: Check the Betslip
        EXPECTED: * There are no selections from undisplayed event neither in the 'Multiples' section nor in the 'Singles' section
        EXPECTED: * Multiples are rebuilt using only active selections
        EXPECTED: * No error messages appear
        """
        pass

    def test_016_repeat_steps_3_15_but_instead_of_undisplaying_an_event_undisplay_a_market(self):
        """
        DESCRIPTION: Repeat steps 3-15 but instead of undisplaying an event, undisplay a market
        EXPECTED: 
        """
        pass

    def test_017_repeat_steps_3_15_but_instead_of_undisplaying_an_event_undisplay_a_selection(self):
        """
        DESCRIPTION: Repeat steps 3-15 but instead of undisplaying an event, undisplay a selection
        EXPECTED: 
        """
        pass
