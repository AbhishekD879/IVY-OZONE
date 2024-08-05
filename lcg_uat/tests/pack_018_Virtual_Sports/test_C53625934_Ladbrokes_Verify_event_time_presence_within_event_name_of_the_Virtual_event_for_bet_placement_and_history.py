import pytest
import voltron.environments.constants as vec
import re
import tests
from time import sleep
from tests.base_test import vtest
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@pytest.mark.reg157_fix
@vtest
class Test_C53625934_Ladbrokes_Verify_event_time_presence_within_event_name_of_the_Virtual_event_for_bet_placement_and_history(BaseBetSlipTest, BaseVirtualsTest):
    """
    TR_ID: C53625934
    NAME: [Ladbrokes] Verify event time presence within event name of the Virtual event for bet placement and history
    DESCRIPTION: Test case verifies event start time presence within event name of Greyhound and Horse Racing virtual events on all bet placement related places(pages), such as QuickBet, Betslip, Bet Receipt and Bet History/Open Bets.
    PRECONDITIONS: Upcoming virtual Greyhounds and Horse Racing events should be configured
    PRECONDITIONS: User should be logged in and have positive balance without any restrictions on betting
    PRECONDITIONS: 'Virtual' page (/virtual-sports) should be opened
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True
    actual_sports_list = []
    virtual_sports_categories = ['HR PT2', 'Victoria Park', 'Horse Racing', 'GR PT2', 'Greyhounds']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sports
        DESCRIPTION: Login into the app
        EXPECTED: User successfully log into the app
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        if not (('285' in virtuals_cms_class_ids) or ('286' in virtuals_cms_class_ids) or (
                '290' in virtuals_cms_class_ids)):
            raise SiteServeException('Required Sports are not configured')
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        for sport in sports_list:
            self.actual_sports_list.append(sport['class']['id'])
        if not (('285' in self.actual_sports_list) or ('286' in self.actual_sports_list) or (
                '290' in self.actual_sports_list)):
            raise SiteServeException('Required Sports are configured but did not find in siteserve response')
        self.site.login()
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        # Added new Virtual hub home page in FE,click on any one of top sport and navigate to main virtual sport page
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != 'NEXT EVENTS'), None)
            list(virtual_section.items_as_ordered_dict.values())[0].click()
        sport_category_names_from_page = self.site.virtual_sports.sport_carousel
        self.assertTrue(sport_category_names_from_page, msg='Virtual sports are not present on UI')
        for item in self.virtual_sports_categories[:3]:
            if item in sport_category_names_from_page.items_names:
                sport = item
                break
        else:
            raise SiteServeException(
                f'None of required sports: "{self.virtual_sports_categories[:3]}" is present on UI: "{sport_category_names_from_page}"')
        sport_category_names_from_page.click_item(sport)
        self.site.wait_content_state_changed(timeout=5)

    def test_001_switch_to_a_tab_of_the_upcoming_horse_racing_events_with_activenot_suspended_selections(self):
        """
        DESCRIPTION: Switch to a tab of the upcoming Horse Racing events with active(not suspended) selections
        EXPECTED: Event Name(Title) is shown above the video player
        EXPECTED: ![](index.php?/attachments/get/88860162)
        EXPECTED: Tab is selected with a red underlining shown below the event start time
        EXPECTED: ![](index.php?/attachments/get/88860163)
        EXPECTED: Event start time is shown in the following format: HH:MM
        """
        tab_content = self.site.virtual_sports.tab_content
        event_time = tab_content.sport_event_time
        self.assertTrue(event_time.is_displayed(), msg=f'Event time: "{event_time.name} is displayed')
        self.assertTrue(tab_content.sport_event_name, msg=f'Event name: "{tab_content.sport_event_name} is displayed')
        event_time_hh_mm = event_time.name
        event_time, event = list(tab_content.event_off_times_list.items_as_ordered_dict.items())[-2]  # meeting times
        event.click()
        sleep(2)
        self.__class__.selected_event_time = tab_content.event_off_times_list.selected_item
        self.assertEqual(event_time, self.selected_event_time,
                         msg=f'Actual event time: "{self.selected_event_time}" is not same as Expected event time: "{event_time}"')
        status = re.search("^\d{2}:\d{2}$", event_time_hh_mm)
        self.assertTrue(status, msg='Event time is not in "HH:MM" format')

    def test_002_add_1_selection_from_the_opened_tab_into_the_quick_bet(self):
        """
        DESCRIPTION: Add 1 selection from the opened tab into the Quick Bet
        EXPECTED: Quick Bet modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name
        EXPECTED: ![](index.php?/attachments/get/88860165)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860166)
        """
        sections = self.site.virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        runner_buttons = list(sections.values())[0]
        runner_buttons.bet_button.click()

        self.site.wait_for_quick_bet_panel()
        self.__class__.event1_name = self.site.quick_bet_panel.selection.content.event_name
        status = re.search("^\d{2}:\d{2}$", self.event1_name.split(' ')[0])
        self.assertTrue(status, msg='Event time is not in "HH:MM" format')
        self.assertEqual(self.selected_event_time, self.event1_name.split(' ')[0],
                         msg=f'selected event time: "{self.selected_event_time}" is not same as event time on quick bet: "{self.event1_name.split(" ")[0]}"')

    def test_003_place_a_bet_on_the_added_selection(self):
        """
        DESCRIPTION: Place a bet on the added selection
        EXPECTED: Bet Receipt modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name next to the market name (on its right side)
        EXPECTED: ![](index.php?/attachments/get/88860168)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860167)
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = 1
        self.site.wait_splash_to_hide(timeout=5)
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        event_name = self.site.quick_bet_panel.bet_receipt.event_name
        status = re.search("^\d{2}:\d{2}$", event_name.split(' ')[0])
        self.assertTrue(status, msg='Event time is not in "HH:MM" format')
        self.assertEqual(self.selected_event_time, event_name.split(' ')[0],
                         msg=f'selected event time: "{self.selected_event_time}" is not same as event time on quick bet: "{event_name.split(" ")[0]}"')
        self.site.quick_bet_panel.header.close_button.click()

    def test_004_close_the_bet_receipt_and_switch_to_a_tab_of_the_upcoming_greyhounds_events_with_activenot_suspended_selections(self):
        """
        DESCRIPTION: Close the Bet Receipt and switch to a tab of the upcoming Greyhounds events with active(not suspended) selections
        EXPECTED: Event Name(Title) is shown above the video player
        EXPECTED: ![](index.php?/attachments/get/88860169)
        EXPECTED: Tab is selected with a red underlining shown below the event start time
        EXPECTED: ![](index.php?/attachments/get/88860170)
        EXPECTED: Event start time is shown in the following format: HH:MM
        """
        sport_category_names_from_page = self.site.virtual_sports.sport_carousel
        self.assertTrue(sport_category_names_from_page, msg='Virtual sports are not present on UI')
        for item in self.virtual_sports_categories[3:]:
            if item in sport_category_names_from_page.items_names:
                sport = item
                break
        else:
            raise SiteServeException(
                f'None of required sports: "{self.virtual_sports_categories[3:]}" is present on UI: "{sport_category_names_from_page}"')
        sport_category_names_from_page.click_item(sport)
        self.site.wait_content_state_changed(timeout=5)

        tab_content = self.site.virtual_sports.tab_content
        event_time = tab_content.sport_event_time
        self.assertTrue(event_time.is_displayed(), msg=f'Event time: "{event_time.name} is displayed')
        self.assertTrue(tab_content.sport_event_name, msg=f'Event name: "{tab_content.sport_event_name} is displayed')
        event_time_hh_mm = event_time.name

        event_time, event = list(tab_content.event_off_times_list.items_as_ordered_dict.items())[-2]
        event.click()
        sleep(2)
        self.__class__.selected_event_time = tab_content.event_off_times_list.selected_item
        self.assertEqual(event_time, self.selected_event_time,
                         msg=f'Actual event time: "{self.selected_event_time}" is not same as Expected event time: "{event_time}"')
        status = re.search("^\d{2}:\d{2}$", event_time_hh_mm)
        self.assertTrue(status, msg='Event time is not in "HH:MM" format')

    def test_005_add_1_selection_from_the_opened_tab_into_the_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add 1 selection from the opened tab into the the Betslip and Open Betslip
        EXPECTED: Betslip modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name
        EXPECTED: ![](index.php?/attachments/get/88860171)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860173)
        """
        sections = self.site.virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        runner_buttons = list(sections.values())[0]
        runner_buttons.bet_button.click()

        self.site.wait_for_quick_bet_panel()
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.site.open_betslip()

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.has_event_name(), msg=f'Event name is not displayed for "{stake_name}"')
        self.__class__.event2_name = stake.event_name
        status = re.search("^\d{2}:\d{2}$", self.event2_name.split(' ')[0])
        self.assertTrue(status, msg='Event time is not in "HH:MM" format')
        self.assertEqual(self.selected_event_time, self.event2_name.split(' ')[0],
                         msg=f'selected event time: "{self.selected_event_time}" is not same as event time on quick bet: "{self.event2_name.split(" ")[0]}"')

    def test_006_place_a_bet_on_the_added_selection(self):
        """
        DESCRIPTION: Place a bet on the added selection
        EXPECTED: Bet Receipt modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name next to the market name (on its right side)
        EXPECTED: ![](index.php?/attachments/get/88860172)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860174)
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        section = list(betreceipt_sections.values())[0]
        event_name = section.event_description
        status = re.search("^\d{2}:\d{2}$", event_name.split(' ')[0])
        self.assertTrue(status, msg='Event time is not in "HH:MM" format')
        self.assertEqual(self.selected_event_time, event_name.split(' ')[0],
                         msg=f'selected event time: "{self.selected_event_time}" is not same as event time on quick bet: "{event_name.split(" ")[0]}"')

    def test_007_close_the_bet_receipt_and_navigate_to_open_bets_page_open_bets(self):
        """
        DESCRIPTION: Close the Bet Receipt and navigate to Open Bets page (/open-bets)
        EXPECTED: Open Bets page is opened
        EXPECTED: Bets from both Quick Bet and Betslip bet placements are shown one under another
        EXPECTED: ![](index.php?/attachments/get/88860178)
        """
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.site.wait_content_state_changed(timeout=10)
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if (len(bets)) == 0:
            current_tab_name = self.site.open_bets.tab_content.grouping_buttons.current
            self._logger.info(
                f'There are no bets displayed on "{current_tab_name}" of "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
        else:
            bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(bets, msg='No bets available under openbets')
            for bet in list(bets.values()):
                if self.event1_name.replace(self.event1_name.split(' ')[0], '') in bet.event_name:
                    status = re.search("^\d{2}:\d{2}$", bet.event_name.split(' ')[0])
                    self.assertTrue(status, msg='Event time is not in "HH:MM" format')
                elif self.event2_name.replace(self.event2_name.split(' ')[0], '') in bet.event_name:
                    status = re.search("^\d{2}:\d{2}$", bet.event_name.split(' ')[0])
                    self.assertTrue(status, msg='Event time is not in "HH:MM" format')

    def test_008_verify_start_time_presence_within_event_names_of_placed_bets(self):
        """
        DESCRIPTION: Verify start time presence within event names of placed Bets
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name
        EXPECTED: (!) **Start time in the event name may differ from the 'factual start time', shown next to the event name (on its right side) in 'HH:MM, Today' format** - this is due to a fact that factual start time doesn't account time zone differences
        """
        # covered in the step test_007

    def test_009_wait_for_both_eventsfrom_steps_2_and_5_to_settle_and_switch_to_settled_bets_page_bet_history(self):
        """
        DESCRIPTION: Wait for both events(from steps 2 and 5) to settle and switch to Settled Bets page (/bet-history)
        EXPECTED: Settled Bets page is opened
        EXPECTED: Bets from step 8 are shown one under another
        EXPECTED: ![](index.php?/attachments/get/88860179)
        """
        # can not be automated

    def test_010_verify_start_time_presence_within_event_names_of_settled_bets(self):
        """
        DESCRIPTION: Verify start time presence within event names of settled Bets
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name for each cell that represents the previously placed(settled) bet.
        """
        # can not be automated
