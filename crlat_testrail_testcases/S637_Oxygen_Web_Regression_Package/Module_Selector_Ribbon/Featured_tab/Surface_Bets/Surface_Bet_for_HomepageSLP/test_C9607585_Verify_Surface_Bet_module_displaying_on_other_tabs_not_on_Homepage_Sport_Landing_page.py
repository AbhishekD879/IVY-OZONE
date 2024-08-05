import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C9607585_Verify_Surface_Bet_module_displaying_on_other_tabs_not_on_Homepage_Sport_Landing_page(Common):
    """
    TR_ID: C9607585
    NAME: Verify Surface Bet module displaying on other tabs (not on Homepage/Sport Landing page)
    DESCRIPTION: Test case verifies that Surface Bets aren't shown on other tabs
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the SLP/Homepage in the CMS
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_application_open_the_homepage_featured_tabverify_the_neighboring_tabs_eg__in_play_streaming_dont_contain_surface_bet_module(self):
        """
        DESCRIPTION: In the application open the Homepage (Featured tab).
        DESCRIPTION: Verify the neighboring tabs, e.g.  In-Play, Streaming, don't contain Surface Bet module
        EXPECTED: Surface Bet module isn't shown on the other tabs
        """
        pass

    def test_002_open_the_sport_category_landing_page_verify_the_neighboring_tabs_dont_contain_surface_bet_module(self):
        """
        DESCRIPTION: Open the Sport category landing page. Verify the neighboring tabs don't contain Surface Bet module
        EXPECTED: Surface Bet module isn't shown on the other tabs
        """
        pass
