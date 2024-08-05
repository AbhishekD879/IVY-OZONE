from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import get_inplay_structure
import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.in_play
@pytest.mark.cms
@pytest.mark.adhoc_suite
@pytest.mark.reg160_fix
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@vtest
class Test_C65940562_MRT__Verify_the_In_play_tab_upcoming_section_display_as_per_category_wise_and_check_expand_collapse(BaseBetSlipTest,BaseSportTest):
    """
    TR_ID: C65940562
    NAME: MRT - Verify the In-play tab- upcoming section display as per category wise and check expand/collapse
    DESCRIPTION: This test case is to verify the upcoming section display as per category wise
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
    PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
    PRECONDITIONS: 3) Click on "+ Create Module ribbon tab" button to create new MRT.
    PRECONDITIONS: 4) Enter All mandatory Fields and click on save button:
    PRECONDITIONS: -Module ribbon tab title as "In-Play"
    PRECONDITIONS: - Select Directive name of In-Play option from dropdown
    PRECONDITIONS: -id as "tab-in-play"
    PRECONDITIONS: -URL  as "/home/in-play"
    PRECONDITIONS: -Click on "Create" CTA button
    PRECONDITIONS: 5)Check and select below required fields in module ribbon tab configuration:
    PRECONDITIONS: -Active
    PRECONDITIONS: -IOS
    PRECONDITIONS: -Android
    PRECONDITIONS: -Windows Phone
    PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
    PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
    PRECONDITIONS: -Click on "Save changes" button
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_selection_ids_from_event(self):
        event_ids = self.get_upcoming_events()
        selections = []
        for i in range(4):
            outcomes = self.ss_req.ss_event_to_outcome_for_event(event_id=event_ids[i])
            selections.append(outcomes[0].get('event').get('children')[0].get('market').get('children')[0].get('outcome').get('id'))
        return selections

    def get_ui_event(self):
        upcomimg_sports = self.site.home.tab_content.upcoming.items_as_ordered_dict
        self.assertTrue(upcomimg_sports, msg='Can not find any sport items in upcoming events')
        sport_item = list(upcomimg_sports.values())[0]
        league_items = list(sport_item.items_as_ordered_dict.values())
        self.assertTrue(league_items, msg = f'no league found in sport')
        events = league_items[0].items_as_ordered_dict
        self.assertTrue(events, msg=f'No event found in sport')
        event = list(events.values())[0]
        return event

    def get_upcoming_events(self):
        logs = get_inplay_structure()
        upcoming_events = logs.get('upcoming').get('eventsBySports')[0].get('eventsIds')
        return upcoming_events

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
        """
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        in_play_tab = next((module_ribbon_tab for module_ribbon_tab in module_ribbon_tabs if module_ribbon_tab.get('internalId')=='tab-in-play'),None)
        if not in_play_tab:
            in_play_tab = self.cms_config.module_ribbon_tabs.create_tab(directive_name = 'InPlay',
                                                          title='In-Play',
                                                          internal_id = 'tab-in-play',
                                                          url = '/home/in-play',
                                                          visible = True,
                                                          devices_android = True,
                                                          devices_ios = True,
                                                          devices_wp = True,
                                                          show_tabs_on = 'both')
        self.__class__.tab_name = in_play_tab.get('title').upper()

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.site.login()
        self.site.wait_content_state(state_name='HomePage')
        self.navigate_to_page(name='settings')
        self.site.wait_content_state('Settings')
        is_quick_bet_enable = self.site.settings.allow_quick_bet.is_enabled()
        if not is_quick_bet_enable:
            self.site.settings.allow_quick_bet.click()
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_verify_in_play_tab_present_in_mrt(self):
        """
        DESCRIPTION: verify In-Play tab present in MRT
        EXPECTED: In-Play tab should be present in MRT
        """
        is_module_ribbon_tabs_displayed = self.site.home.module_selection_ribbon.tab_menu.is_displayed()
        self.assertTrue(is_module_ribbon_tabs_displayed, msg='module ribbon tabs are not displayed')
        module_ribbon_tab = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(self.tab_name)
        self.assertTrue(module_ribbon_tab, msg=f'{self.tab_name} is not present in MRT')

    def test_003_click_on_in_play_tab(self):
        """
        DESCRIPTION: Click on In-play tab
        EXPECTED: user should be able to see In-play tab
        """
        self.site.home.module_selection_ribbon.tab_menu.click_item(self.tab_name)
        self.site.wait_content_state_changed()

    def test_004_scroll_down_and_verify_upcoming_events_display_with_event_count(self):
        """
        DESCRIPTION: Scroll down and Verify Upcoming events display with event count
        EXPECTED: Upcoming events section should be displayed with count
        """
        upcoming_section  = self.site.home.tab_content.upcoming
        self.assertTrue(upcoming_section, msg='upcoming section is not available in homepage')
        self.__class__.upcoming_events = self.site.home.tab_content.upcoming.items_as_ordered_dict
        self.assertTrue(self.upcoming_events, msg='upcoming events are not available in upcoming section')
        list(self.upcoming_events.values())[0].scroll_to_we()
        logs = get_inplay_structure()
        expected_upcoming_event_count = logs.get('upcoming').get('eventCount')
        upcoming_header_label = upcoming_section.upcoming_header.text_label
        upcoming_count_label = upcoming_section.upcoming_header.events_count_label_text
        actual_upcoming_label_name =  upcoming_section.upcoming_header.header_name
        expected_upcoming_label_name = f'{upcoming_header_label} {upcoming_count_label}'
        self.assertAlmostEqual(int(upcoming_count_label.strip('()')), expected_upcoming_event_count , delta=5 ,msg=f'actual upcoming event count {int(upcoming_count_label.strip("()"))} is not equal to '
                                                                                                    f'expected upcoming event count {expected_upcoming_event_count}' )
        self.assertEqual(actual_upcoming_label_name, expected_upcoming_label_name, msg=f'actual label {actual_upcoming_label_name} is not equal to expected label'
                                                                                         f'{expected_upcoming_label_name}')

    def test_005_verify_upcoming_events_unsubscribed_by_default(self):
        """
        DESCRIPTION: Verify Upcoming events unsubscribed by default
        EXPECTED: Upcoming events should be listed in collapsed state and category wise (sport wise)
        """
        for event_name,event in self.upcoming_events.items():
            event.scroll_to()
            self.assertFalse(event.is_expanded(), msg=f'{event_name} is expanded which is not expected')

    def test_006_verify_whether_upcoming_events_are_able_to_subscribe(self):
        """
        DESCRIPTION: Verify whether Upcoming events are able to subscribe
        EXPECTED: Upcoming events should be able to subscribe (Expand) for all categories
        """
        for event_name,event in self.upcoming_events.items():
            if not event.is_expanded():
                event.expand()
                self.assertTrue(event.is_expanded(), msg=f'{event_name} is not expanded after expand the event ')

    def test_007_verify_bet_placement_for_single_bet_from_quick_bet(self):
        """
        DESCRIPTION: Verify bet placement for single bet from Quick bet
        EXPECTED: Bet placement should be happened successfully for single be
        """
        # Single bet placement from quick bet
        event = self.get_ui_event()
        list(event.template.items_as_ordered_dict.values())[0].click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        quick_bet.place_bet.click()
        is_bet_receipt_displayed = quick_bet.bet_receipt.is_displayed()
        self.assertTrue(is_bet_receipt_displayed, msg='bet receipt is not diplayed')
        quick_bet.header.close_button.click()

    def test_008_verify_multiple_and_complex_bet_placement_from_betslip(self):
        """
        DESCRIPTION: Verify multiple and complex bet placement from betslip
        EXPECTED: Bet placement should be happened succefully for multiple and complex bets from Betslip
        """
        # Multiple bet placement from betslip
        multiple_selections = self.get_selection_ids_from_event()
        self.open_betslip_with_selections(selection_ids=multiple_selections)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        self.assertFalse(self.site.is_bet_receipt_displayed(), msg='Bet reciept is diplayed')
        # Complex bet placement from betslip
        self.test_003_click_on_in_play_tab()
        complex_selections = self.get_selection_ids_from_event()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=complex_selections)
        self.place_multiple_bet(number_of_stakes=4)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        self.assertFalse(self.site.is_bet_receipt_displayed(), msg='Bet reciept is diplayed')