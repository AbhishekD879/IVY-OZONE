import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1473951_Verify_UK_Tote_tab_switcher_navigation(Common):
    """
    TR_ID: C1473951
    NAME: Verify UK Tote tab switcher navigation
    DESCRIPTION: This test case verifies the presence of the UK Tote tab & navigation through available tote types using the switcher
    PRECONDITIONS: Horse Racing Events with at least one UK Tote pool are available (Exacta, Trifecta, Quadpot, Placepot, Jackpot, Scoop 6)
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    PRECONDITIONS: Enable UK Tote feature in CMS (check the checkbox) and save changes
    """
    keep_browser_open = True

    def test_001_navigate_to_hr_edp(self):
        """
        DESCRIPTION: Navigate to HR EDP
        EXPECTED: * "Totepools" tab is available
        EXPECTED: * "Totepools" tab is displayed after main market tabs
        """
        pass

    def test_002_tap_on_the_totepools_tab(self):
        """
        DESCRIPTION: Tap on the "Totepools" Tab
        EXPECTED: * Tab is loaded;
        EXPECTED: * First UK Tote pool tab is selected by default, and underlined;
        EXPECTED: * All UK tote subtabs are displayed in the following order, depending on tote type availability:
        EXPECTED: * Win
        EXPECTED: * Place
        EXPECTED: * Exacta
        EXPECTED: * Trifecta
        EXPECTED: * Quadpot
        EXPECTED: * Placepot
        EXPECTED: * Jackpot
        EXPECTED: * Scoop 6
        """
        pass

    def test_003_on_mobile_only_scroll_through_the_available_uk_tote_subtabs(self):
        """
        DESCRIPTION: On Mobile only, scroll through the available UK tote subtabs
        EXPECTED: Tote subtabs should be horizontally scrollable.
        """
        pass

    def test_004_tap_on_each_available_uk_tote_subtab(self):
        """
        DESCRIPTION: Tap on each available UK tote subtab
        EXPECTED: * Every UK tote subtab loads the correct UK tote type;
        EXPECTED: * The selected UK tote subtab is underlined per the design.
        """
        pass

    def test_005_desktop_navigate_to_hr_landing_page_click_build_a_racecard_button_select_at_least_one_event_with_totepool_are_available_click_build_your_racecard_button_repeat_steps_2_and_4(self):
        """
        DESCRIPTION: **Desktop**
        DESCRIPTION: * Navigate to HR landing page:
        DESCRIPTION: * Click 'Build a Racecard' button
        DESCRIPTION: * Select at least one Event with Totepool are available
        DESCRIPTION: * Click 'Build Your Racecard' button
        DESCRIPTION: * Repeat steps 2 and 4
        EXPECTED: 
        """
        pass
