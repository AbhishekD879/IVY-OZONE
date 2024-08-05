import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C16408289_Verify_My_Bets_counter_animation_when_increasing_decreasing_counter(Common):
    """
    TR_ID: C16408289
    NAME: Verify My Bets counter animation when increasing /decreasing counter
    DESCRIPTION: This test case verifies displaying My Bets counter animation when increasing/decreasing counter
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Make sure user has open (unsettled) bets
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_verify_displaying_my_bets_badge_animation_when_number_of_my_bets_has_changed_after__settled_bets_after_navigation_to_my_bets_pagetab_or_refresh_the_page__cash_out__bet_placement(self):
        """
        DESCRIPTION: Verify displaying My Bets badge animation when number of My bets has changed after:
        DESCRIPTION: - Settled Bets (After navigation to My Bets page/tab or refresh the page)
        DESCRIPTION: - Cash-out
        DESCRIPTION: - Bet placement
        EXPECTED: - My Bets animation  is displaying after number of bets has changed
        EXPECTED: - My bets badge icon showing the correct number of open bets.
        EXPECTED: - My bets badge icon is not shown when there are no open bets ( '0' counter is NOT displayed)
        """
        pass
