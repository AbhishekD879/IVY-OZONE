import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C49345818_Verify_the_logic_of___buttons_on_Player_Card(Common):
    """
    TR_ID: C49345818
    NAME: Verify the logic of +/ - buttons on Player Card
    DESCRIPTION: This test case verifies the logic of +/ - buttons on Player Card
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP:
    PRECONDITIONS: - '5 A Side' sub tab (event type described above):
    PRECONDITIONS: - 'Build a team' button ->
    PRECONDITIONS: - click on '+' button near the player on the overlay ->
    PRECONDITIONS: - in the list of players select one specific.
    """
    keep_browser_open = True

    def test_001_verify_the_default_value_when_entering_player_card(self):
        """
        DESCRIPTION: Verify the default value when entering player card
        EXPECTED: - default value is displayed as median/average stat value
        EXPECTED: - values are received in response (Network tab: 'statistic-value-range?obEventId=773006&playerId=28&statId=5' request, minValue: /maxValue: /average:)
        EXPECTED: and correspond to values on UI
        EXPECTED: - '+/-' buttons are clickable (if more than 1 step available)
        EXPECTED: ![](index.php?/attachments/get/59204748)
        """
        pass

    def test_002_click_on_plus_button_on_player_card_overlay(self):
        """
        DESCRIPTION: Click on '+' button on player card overlay
        EXPECTED: - step value increases
        EXPECTED: - price odds button value is recalculated as well on 'Add Player' button ('price' request is sent with latest odds value)
        EXPECTED: - market value (e.g. T.Krul to Concede < 1 Goals) is updated
        EXPECTED: ![](index.php?/attachments/get/59681304)
        """
        pass

    def test_003_click_on_plus_button_several_times(self):
        """
        DESCRIPTION: Click on '+' button several times
        EXPECTED: All places stated above are updated
        """
        pass

    def test_004_reach_the_max_value_by_clicking_plus_button(self):
        """
        DESCRIPTION: Reach the max value (by clicking '+' button)
        EXPECTED: Button becomes greyed out and not clickable
        EXPECTED: (max value is received in 'statistic-value-range?obEventId=773006&playerId=28&statId=5' request, maxValue:)
        """
        pass

    def test_005_click_on___button(self):
        """
        DESCRIPTION: Click on '-' button
        EXPECTED: - step value decreases
        EXPECTED: - price odds button value is recalculated as well on 'Add Player' button ('price' request is sent with latest odds value)
        EXPECTED: - market value (e.g. T.Krul to Concede < 1 Goals) is updated
        """
        pass

    def test_006_reach_the_min_value_by_clicking___button(self):
        """
        DESCRIPTION: Reach the min value (by clicking '-' button)
        EXPECTED: Button becomes greyed out and not clickable
        EXPECTED: (min value is received in 'statistic-value-range?obEventId=773006&playerId=28&statId=5' request, minValue:)
        """
        pass

    def test_007_verify_edge_case_if_happensclick_on_plus__buttons(self):
        """
        DESCRIPTION: Verify edge case (if happens):
        DESCRIPTION: click on '+/-' buttons
        EXPECTED: - step value increases/decreases
        EXPECTED: - market value (e.g. T.Krul to Concede < 1 Goals) is updated
        EXPECTED: - price odds button value stays the same because in 'price' request we receive priceNum: 0, priceDen: 0
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: ![](index.php?/attachments/get/62318401)
        """
        pass
