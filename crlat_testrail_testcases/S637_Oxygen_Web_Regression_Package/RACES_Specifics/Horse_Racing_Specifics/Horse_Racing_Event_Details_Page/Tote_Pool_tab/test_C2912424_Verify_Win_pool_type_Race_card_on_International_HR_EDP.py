import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2912424_Verify_Win_pool_type_Race_card_on_International_HR_EDP(Common):
    """
    TR_ID: C2912424
    NAME: Verify Win pool type Race card on International HR EDP
    DESCRIPTION: This test case verifies the Race card of Win pool type of International Tote
    PRECONDITIONS: * User should have a International HR EDP open ("Tote" tab)
    PRECONDITIONS: * Event should have Win pool type  available
    """
    keep_browser_open = True

    def test_001_select_win_tab(self):
        """
        DESCRIPTION: Select "Win" tab
        EXPECTED: * "Win" tab is selected
        EXPECTED: * Win racecard is shown
        """
        pass

    def test_002_verify_win_racecard_for_an_active_event(self):
        """
        DESCRIPTION: Verify Win racecard for an **active** event
        EXPECTED: Win racecard consists of:
        EXPECTED: * Current pool value (only shown if available)
        EXPECTED: * Runner number, name and information for each runner
        EXPECTED: * Runner silks (if available) for each runner
        EXPECTED: * Win grey button/selection for each runner
        """
        pass

    def test_003_refresh_the_page_after_current_pool_value_changes(self):
        """
        DESCRIPTION: Refresh the page **after** current pool value changes
        EXPECTED: * Current pool value is updated upon page refresh
        """
        pass

    def test_004_lick_on_spotlight_downward_arrow_or_form_options_under_individual_selections(self):
        """
        DESCRIPTION: Сlick on spotlight (downward arrow) or form options under individual selections
        EXPECTED: The spotlight and form information under the selection are shown to the user
        """
        pass

    def test_005_select_any_runner_press_win_button(self):
        """
        DESCRIPTION: Select any runner (press Win button)
        EXPECTED: * Button becomes green/selected
        EXPECTED: * All other buttons remain grey
        EXPECTED: * Bet builder appears at the bottom with enabled 'Add to betslip' button and Clear selection link
        EXPECTED: * Bet builder shows corresponding number of selections that are selected
        """
        pass

    def test_006_unselect_the_win_button(self):
        """
        DESCRIPTION: Unselect the Win button
        EXPECTED: * The becomes unselected (grey)
        EXPECTED: * Bet builder disappears
        EXPECTED: * Footer menu is shown at the bottom
        """
        pass

    def test_007_select_several_runnersselections(self):
        """
        DESCRIPTION: Select several runners/selections
        EXPECTED: * Win buttons become selected
        EXPECTED: * Bet builder appears at the bottom with enabled 'Add to betslip' button and Clear selection link
        EXPECTED: * Bet builder shows corresponding number of selections that are selected
        """
        pass

    def test_008_uncheck_1_or_2_buttons_but_not_all(self):
        """
        DESCRIPTION: Uncheck 1 or 2 buttons (but not all)
        EXPECTED: * Corresponding selections become unselected except those that are selected
        EXPECTED: * Bet builder shows corresponding number of selections that are selected
        """
        pass
