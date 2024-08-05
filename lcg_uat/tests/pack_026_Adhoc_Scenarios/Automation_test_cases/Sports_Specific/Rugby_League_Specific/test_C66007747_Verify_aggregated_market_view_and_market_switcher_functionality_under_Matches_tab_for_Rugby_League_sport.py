import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C66007747_Verify_aggregated_market_view_and_market_switcher_functionality_under_Matches_tab_for_Rugby_League_sport(Common):
    """
    TR_ID: C66007747
    NAME: Verify aggregated market view and market switcher functionality under Matches tab for Rugby League sport
    DESCRIPTION: To validate data displayed under Matches tab.
    PRECONDITIONS: In CMS, Sport pages-&gt; Sport Categories-&gt; Rugby league sport -&gt; Tabs and modules should be configured.
    PRECONDITIONS: Market switcher should be enabled in System Config -&gt; Structure -&gt; Market Switcher.
    PRECONDITIONS: Two Aggregated Markets should be added to Market Switcher label table on below path in CMS.
    PRECONDITIONS: Sports categories -&gt; Sport pages  -&gt; Rugby league -&gt; Matches -&gt; Market switcher Label section
    PRECONDITIONS: Config below 2 way markets as aggregated Market with display name "Game Lines"
    PRECONDITIONS: – Moneyline, Handicap, Total Points(2 way markets which has 2 selections)
    PRECONDITIONS: Config below 2 way markets as aggregated Market with display name "Game Lines 3-Way"
    PRECONDITIONS: – Moneyline 3-way, Handicap way, Total Points 3-way(3 way markets which has 3 selections)
    PRECONDITIONS: Note: Market aggregation should be done for either 2 way or 3-way markets only.
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        pass

    def test_002_navigate_to_rugby_league_sport(self):
        """
        DESCRIPTION: Navigate to Rugby league sport
        EXPECTED: Navigation should be successful.
        EXPECTED: By default application navigates to Matches tab/Today subtab.
        """
        pass

    def test_003_verify__market_switcher(self):
        """
        DESCRIPTION: Verify  Market Switcher.
        EXPECTED: If the aggregated market "Game Lines" is on top in market switcher label table, then it should be selected by default.
        EXPECTED: If Game Lines selected by default then aggregated markets should display on event card.
        """
        pass

    def test_004_verify_aggregated_market_view_on_event_card(self):
        """
        DESCRIPTION: Verify Aggregated Market view on event card.
        EXPECTED: Aggregated markets odds will be shown in same order which we set in Market switcher label table.
        EXPECTED: Markets names should be wrapped to second line (no more than 2 lines, any market that is longer than 2 lines we should use ellipses '...' and on mouse hovering it should display full name. for mobiles by clicking on market name it should display full name of markets.
        EXPECTED: For below Markets respective abbreviation should show in SLP not in edp markets.
        EXPECTED: No Draw Handicap 1    --&amp;gt; No Draw Hcap 1
        EXPECTED: No Draw Handicap 2    --&amp;gt; No Draw Hcap 2
        EXPECTED: No Draw Handicap 3    --&amp;gt; No Draw Hcap 3
        EXPECTED: Total Match Points    --&amp;gt; Total Points
        EXPECTED: Handicap Betting  --&amp;gt; Hcap
        EXPECTED: Handicap 2-way    --&amp;gt; Hcap 2-way
        EXPECTED: If we set Aggregated markets as Moneyline, Handicap, Total Points in MS label table then first money line markets odds should display then Handicap market followed by Total points.
        EXPECTED: For total points market if we have more markets i.e. Total points over and Under 5 and Total Points over and under 6 then Total Points over and Under 5 market selections should show on event card with aggregated view.
        EXPECTED: For Total points over and under markets selections "O" should show in Selection button prior to Over value selection and "U" for under selection.
        """
        pass

    def test_005_click_on_market_switcher(self):
        """
        DESCRIPTION: Click on Market Switcher.
        EXPECTED: Markets which are configured in market switcher labels table should display if we have events with configured markets.
        EXPECTED: If we don't have any single event with configured markets, that specific market shouldn't be shown in market switcher dropdown.
        """
        pass

    def test_006_verify_game_lines_3_way_on_market_switcher(self):
        """
        DESCRIPTION: Verify Game Lines 3-way on Market Switcher.
        EXPECTED: Result should be same step no 4.
        EXPECTED: For Game Lines 3-Way 3 odds should show.
        """
        pass

    def test_007_verify_other_markets_on_market_switcher(self):
        """
        DESCRIPTION: Verify other markets on Market Switcher.
        EXPECTED: Events should load with selected markets.
        """
        pass

    def test_008_switch_between_two_aggregated_markets_simultaneously(self):
        """
        DESCRIPTION: Switch between two aggregated markets simultaneously.
        EXPECTED: Respect market odds should load properly without page refresh.
        """
        pass

    def test_009_verify_multiple_types_of_bet_placements_on_game_lines_and_game_lines_3_way_marketseg_single_double_acca_etc(self):
        """
        DESCRIPTION: Verify multiple types of bet placements on Game Lines and Game Lines 3-way markets.
        DESCRIPTION: e.g. Single, double, Acca etc.
        EXPECTED: Bets should be placed successfully.
        """
        pass

    def test_010_switch_to_tomorrow_sub_tab_and_repeat_the_steps_3_9(self):
        """
        DESCRIPTION: Switch to Tomorrow sub tab and repeat the steps 3-9
        EXPECTED: Result should be same as expected.
        """
        pass

    def test_011_now_switch_to_future_sub_tab_and_repeat_the_steps_3_9(self):
        """
        DESCRIPTION: Now switch to Future sub tab and repeat the steps 3-9
        EXPECTED: Result should be same as expected.
        """
        pass
