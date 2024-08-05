import pytest
import voltron.environments.constants as vec
from crlat_cms_client.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events cannot be created in prod
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094823_Verify_Price_display_for_Non_Runner(Common):
    """
    TR_ID: C60094823
    NAME: Verify Price display for Non-Runner
    DESCRIPTION: Verify that the latest available price of the horse before it was declared non-runner is displayed at price and greyed out.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Event should have atleast one Non-Runner
    PRECONDITIONS: (In Open Bet make one selection as Non- Runner)
    """
    keep_browser_open = True
    runner_names = ['|Horse1|', '|Horse2|', '|Horse3|', '|Horse4||N/R|']
    prices = {0: '1/2', 1: '1/3', 2: '2/9', 3: '2/7'}

    def get_outcomes(self):
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        return outcomes

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Create Horse racing event
        """
        horse_racing_event = self.ob_config.add_UK_racing_event(lp_prices=self.prices,
                                                                runner_names=self.runner_names)
        self.__class__.event_id = horse_racing_event.event_id
        self.__class__.selection_ids = list(horse_racing_event.selection_ids.values())
        self.__class__.cms_horse_tab_name = self.get_sport_title(category_id=21)

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
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_004_scroll_down_to_the_non_runner_selections_from_any_market(self):
        """
        DESCRIPTION: Scroll down to the Non-Runner selections from any market
        EXPECTED: 1: User should be displayed the latest available price of the horse before it was declared non-runner
        EXPECTED: 2; Price should be greyed out
        """
        non_runner_list = []
        before_outcomes = self.get_outcomes()
        for outcome in before_outcomes.values():
            non_runner_list.append(outcome.is_non_runner)
        self.assertIn(True, non_runner_list,
                      msg='Event has not even one non runner')
        before_horse1 = before_outcomes['Horse1']
        actual_price = before_horse1.output_price
        self.assertTrue(before_horse1.bet_button.is_enabled(), msg=' Price button is not enabled')
        self.assertEqual(self.prices[0], actual_price,
                         msg=f' Actual Price: "{actual_price}" is not same as '
                             f' Expected Price: "{self.prices[0]}" , "Latest price" is not available')
        self.assertFalse(before_horse1.is_non_runner, msg=f' "{before_horse1.name}" is a non runner')

        self.ob_config.change_selection_name(selection_id=self.selection_ids[0],
                                             new_selection_name=self.runner_names[0] + '|N/R|')
        iteration = 1
        after_horse1, susp_price = None, None
        while iteration <= 6:
            self.device.refresh_page()
            self.site.wait_content_state_changed()
            after_outcomes = self.get_outcomes()
            after_horse1 = after_outcomes['Horse1']
            susp_price = after_horse1.output_price
            result = wait_for_result(lambda: after_horse1.bet_button.is_enabled(), expected_result=False,
                                     timeout=10)
            if not result:
                break
            iteration += 1
        self.assertFalse(after_horse1.bet_button.is_enabled(), msg=' Price is not greyed out')
        self.assertEqual(vec.bet_history.SUSPENDED.upper(), susp_price,
                         msg=f' Actual Price: "{susp_price}" is not same as '
                             f' Expected Price: "{vec.bet_history.SUSPENDED.upper()}", "Latest price" is not changed')
        self.assertTrue(after_horse1.is_non_runner, msg=f' "{after_horse1.name}" is not non runner')
