import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.lotto
@vtest
class Test_C29586_Select_Draw_Opions(Common):
    """
    TR_ID: C29586
    NAME: Select Draw Opions
    DESCRIPTION: This Test Case verifies Select Draw Options for Lotteries.
    DESCRIPTION: **Jira Ticket:**
    DESCRIPTION: BMA-2329 'Lottery - Select draw options'
    DESCRIPTION: BMA-7414 'Lotto - select draw bug'
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: **NOTE** :
    PRECONDITIONS: *   for all Lotteries all available 'Draw' options for the next t days (7*24=168) are displayed in ascending (in two columns)
    PRECONDITIONS: *   except of two lotteries , i.e. '49's' & 'Daily Million', for which we display only two earliest 'Draw' options
    """
    keep_browser_open = True

    def test_001_tap_on_lotto_icon_from_sports_menu_ribbon_or_a_z_page(self):
        """
        DESCRIPTION: Tap on 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: *   'Lotto' page is opened.
        EXPECTED: *   Lottery with the upcoming Draw is selected by default.
        """
        pass

    def test_002_navigate_to_options_panel(self):
        """
        DESCRIPTION: Navigate to 'Options' panel
        EXPECTED: *   'Options' panel is displayed and expanded by default.
        EXPECTED: *   'Select Draw' label is displayed under panel's header.
        EXPECTED: *   The list of all draws availble for the selected Lottery is displayed according to attributes 'openAtTime' & 'shutAtTime'
        EXPECTED: *   Draw name is taken from 'description' attribute on the draw level from SS response.
        EXPECTED: *   Each unique draw description is displayed with a checkbox alongside it.
        EXPECTED: *   The next availabel draw is selected by default.
        EXPECTED: *   'How Long Would You Like To Play For?' label is displayed under all available draws.
        EXPECTED: *   1 Week (selected by default), 2 Weeks, 4 Weeks and 8 Weeks buttons are displayed at the bottom of the section.
        """
        pass

    def test_003_collapseexpand_the_panelby_tapping_on_its_header(self):
        """
        DESCRIPTION: Collapse/Expand the panel by tapping on it's header
        EXPECTED: It is possible to collapse/expand the panel.
        """
        pass

    def test_004_select_another_lottery(self):
        """
        DESCRIPTION: Select another Lottery
        EXPECTED: Appropriate draw descriptions taken from SS are displayed within Options section.
        """
        pass

    def test_005_uncheck_selected_by_default_draws_checkbox_and_tap_on_place_bet_for_button(self):
        """
        DESCRIPTION: Uncheck selected by default draw's checkbox and tap on 'Place Bet for' button
        EXPECTED: * Button to place bet is disabled
        """
        pass

    def test_006_check_out_several_available_draws(self):
        """
        DESCRIPTION: Check out several available draws
        EXPECTED: User has ability to select multiple draws.
        """
        pass

    def test_007_select_lottery_without_any_draws_available(self):
        """
        DESCRIPTION: Select Lottery without any draws available
        EXPECTED: Whole Options section should not be displayed on front end at all.
        """
        pass
