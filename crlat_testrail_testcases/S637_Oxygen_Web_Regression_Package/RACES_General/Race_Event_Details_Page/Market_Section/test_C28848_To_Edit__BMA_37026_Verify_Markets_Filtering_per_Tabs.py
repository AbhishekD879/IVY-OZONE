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
class Test_C28848_To_Edit__BMA_37026_Verify_Markets_Filtering_per_Tabs(Common):
    """
    TR_ID: C28848
    NAME: [To Edit - BMA-37026] Verify Market's Filtering per Tabs
    DESCRIPTION: This test case verifies market's filtering per tabs
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 - Racecard Layout Update - Markets and Selections area
    PRECONDITIONS: To retrieve an information from Site Server use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: See attribute:
    PRECONDITIONS: 'name' attribute in the market level to see market name
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: *   Event details page is opened
        EXPECTED: *   'Win or E/W' tab is opened by default
        EXPECTED: *   Tab is expanded by default and not collapsible
        """
        pass

    def test_004_verify_win_or_ew_tab(self):
        """
        DESCRIPTION: Verify 'Win or E/W' tab
        EXPECTED: *   Market with **'name' = 'Win or Each Way'** is shown (**'name'** attribute on market level)
        EXPECTED: *   All outcomes within market are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab is not shown
        """
        pass

    def test_005_tap_win_only_tab(self):
        """
        DESCRIPTION: Tap 'Win Only' tab
        EXPECTED: 'Win Only' tab is expanded by default and not collapsible
        """
        pass

    def test_006_verify_win_only_tab(self):
        """
        DESCRIPTION: Verify 'Win Only' tab
        EXPECTED: *   Market with **'name' = 'Win Only'** is shown (**'name'** attribute on market level)
        EXPECTED: *   All outcomes within market are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab 'Win Only' is not shown
        """
        pass

    def test_007_tap_betting_wo_tab(self):
        """
        DESCRIPTION: Tap 'Betting WO' tab
        EXPECTED: *   The list of all available markets is shown
        EXPECTED: *   All markets are expanded by default
        EXPECTED: *   Each market is collapsible/expandable
        """
        pass

    def test_008_verify_betting_wo_tab(self):
        """
        DESCRIPTION: Verify 'Betting WO' tab
        EXPECTED: *   Markets with **'name' = 'Betting without XXXX' **are shown (e.g. 'Betting without Theatrical Style')
        EXPECTED: *   All outcomes within markets are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab 'Betting WO' is not shown
        """
        pass

    def test_009_tap_more_markets_tab(self):
        """
        DESCRIPTION: Tap 'More Markets' tab
        EXPECTED: *   The list of all available markets is shown
        EXPECTED: *   All markets are expanded by default
        EXPECTED: *   Each market is collapsible/expandable
        """
        pass

    def test_010_verify_more_markets_tab(self):
        """
        DESCRIPTION: Verify 'More Markets' tab
        EXPECTED: *   Markets which doesn't contain any** name = **Win or E/W', 'Win Only' or 'Betting WO appear in 'More markets' tab
        EXPECTED: *   All outcomes within markets are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab 'More Markets' is not shown
        """
        pass
