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
class Test_C60079480_Football_displaying_market_in_market_selector_when_event_has_To_Win_Not_to_Nil_market(Common):
    """
    TR_ID: C60079480
    NAME: Football: displaying market in market selector when event has 'To Win Not to Nil' market
    DESCRIPTION: This test case verifies displaying of 'To win & Both Teams to Score' market in market selector and respective event card with selections on Matches, Competitions and Coupons
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have an active Football event with active market added from 'To win Not to Nil' market template and with added selections
    PRECONDITIONS: - You should have a Football Coupon created with the event above based on 'To Win Not to Nil' market
    PRECONDITIONS: - You should be on Football landing page > Matches tab
    """
    keep_browser_open = True

    def test_001_tap_market_selector_and_verify_to_win__both_teams_to_score_market_displaying(self):
        """
        DESCRIPTION: Tap market selector and verify 'To win & Both Teams to Score' market displaying
        EXPECTED: 'To win & Both Teams to Score' market is displayed
        """
        pass

    def test_002_select_to_win__both_teams_to_score_market_and_verify_card_displaying(self):
        """
        DESCRIPTION: Select 'To win & Both Teams to Score' market and verify card displaying
        EXPECTED: Event card with 'To Win Not to Nil' market is displayed with respective selections
        """
        pass

    def test_003___go_to_coupons_tab_and_open_the_coupon_with_event_with_to_win_not_to_nil_market__tap_market_selector_and_verify_to_win__both_teams_to_score_market_displaying(self):
        """
        DESCRIPTION: - Go to Coupons tab and open the Coupon with event with 'To Win Not to Nil' market
        DESCRIPTION: - Tap market selector and verify 'To win & Both Teams to Score' market displaying
        EXPECTED: 'To win & Both Teams to Score' market is displayed
        """
        pass

    def test_004_select_to_win__both_teams_to_score_market_and_verify_card_displaying(self):
        """
        DESCRIPTION: Select 'To win & Both Teams to Score' market and verify card displaying
        EXPECTED: Event card with 'To Win Not to Nil' market is displayed with respective selections
        """
        pass

    def test_005___go_to_football_landing_page__competitions_tab_and_open_a_competition_with_event_with_to_win_not_to_nil_market__tap_market_selector_and_verify_to_win__both_teams_to_score_market_displaying(self):
        """
        DESCRIPTION: - Go to Football landing page > Competitions tab and open a competition with event with 'To win Not to Nil' market
        DESCRIPTION: - Tap market selector and verify 'To win & Both Teams to Score' market displaying
        EXPECTED: 'To win & Both Teams to Score' market is displayed
        """
        pass

    def test_006_select_to_win__both_teams_to_score_market_and_verify_card_displaying(self):
        """
        DESCRIPTION: Select 'To win & Both Teams to Score' market and verify card displaying
        EXPECTED: Event card with 'To Win Not to Nil' market is displayed with respective selections
        """
        pass
