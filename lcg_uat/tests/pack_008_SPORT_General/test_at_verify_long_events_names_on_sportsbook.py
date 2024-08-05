import pytest
from random import randint
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.event_details
@pytest.mark.safari
@vtest
class Test_at_verify_long_events_names_on_sportsbook(BaseSportTest):
    """
    TR_ID: C9698235
    NAME: Verify that events with long names are displayed correctly on Sportsbook
    """
    keep_browser_open = True
    event = None
    long_name = 'Test team %d with a long name, really very long one'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 'Football' event with long name
        """
        self.__class__.team1 = self.long_name % randint(1000, 5000)
        self.__class__.team2 = self.long_name % randint(5000, 10000)

        event_params = self.ob_config.add_autotest_premier_league_football_event(team1=self.team1, team2=self.team2)

        self.__class__.eventID = event_params.event_id

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_tap_football(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_verify_sportsbook(self):
        """
        DESCRIPTION: Verify that just added event with a long name is displayed on Sportsbook correctly
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        event_should_be_truncated = True if self.brand != 'ladbrokes' else False
        self.assertEqual(event_should_be_truncated, self.event.is_event_name_truncated(),
                         msg=f'Event name truncated state is not "{event_should_be_truncated}"')

    def test_003_verify_event_details(self):
        """
        DESCRIPTION: Click event and verify long name is displayed on details page correctly
        """
        self.event.click()
        ui_event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(ui_event_name, self.event_name,
                         msg='Event name "%s" is not the same as expected "%s"'
                         % (ui_event_name, self.event_name))
