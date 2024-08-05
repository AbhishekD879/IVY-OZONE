import pytest
from tests.base_test import vtest
from tests.Common import Common


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
class Test_C60094818_Verify_that_Non_Runners_is_displayed_below_the_horse_names(Common):
    """
    TR_ID: C60094818
    NAME: Verify that "Non-Runners" is displayed below the horse names.
    DESCRIPTION: Verify that "Non-Runners" is displayed below the horse names.
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
        self.__class__.cms_horse_tab_name = self.get_sport_title(category_id=self.ob_config.horseracing_config.category_id)

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        cms_horse_tab_name = self.cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else self.cms_horse_tab_name.upper()
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
        all_items.get(cms_horse_tab_name).click()
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_the_event_which_has_atleast_one_non_runner(self):
        """
        DESCRIPTION: Click on the event which has atleast one Non-Runner
        EXPECTED: User should be navigated to the Event details page
        """
        self.navigate_to_edp(self.event.event_id, sport_name='horse-racing')

    def test_004_scroll_down_to_the_non_runner_selections_from_any_marketindexphpattachmentsget111391783(self):
        """
        DESCRIPTION: Scroll down to the Non-Runner selections from any market
        DESCRIPTION: ![](index.php?/attachments/get/111391783)
        EXPECTED: User should be able to see "Non-Runner" below the Horse name
        """
        non_runner = self.site.racing_event_details.items_as_ordered_dict.get(self.non_runner)
        self.assertTrue(non_runner.is_non_runner, msg=f'"Non-Runner" is not displayed under horse name "{self.non_runner}"')
