import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod can't create OB event on prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094825_Verify_removal_of_previous_price_for_Non_Runner(BaseRacing):
    """
    TR_ID: C60094825
    NAME: Verify removal of previous price for Non-Runner
    DESCRIPTION: This test case is to verify not to display previous odds of Non-Runner
    PRECONDITIONS: Non-runner horse should have previous odds
    """
    keep_browser_open = True
    non_runner = 'runner 1'
    price = ['1/10', '1/7']
    price_2 = '1/3'
    price_3 = '1/5'
    selection_names = ['|runner 1|', '|runner 2|', '|runner 3|']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get or create events with at least one non runner
        """
        self.__class__.event = self.ob_config.add_UK_racing_event(runner_names=self.selection_names,
                                                                  lp_prices={0: self.price[0], 1: self.price_2, 2: self.price_3})
        self.__class__.eventID = self.event.event_id
        self.__class__.selection_ids = self.event.selection_ids

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('homepage')
        selection_name, selection_id = list(self.selection_ids.items())[0]
        new_selection_name = f'{selection_name} N/R'
        self.ob_config.change_selection_name(selection_id=selection_id, new_selection_name=new_selection_name)

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_003_click_on_the_event_which_has_non_runner_information_with_previous_odds(self):
        """
        DESCRIPTION: Click on the event which has Non-Runner information with previous odds
        EXPECTED: If non runner horse has previous odds it should not display
        EXPECTED: ![](index.php?/attachments/get/115417211)
        """
        self.navigate_to_edp(self.event.event_id, sport_name='horse-racing')
        non_runner = self.site.racing_event_details.items_as_ordered_dict.get(self.non_runner)
        selection_id = self.selection_ids[self.non_runner]
        self.ob_config.change_price(selection_id=selection_id, price=self.price[1])
        expected_previous_price = f'{self.price[0]} > {self.price[1]}'
        self.assertNotEqual(non_runner.previous_price, expected_previous_price, msg="previous odds displaying for non runner")
