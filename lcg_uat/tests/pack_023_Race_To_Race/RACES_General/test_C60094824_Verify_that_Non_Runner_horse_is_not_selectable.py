import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can't create events in prob ob
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.horseracing
@vtest
class Test_C60094824_Verify_that_Non_Runner_horse_is_not_selectable(Common):
    """
    TR_ID: C60094824
    NAME: Verify that Non-Runner horse is not selectable
    DESCRIPTION: Verify that Non-Runner horse is not selectable.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Event should have atleast one Non-Runner
    PRECONDITIONS: (In Open Bet make one selection as Non- Runner)
    """
    keep_browser_open = True
    non_runner = 'runner 1'
    selection_names = ['|runner 1||N/R|', '|runner 2|', '|runner 3|']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get or create events with at least one non runner
        """
        self.__class__.event = self.ob_config.add_UK_racing_event(runner_names=self.selection_names)

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        # covered in step_002

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_the_event_which_has_atleast_one_non_runner(self):
        """
        DESCRIPTION: Click on the event which has atleast one Non-Runner
        EXPECTED: User should be navigated to the Event details page
        """
        self.navigate_to_edp(self.event.event_id, sport_name='horse-racing')

    def test_004_try_to_add_non_runner_selection_to_betslip(self):
        """
        DESCRIPTION: Try to add Non-runner selection to betslip
        EXPECTED: User should not be able to select Non-Runner horse
        """
        non_runner = self.site.racing_event_details.items_as_ordered_dict.get(self.non_runner)
        self.assertFalse(non_runner.bet_button.is_enabled(), msg='Bet Button is not disabled')
        try:
            non_runner.bet_button.click()
        except VoltronException:
            self._logger.info('*** Cannot select non runner as expected')
        if self.device_type == 'mobile':
            self.site.open_betslip()
        message = self.site.betslip.no_selections_title
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual message "{message}" is not same as '
                             f'expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
