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
class Test_C28119_Rebuild_Multiples_section(Common):
    """
    TR_ID: C28119
    NAME: Rebuild 'Multiples' section
    DESCRIPTION: This test case verifies rebuilding of 'Multiples' section
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-7831 RIGHT COLUMN: Display Betslip
    DESCRIPTION: *   BMA-8173 DESKTOP GLOBAL RIGHT COLUMN
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application_on_desktoptablet_device(self):
        """
        DESCRIPTION: Load Invictus application on desktop/tablet device
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_the_betslip_and_verify_betslip_widget(self):
        """
        DESCRIPTION: Add selection to the Betslip and verify Betslip widget
        EXPECTED: *   Added selection appears in 'Singles' section immediately
        EXPECTED: *   The counter in 'Singles' section header increases by 1 (**From OX99** 'Singles' title is removed. )
        """
        pass

    def test_003_add_a_few_selections_from_different_events_to_betslip(self):
        """
        DESCRIPTION: Add a few selections from different events to Betslip
        EXPECTED: *   Added selections appear in 'Singles' section immediately;  (**From OX99** 'Singles' title is removed.)
        EXPECTED: *   The counter on 'Singles' section header increases accordingly to quantity of added selection;  'Your selections: (n)' title ' is shown as a header, where n - quantity of added selection)
        EXPECTED: *   Available Multiple bets appear in 'Multiples' section immediately;
        EXPECTED: *   The counter on 'Multiples' section header increases accordingly to quantity of available bets.
        EXPECTED: *   'Place your ACCA' section is shown at the top of the betslip IF available (**From OX99**  'Place your ACCA' section is removed. ACCA bet is shown the first under the 'Multiples' section)
        """
        pass

    def test_004_remove_one_selection_via_corresponding_bin_iconfrom_ox99_via_x_button(self):
        """
        DESCRIPTION: Remove one selection via corresponding Bin icon (**From OX99** via 'X' button)
        EXPECTED: *   Selection is removed from 'Singles' section; (**From OX99** 'Singles' title is removed.)
        EXPECTED: *   The counter in the 'Single' section header is decremented by 1; (**From OX99**: 'Your selections: (n)' section header is decremented by 1)
        EXPECTED: *   'Multiples' section is rebuilt with available selections.
        EXPECTED: *   The counter in the 'Multiples' section header displays new quantity of available bets;
        EXPECTED: *   'Place your ACCA' section is shown at the top of the betslip IF available (**From OX99**  'Place your ACCA' section is removed. ACCA bet is shown the first under the 'Multiples' section)
        """
        pass

    def test_005_repeat_steps__2__3(self):
        """
        DESCRIPTION: Repeat steps # 2 -3
        EXPECTED: 
        """
        pass

    def test_006_unselect_one_bet_from_event_page(self):
        """
        DESCRIPTION: Unselect one bet from Event page
        EXPECTED: *   Bet is no more displayed in 'Singles' section; (**From OX99** 'Singles' title is removed.)
        EXPECTED: *   The counter in the 'Singles' section header is decremented by 1; (**From OX99**: 'Your selections: (n)' section header is decremented by 1)
        EXPECTED: *   'Multiples' section is rebuilt with available selections;
        EXPECTED: *   The counter in the 'Multiples' section header displays new quantity of available bets.
        EXPECTED: *   'Place your ACCA' section is shown at the top of the betslip IF available (**From OX99**  'Place your ACCA' section is removed. ACCA bet is shown the first under the 'Multiples' section)
        """
        pass

    def test_007_add_only_one_selection(self):
        """
        DESCRIPTION: Add Only one selection
        EXPECTED: *   Added selections appear in 'Singles' section immediately; (**From OX99** 'Singles' title is removed.)
        EXPECTED: *   The counter on 'Singles' section header increased by 1; (**From OX99**: 'Your selections: (n)' section header is increased by 1)
        EXPECTED: *   Available Multiple bets appear in 'Multiples' section immediately;
        EXPECTED: *   The counter on 'Multiples' section header increases accordingly to quantity of available bets.
        EXPECTED: *   'Place your ACCA' section is shown at the top of the betslip IF available(**From OX99**  'Place your ACCA' section is removed. ACCA bet is shown the first under the 'Multiples' section)
        """
        pass

    def test_008_tap_bin_icon_on_betslip_footer___tap_confirm_clear_betslipfrom_ox99bin_icon_on_betslip_footer_was_removedtap_remove_all_button_at_the_top_of_betslip_then_tap_continue_button_on_confirmation_removing_message(self):
        """
        DESCRIPTION: Tap Bin icon on betslip footer -> Tap 'Confirm Clear Betslip'
        DESCRIPTION: **From OX99**
        DESCRIPTION: Bin icon on betslip footer was removed.
        DESCRIPTION: Tap 'Remove All' button at the top of Betslip. Then tap 'Continue' button on confirmation removing message
        EXPECTED: *   All selections are removed from the Bet Slip
        EXPECTED: *   User stays on the 'Betslip' tab and sees the message: 'You have no selections in the slip.'
        """
        pass
