import re

import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from datetime import datetime
from tzlocal import get_localzone
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.byb_widget
@pytest.mark.OZONE_15384
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.insprint_auto
@pytest.mark.mobile_only
@vtest
class Test_C66133296_Verify_selections_in_displayed_as_per_the_order_value_ascending_order_which_is_set_in_OB_in_Bet_Builder_MRT(
    BaseBetSlipTest):
    """
    TR_ID: C66133296
    NAME: Verify selections in displayed as per the order value ascending order which is set in OB in Bet Builder MRT
    DESCRIPTION: This testcase is to verify selections in BYB widget to be displayed as per the order value which is set in OB in Bet Builder MRT
    PRECONDITIONS: 1) Create BYB market card in Bet Builder MRT for the event in OB 2) BYB Widget sub section should be created under BYB main section3) Navigate a BYB active card for the above created event in OB
    """
    keep_browser_open = True
    timezone = str(get_localzone())

    def date_from(self):
        # Time Zone validation
        if self.timezone.upper() == "UTC":
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, minutes=-1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, hours=-1, minutes=-1)[:-3] + 'Z'
        else:
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, hours=-5.5, minutes=-1)[:-3] + 'Z'
        return date_from

    def date_to(self):
        # Time Zone validation

        if self.timezone.upper() == "UTC":
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, minutes=2)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-1, minutes=2)[:-3] + 'Z'
        else:
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-5.5, minutes=2)[:-3] + 'Z'
        return date_to

    def reading_disp_order_from_ss_response(self, market_ids, event_name_FE,outcomes=None):
        byb_widget_market_cards_ob = self.ss_req.ss_events_to_outcome_for_markets(market_ids=market_ids)
        for card_ob in byb_widget_market_cards_ob:
            event_name = card_ob['event']['name'].replace('|', '').replace('vs', 'v')
            if event_name_FE == event_name:
                if card_ob['event']['isActive'] and card_ob['event']['eventStatusCode'] == 'A':
                    markets = card_ob['event']['children']
                    for market in markets:
                        outcomes = market['market']['children']
                    break
        else:
            raise CMSException("events is not active or Event is suspended")
        return outcomes

    def is_all_negative(self,lst):
        return all(x < 0 for x in lst)

    def is_ascending(self,lst):
        return lst == sorted(lst)

    def check_list(self,lst):
        if self.is_all_negative(lst):
            return self.is_ascending(lst)
        else:
            return False

    def test_000_preconditions(self):
        """
        DESCRIPTION: BYB Module is enabled or not in MRT
        """
        byb_ribbon_tabs = [
            (i, tab.get('title')) for i, tab in enumerate(self.cms_config.module_ribbon_tabs.visible_tabs_data)
            if tab.get('directiveName') == 'BuildYourBet'
        ]

        if byb_ribbon_tabs:
            byb_mrt_data = next((tab for tab in self.cms_config.module_ribbon_tabs.visible_tabs_data
                                 if tab.get('directiveName') == 'BuildYourBet'), None)
            if not byb_mrt_data['visible']:
                raise CMSException("Bet Builder Tab is not enabled in CMS")
            if not byb_mrt_data['bybVisble']:
                raise CMSException("BYB Widget is not enabled MRT in CMS")

            self.__class__.bet_builder_tab_name = byb_mrt_data.get('title').upper()
        # check byb widget cards have BYB Mobile or not
        byb = self.cms_config.get_byb_widget()
        self.__class__.byb_widget_container_title = byb.get('title')
        byb_widget_datas = byb.get('data')
        byb_widget_card_locations = []
        byb_widget_cards_ids = []
        self.__class__.byb_widget_market_ids = []
        for byb_widget_data in byb_widget_datas:
            byb_widget_cards_ids.append(byb_widget_data['id'])
            self.byb_widget_market_ids.append(byb_widget_data['marketId'])
            byb_widget_card_locations.append(byb_widget_data.get('locations'))
        expected_locations = ['Byb Homepage']
        if len(byb_widget_card_locations) == 0:
            self.cms_config.create_new_market_cards(title='Auto_BYB', event_id='',
                                                    market_id='', date_from=self.date_from(),
                                                    date_to=self.date_to(), locations=expected_locations)
        for expected_location in expected_locations:
            if expected_location in [item for sublist in byb_widget_card_locations for item in sublist]:
                self._logger.info('BYB Widget is enabled in Bet Builder MRT Page')
            else:
                self.cms_config.update_market_cards(market_card_id=byb_widget_cards_ids[0], locations=expected_location)

    def test_001_launch_ladscoral_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch Lads/Coral and login with valid credentials
        EXPECTED: Login should be successful
        """
        self.site.login()
        # Wait for the homepage content to load successfully.
        self.site.wait_content_state("homepage")

    def test_002_navigate_to_bet_builder_mrt_tab(self):
        """
        DESCRIPTION: Navigate to Bet builder MRT Tab
        EXPECTED: User should be navigated to Bet Builder MRT
        """
        for i in range(20):
            # Get the current Module Ribbon Tabs from the site.
            module_ribbon_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            # Check if the 'Bet Builder' tab is present.
            tab_name = next((tab for tab in module_ribbon_tabs if tab.upper() == self.bet_builder_tab_name),
                            None)
            if tab_name:
                # If the tab is found, break out of the loop.
                break
            else:
                # If the tab is not found, refresh the page and wait for content state change.
                self.device.refresh_page()
                self.site.wait_content_state_changed()

        # Click on the 'Bet Builder' module ribbon tab.
        bet_builder_module_ribbon_tab = module_ribbon_tabs.get(tab_name)
        bet_builder_module_ribbon_tab.click()       

    def test_003_verify_the_display_of_byb_widget_in_bet_builder_mrt(self):
        """
        DESCRIPTION: Verify the display of BYB Widget in Bet Builder MRT
        EXPECTED: User can able to see the BYB Widget
        """
        self.site.wait_splash_to_hide()
        self.__class__.byb_outcome_ids_FE = []
        # verifying BYB Widget container present or not
        self.__class__.byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
        self.assertTrue(self.byb_widget_containers, msg='BYB Widget container is not present in Home Page')
        for byb_widget_container_name, byb_widget_container in self.byb_widget_containers.items():
            self.assertEqual(byb_widget_container_name.upper(), self.byb_widget_container_title.upper(),
                             msg=f'Expected BYB Widget container Title from CMS: {self.byb_widget_container_title.upper()} and '
                                 f'Actual BYB Widget Container Title from FE:{byb_widget_container_name.upper()} both are not same')
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            self.assertTrue(byb_widgets, msg='BYB Widget is not present in Home Page')
            for byb_widget_name, byb_widget in byb_widgets.items():
                # verifying BYB widget cards
                self.__class__.byb_widget_name_v = byb_widget.name
                byb_sections = byb_widget.items_as_ordered_dict_inc_dup
                self.assertTrue(byb_sections, msg='BYB Widget cards is not present in Home Page')
                for byb_section_name, byb_section in byb_sections.items():
                    result = byb_section.has_card_odds()
                    self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                    self.byb_outcome_ids_FE.append(int(byb_section.card_odds.selection_id))

                count = byb_widget.byb_footer_page_counter
                numbers = re.findall(r'\d+', count)

                # Convert extracted numbers to integers
                numbers = [int(num) for num in numbers]

                # Find the highest number
                highest_number = max(numbers)
                for i in range(1, highest_number):
                    if highest_number >= i:
                        byb_widget.right_arrow.click()
                        byb_sections = byb_widget.items_as_ordered_dict_inc_dup
                        for byb_section_name, byb_section in byb_sections.items():
                            result = byb_section.has_card_odds()
                            self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                            self.byb_outcome_ids_FE.append(int(byb_section.card_odds.selection_id))
                break

            break

    def test_004_verify_the_selections_order_id_siplayed_as_per_display_order_in_the_ob(self):
        """
        DESCRIPTION: Verify the selections order id siplayed as per display order in the OB
        EXPECTED: Selections order should be as per display order in OB
        """
        # Verifying BYB Widget outcome ids are ascending order in FE
        result = self.check_list(lst=self.byb_outcome_ids_FE)
        if result:
            self.assertTrue(result, msg=f'FE Selection ids are not in ascendng order')
        else:
            outcomes = self.reading_disp_order_from_ss_response(market_ids=self.byb_widget_market_ids, event_name_FE=self.byb_widget_name_v )
            display_order_in_FE = []
            for FE_outcome_id in self.byb_outcome_ids_FE:
                for outcome in outcomes:
                    outcome_id = outcome['outcome']['id']
                    if FE_outcome_id == outcome_id:
                        disp_order = outcome['outcome']['displayOrder']
                        display_order_in_FE.append(int(disp_order))

            self.assertTrue(self.check_list(lst=display_order_in_FE),
                            msg='In FSC call display orders of selection ids are not in sort order')

    def test_005_verify_the_selections_order_for_the_two_selections_for_which_same_disporder_is_set_in_ob(self):
        """
        DESCRIPTION: Verify the selections order for the two selections for which same disporder is set in OB
        EXPECTED: Selections ID ascending order is compared and smaller one is displaed first folloed the second one
        """
        # Covered in above step

        # place bet
        for byb_widget_container_name, byb_widget_container in self.byb_widget_containers.items():
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            for byb_widget_name, byb_widget in byb_widgets.items():
                # verifying BYB widget cards
                byb_sections = byb_widget.items_as_ordered_dict
                for byb_outcome_name, byb_section in byb_sections.items():
                    result = byb_section.has_card_odds()
                    self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                    byb_section.card_odds.click()
                    break
                break
            break
        # verifying the selection in betslip
        if self.device_type == 'desktop':
            self.site.open_betslip()
            betslip = self.get_betslip_content()
            self.assertTrue(betslip, msg='Betslip is not displayed')
            singles_section = self.get_betslip_sections().Singles
            for selection_name, selection in singles_section.items():
                self.assertEqual(byb_outcome_name, selection_name, msg="both names are not same")
        else:
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertTrue(quick_bet, msg='Quick Bet content is not loading')

        # place bet
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel.selection.content
            quick_bet.amount_form.input.click()
            quick_bet.amount_form.input.value = self.bet_amount
            self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                            msg='The button "Place bet" is not active')
            self.site.quick_bet_panel.place_bet.click()
            wait_for_haul(3)            
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()