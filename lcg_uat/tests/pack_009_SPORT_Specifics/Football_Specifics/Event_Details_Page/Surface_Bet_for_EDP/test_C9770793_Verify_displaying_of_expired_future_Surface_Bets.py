import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@pytest.mark.sports
@pytest.mark.event_details
@pytest.mark.surface_bets
@vtest
class Test_C9770793_Verify_displaying_of_expired_future_Surface_Bets(Common):
    """
    TR_ID: C9770793
    VOL_ID: C12600639
    NAME: Verify displaying of expired/future Surface Bets
    DESCRIPTION: Test case verifies that expired/future Surface Bet is shown on the EDP
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
        DESCRIPTION: 2. Open this EDP
        """
        event = self.ob_config.add_football_event_to_uefa_champions_league()
        surface_bet_event = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.eventID = event.event_id
        selection_ids, team1 = surface_bet_event.selection_ids, surface_bet_event.team1
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_ids[team1],
                                                      eventIDs=self.eventID, edpOn=True)
        self.__class__.surface_bet_id = surface_bet.get('id')
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.navigate_to_edp(self.eventID, timeout=15)
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id {self.eventID}')

    def test_001_in_the_cms_edit_the_surface_bet_set_display_from_to_to_the_past(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the past.
        """
        past_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=-3)[:-3] + 'Z'
        past_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=-2)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=past_date_from,
                                           displayTo=past_date_to)

    def test_002_in_the_application_refresh_the_edp_verify_this_surface_bet_is_displayed(self):
        """
        DESCRIPTION: In the application refresh the EDP verify this Surface bet is displayed
        EXPECTED: Surface Bet is shown
        EXPECTED: _NOTE: Surface Bet is shown on the EDP regardless Display From/To settings!_
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id {self.eventID}')

        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" is not found in "{list(surface_bets.keys())}"')

    def test_003_in_the_cms_edit_the_surface_bet_set_display_from_to_to_the_future(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the future.
        """
        future_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=2)[:-3] + 'Z'
        future_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=3)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=future_date_from,
                                           displayTo=future_date_to)

    def test_004_in_the_application_refresh_the_edp_verify_this_surface_bet_is_displayed(self):
        """
        DESCRIPTION: In the application refresh the EDP verify this Surface bet is displayed
        EXPECTED: Surface Bet is shown
        EXPECTED: _NOTE: Surface Bet is shown on the EDP regardless Display From/To settings!_
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id {self.eventID}')

        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" is not found in "{list(surface_bets.keys())}"')
