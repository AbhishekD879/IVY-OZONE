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
class Test_C9770808_Verify_Surface_Bet_module_displaying_on_a_few_Event_Details_Pages(BaseFeaturedTest):
    """
    TR_ID: C9770808
    VOL_ID: C12587643
    NAME: Verify Surface Bet module displaying on a few Event Details Pages
    DESCRIPTION: Test case verifies possibility to add a Surface Bet to a few Event Details Pages
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. There is a single Surface Bet added to a few Event Details pages (EDP).
        PRECONDITIONS: 2. Valid Selection Id is set
        PRECONDITIONS: 3. Open those EDPs in Oxygen application.
        PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventIDs = [event.event_id, event_2.event_id]
        surface_bet = self.cms_config.add_surface_bet(selection_id=event.selection_ids[event.team1],
                                                      eventIDs=self.eventIDs, edpOn=True)
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

    def test_001_verify_the_surface_bet_is_shown_on_the_all_edps_its_added_to(self):
        """
        DESCRIPTION: Verify the Surface Bet is shown on the all EDPs it's added to
        EXPECTED: Surface bet is shown on the all EDPs
        """
        for eventID in self.eventIDs:
            self.navigate_to_edp(event_id=eventID, sport_name='football')
            self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                            msg=f'Surface Bet module is not shown on the EDP with event_id {eventID}')

            surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
            surface_bet = surface_bets.get(self.surface_bet_title)
            self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" is not found in "{list(surface_bets.keys())}"')
