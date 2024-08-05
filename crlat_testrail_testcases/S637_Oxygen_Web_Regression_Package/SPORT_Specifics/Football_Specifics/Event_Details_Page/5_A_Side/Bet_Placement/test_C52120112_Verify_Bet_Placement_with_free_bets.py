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
class Test_C52120112_Verify_Bet_Placement_with_free_bets(Common):
    """
    TR_ID: C52120112
    NAME: Verify Bet Placement with free bets
    DESCRIPTION: This test case verifies Bet Placement with free bets
    PRECONDITIONS: User should have 'free bets' and 'odds boost'
    PRECONDITIONS: How to add Odds boost token: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: How to Manually Add Freebet Token to Account: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
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
    PRECONDITIONS: - 'Build a team' button (pitch view)
    """
    keep_browser_open = True

    def test_001_select_valid_combinations(self):
        """
        DESCRIPTION: Select valid combinations
        EXPECTED: - Odds are available on the left of the Place Bet' button
        EXPECTED: - Button becomes active
        EXPECTED: - All other positions ('+') are in active state
        EXPECTED: ![](index.php?/attachments/get/59602293)
        """
        pass

    def test_002_clicktap_on_place_bet_button(self):
        """
        DESCRIPTION: Click/tap on 'Place Bet' button
        EXPECTED: - Bet builder is initiated
        """
        pass

    def test_003_clicktap_on_free_bet_link(self):
        """
        DESCRIPTION: Click/tap on 'free bet' link
        EXPECTED: - Appears pop-up with a list of available free bets.
        EXPECTED: ![](index.php?/attachments/get/74701516)
        """
        pass

    def test_004_select_one_of_the_available_free_bet(self):
        """
        DESCRIPTION: Select one of the available free bet.
        EXPECTED: - Free bet selected correctly.
        """
        pass

    def test_005_place_a_5a_side_bet_with_a_free_bet(self):
        """
        DESCRIPTION: PLace a 5A side bet with a free bet.
        EXPECTED: - Bet placed successfully.
        """
        pass

    def test_006_verify_channel_used_for_5_a_side_bets(self):
        """
        DESCRIPTION: Verify channel used for 5-A-Side bets
        EXPECTED: Channel: "f" is present in '50011' request in 'remotebetslip' websocket
        """
        pass
