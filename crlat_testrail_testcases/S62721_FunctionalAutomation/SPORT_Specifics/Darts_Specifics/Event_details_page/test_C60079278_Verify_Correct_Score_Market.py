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
class Test_C60079278_Verify_Correct_Score_Market(Common):
    """
    TR_ID: C60079278
    NAME: Verify Correct Score Market
    DESCRIPTION: This test case verifies Correct Score Market for 'Darts' Sport.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapdarts_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Darts' icon on the Sports Menu Ribbon
        EXPECTED: *   Darts Landing Page is opened
        EXPECTED: *   **Matches** ->''**Today**' tab is opened by default (for desktop)/ 'Matches' tab is opened (for mobile)
        """
        pass

    def test_003_tap_on_one_event(self):
        """
        DESCRIPTION: Tap on one Event
        EXPECTED: Event page is opened
        """
        pass

    def test_004_tap_on_score_markets_tabexpand_correct_score_market(self):
        """
        DESCRIPTION: Tap on "SCORE MARKETS" tab
        DESCRIPTION: Expand "CORRECT SCORE" market
        EXPECTED: "CORRECT SCORE" market is expanded
        """
        pass

    def test_005_verify_correct_score_market_layout(self):
        """
        DESCRIPTION: Verify "CORRECT SCORE" market layout
        EXPECTED: "CORRECT SCORE" market is composed by:
        EXPECTED: *  **Title** - "CORRECT SCORE"
        EXPECTED: *  **Player's Names**
        EXPECTED: *  **Drop-down boxes below each name** and box with price on the right side
        EXPECTED: *  **"SHOW ALL" hyperlink**
        EXPECTED: *  **White boxes with different scores and box below with respective price**
        """
        pass

    def test_006_tap_show_all_hyperlink(self):
        """
        DESCRIPTION: Tap "SHOW ALL" hyperlink
        EXPECTED: List with all kinds of Odds should be displayed
        EXPECTED: SHOW LESS hyperlink replaces previous hyperlink
        """
        pass

    def test_007_verify_all_possible_combinations_by_selecting_different_items_from_drop_down_boxes_below_players_names(self):
        """
        DESCRIPTION: Verify all possible combinations by selecting different items from drop-down boxes below player's names
        EXPECTED: - All numbers are possible to select from Drop-down boxes
        EXPECTED: - Price on the right side is updated accordingly
        """
        pass

    def test_008_tap_on_show_less_hyperlink(self):
        """
        DESCRIPTION: Tap on "SHOW LESS" hyperlink
        EXPECTED: Verify that Prices shown below are collapsed and SHOW ALL hyperlink replaces previous hyperlink
        """
        pass

    def test_009_tap_on_price_on_the_right_side_and_place_bet(self):
        """
        DESCRIPTION: Tap on price on the right side and place bet
        EXPECTED: The bet is successfully placed
        """
        pass
