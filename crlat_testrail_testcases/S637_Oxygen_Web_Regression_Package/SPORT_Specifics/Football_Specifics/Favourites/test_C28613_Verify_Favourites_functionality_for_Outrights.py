import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28613_Verify_Favourites_functionality_for_Outrights(Common):
    """
    TR_ID: C28613
    NAME: Verify Favourites functionality for Outrights
    DESCRIPTION: This Test Case verified Favourites functionality for Outrights
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on Football icon from the Sports Menu Ribbon
        EXPECTED: Football landing page is opened
        """
        pass

    def test_003_tap_on_outrights_tab(self):
        """
        DESCRIPTION: Tap on Outrights tab
        EXPECTED: Outrights page is opened
        """
        pass

    def test_004_tap_on_competition_header(self):
        """
        DESCRIPTION: Tap on Competition header
        EXPECTED: - Competition header is expanded
        EXPECTED: - Outright and Relegation sections are shown
        EXPECTED: - There is no Favourites star near Outright events
        """
        pass

    def test_005_tap_on_outright_section(self):
        """
        DESCRIPTION: Tap on Outright section
        EXPECTED: Outright details page is opened
        """
        pass

    def test_006_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_the_bet_slip(self):
        """
        DESCRIPTION: Navigate to the Bet Slip
        EXPECTED: Selection added to the Bet Slip
        """
        pass

    def test_008_place_a_bet(self):
        """
        DESCRIPTION: Place a bet
        EXPECTED: - Bet Receipt page is opened
        EXPECTED: - Outrigth selection is shown on Bet Receipt page
        EXPECTED: - There is no Favourites star on Bet Receipt for Outright selection
        """
        pass

    def test_009_tap_on_done_button(self):
        """
        DESCRIPTION: Tap on Done button
        EXPECTED: 
        """
        pass

    def test_010_navigate_to_my_bets_cash_out_page(self):
        """
        DESCRIPTION: Navigate to My Bets->Cash Out page
        EXPECTED: - Cash Out tab is opened
        EXPECTED: - Outright selection is shown on Cash Out page
        EXPECTED: - There is no Favourites star for Outright selection
        """
        pass

    def test_011_tap_on_outright_name(self):
        """
        DESCRIPTION: Tap on Outright name
        EXPECTED: - Outright details page is opened
        EXPECTED: - My Bets tab is present
        """
        pass

    def test_012_tap_on_my_bets_tab(self):
        """
        DESCRIPTION: Tap on 'My Bets' tab
        EXPECTED: - 'My Bets' tab is opened
        EXPECTED: - Outright selection is shown on 'My Bets' tab
        EXPECTED: - There is no Favourites star
        """
        pass
