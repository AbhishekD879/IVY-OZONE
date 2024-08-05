import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.watch_free
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C1274043_Verify_WATCH_FREE_for_Groups_of_Races(BaseRacing):
    """
    TR_ID: C1274043
    NAME: Verify WATCH FREE for Groups of Races
    DESCRIPTION: This test case verifies availability of visualization (LiveSim) for Race on Event Details page under Media Area.
    PRECONDITIONS: *   Application is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    """
    keep_browser_open = True
    eventIDs = {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add racing event with start time more than 5 minutes to the following groups:
        DESCRIPTION: UK & IRE,
        DESCRIPTION: International
        DESCRIPTION: Virtual
        EXPECTED: Racing event added
        """
        self.__class__.eventIDs.update({'UK IRE': self.ob_config.add_UK_racing_event(number_of_runners=1)[0],
                                        'International':
                                            self.ob_config.add_international_racing_event(number_of_runners=1)[0],
                                        'Virtual': self.ob_config.add_virtual_racing_event(number_of_runners=1)[0]})
        self._logger.info(f'*** Created events with IDs {self.eventIDs}')

    def test_001_go_to_uk_ire_group(self):
        """
        DESCRIPTION: Go to '**UK & IRE**' group
        """
        self.navigate_to_edp(event_id=self.eventIDs['UK IRE'], sport_name='horse-racing')

    def test_002_open_event_details_pagemore_than_5_minutes_before_the_scheduled_race_off_time_or_open_live_event_details_page(self):
        """
        DESCRIPTION: Open event details page **more **than 5 minutes before the scheduled race-off time or open Live event details page
        EXPECTED: *     Event details page is opened
        EXPECTED: *    'WATCH FREE' button is present under media area
        """
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        has_watch_free_button = self.horse_racing_edp.has_watch_free_button()
        self.assertTrue(has_watch_free_button,
                        msg=f'Watch Free button was not found for event type "{self.eventIDs["UK IRE"]}"')

    def test_003_go_to_international_group(self):
        """
        DESCRIPTION: Go to '**International**' group
        """
        self.navigate_to_edp(event_id=self.eventIDs['International'], sport_name='horse-racing')

    def test_004_open_event_details_pagemore_than_5_minutes_before_the_scheduled_race_off_time_or_open_live_event_details_page(self):
        """
        DESCRIPTION: Open event details page **more **than 5 minutes before the scheduled race-off time or open Live event details page
        EXPECTED: *   Event details page is opened
        EXPECTED: *   'WATCH FREE' button is NOT present under media area
        """
        has_watch_free_button = self.horse_racing_edp.has_watch_free_button()
        self.assertFalse(has_watch_free_button,
                         msg=f'Watch Free button is found for event type "{self.eventIDs["International"]}"')

    def test_005_go_to_virtual_group(self):
        """
        DESCRIPTION: Go to '**Virtual**' group
        """
        self.navigate_to_edp(event_id=self.eventIDs['Virtual'], sport_name='horse-racing')

    def test_006_open_event_details_pagemore_than_5_minutes_before_the_scheduled_race_off_time_or_open_live_event_details_page(self):
        """
        DESCRIPTION: Open event details page **more **than 5 minutes before the scheduled race-off time or open Live event details page
        EXPECTED: *   Event details page is opened
        EXPECTED: *   'WATCH FREE' button is NOT present under media area
        """
        has_watch_free_button = self.horse_racing_edp.has_watch_free_button()
        self.assertFalse(has_watch_free_button,
                         msg=f'Watch Free button is found for event type "{self.eventIDs["Virtual"]}"')
