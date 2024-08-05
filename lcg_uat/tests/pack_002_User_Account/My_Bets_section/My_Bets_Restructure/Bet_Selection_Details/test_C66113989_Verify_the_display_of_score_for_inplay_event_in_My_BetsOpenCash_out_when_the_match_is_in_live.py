import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66113989_Verify_the_display_of_score_for_inplay_event_in_My_BetsOpenCash_out_when_the_match_is_in_live(Common):
    """
    TR_ID: C66113989
    NAME: Verify the display of score for inplay event in My Bets(Open,Cash out) when the match is in live
    DESCRIPTION: This testcase verifies the display of score for inplay event in My Bets(Open,Cash out) when the match is in live
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_place_bet_by_adding_selections_of_inplay_events_which_shows_dcore_updates_in_my_bets_area(self):
        """
        DESCRIPTION: Place bet by adding selections of inplay events which shows dcore updates in my bets area
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_the_display_of_score_for_inplay_event_in_open_tab_when_the_match_is_in_live(self):
        """
        DESCRIPTION: Verify the display of score for inplay event in Open tab when the match is in live
        EXPECTED: The score with be displayed with a grey background as per figma.
        EXPECTED: Football:
        EXPECTED: ![](index.php?/attachments/get/da843504-1822-4e00-bb97-bd9bea301f4a)
        EXPECTED: Tennis:
        EXPECTED: ![](index.php?/attachments/get/dfe633f4-47e5-4f91-96f3-50b16cada9c4)
        """
        pass

    def test_005_verify_the_display_of_score_for_inplay_event_in_cash_out_tab_when_the_match_is_in_live(self):
        """
        DESCRIPTION: Verify the display of score for inplay event in Cash out tab when the match is in live
        EXPECTED: The score with be displayed with a grey background as per figma.
        EXPECTED: Football:
        EXPECTED: ![](index.php?/attachments/get/f9c24a31-9461-4229-834e-dcb1a051cc40)
        EXPECTED: Tennis:
        EXPECTED: ![](index.php?/attachments/get/f2115230-fea8-407e-8e67-d571cc8cb12d)
        """
        pass

    def test_006_verify_the_display_of_score_for_inplay_event_in_settled_tab_when_the_match_is_in_live(self):
        """
        DESCRIPTION: Verify the display of score for inplay event in Settled tab when the match is in live.
        EXPECTED: The score with be displayed with a grey background as per figma.
        EXPECTED: Football:
        EXPECTED: ![](index.php?/attachments/get/c2a6fab4-aaef-47a5-9072-f6d57f0ccb14)
        EXPECTED: Tennis:
        EXPECTED: ![](index.php?/attachments/get/271d4ce2-331d-446b-a157-932ab59e1eda)
        """
        pass

    def test_007_repeat_3_7_with_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat 3-7 with Tier1 and Tier2 sports
        EXPECTED: Result should be same
        """
        pass
