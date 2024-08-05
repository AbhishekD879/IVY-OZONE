import pytest

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@pytest.mark.surface_bets
@pytest.mark.event_details
@vtest
class Test_C9770792_Verify_Surface_Bet_module_displaying_on_Event_Details_Page_with_no_Surface_bets_assigned(BaseFeaturedTest):
    """
    TR_ID: C9770792
    VOL_ID: C12529761
    NAME: Verify Surface Bet module displaying on Event Details Page with no Surface bets assigned
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
        """
        simple_event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = simple_event.event_id

    def test_001_in_the_application_open_the_edp_without_added_surface_betsverify_this_edp_doesnt_contain_surface_bet_module(self):
        """
        DESCRIPTION: In the application open the EDP without added Surface Bets
        DESCRIPTION: Verify this EDP doesn't contain Surface Bet module
        EXPECTED: Surface Bet module isn't shown on the other EDP
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.assertFalse(self.site.sport_event_details.tab_content.has_surface_bets(expected_result=False),
                         msg='Surface Bet module is shown on the EDP')
