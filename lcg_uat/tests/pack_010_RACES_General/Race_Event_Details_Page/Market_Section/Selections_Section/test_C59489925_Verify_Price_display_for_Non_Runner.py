import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from crlat_cms_client.utils.waiters import wait_for_result
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot change an active selection to non-runner in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C59489925_Verify_Price_display_for_Non_Runner(Common):
    """
    TR_ID: C59489925
    NAME: Verify Price display for Non-Runner
    DESCRIPTION: Verify that the latest available price of the horse before it was declared non-runner is displayed at price and greyed out.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Event should have atleast one Non-Runner
    PRECONDITIONS: (In Open Bet make one selection as Non- Runner)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3', 2: '2/9', 3: '2/7'}

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Create Horse racing event
        """
        horse_racing_event = self.ob_config.add_UK_racing_event(number_of_runners=4, lp_prices=self.prices)
        self.__class__.event_id = horse_racing_event.event_id
        self.__class__.selection_ids = horse_racing_event.selection_ids

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
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_the_event_which_has_atleast_one_non_runner(self):
        """
        DESCRIPTION: Click on the event which has atleast one Non-Runner
        EXPECTED: User should be navigated to the Event details page
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_004_scroll_down_to_the_non_runner_selections_from_any_market(self):
        """
        DESCRIPTION: Scroll down to the Non-Runner selections from any market
        EXPECTED: 1: User should be displayed the latest available price of the horse before it was declared non-runner
        EXPECTED: 2; Price should be greyed out
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        outcome_name, outcome = list(outcomes.items())[0]
        self.assertTrue(outcome.output_price, msg=f'Price is not shown for "{outcome_name}" before its declared as non-runner')
        selection_id = self.selection_ids[outcome_name]
        new_selection_name = f'{outcome_name} N/R'
        self.ob_config.change_selection_name(selection_id=selection_id,
                                             new_selection_name=new_selection_name)
        iteration = 0
        result = True
        while iteration <= 6 and result:
            self.device.refresh_page()
            self.site.wait_content_state_changed()
            non_runner = self.site.racing_event_details.items_as_ordered_dict.get(outcome_name)
            result = wait_for_result(lambda: non_runner.bet_button.is_enabled(), expected_result=False,
                                     timeout=10)
            if not result:
                break
            else:
                iteration += 1
        self.assertEqual(non_runner.output_price, 'SUSP',
                         msg=f'Actual text "{non_runner.output_price}" is not same as Expected text "SUSP"')
