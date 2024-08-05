import pytest
from voltron.environments import constants as vec
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@pytest.mark.bet_share
@pytest.mark.adhoc_suite
@pytest.mark.timeout(1000)
@pytest.mark.other
@vtest
class Test_C65969090_Verify_the_flexibility_to_configure_headers_and_sub_headers_in_Lucky_dip_Bet_share_Configurations(BaseGolfTest):
    """
    TR_ID: C65969090
    NAME: Verify the flexibility to configure headers and sub-headers in Lucky dip Bet share Configurations
    DESCRIPTION: This testcase verifies the flexibility to configure headers and sub-headers
    PRECONDITIONS: 1. Bet sharing should be configured in CMS page.
    PRECONDITIONS: 2. Go to CMS-&gt;Bet sharing-&gt;enable. Note: All bet share card details can be configured  and managed via CMS.
    """
    keep_browser_open = True
    bet_amount = 0.10
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    end_date = get_date_time_as_string(days=30,time_format="%Y-%m-%dT%H:%M")

    @classmethod
    def custom_tearDown(cls, **kwargs):
        openBetControl_list = {
                                "DATE": {"isSelected": True},
                                "SELECTIONNAME": {"isSelected": True},
                                "ODDS": {"isSelected": True},
                                "RETURNS": {"isSelected": True}

                                }
        cms_config = cls.get_cms_config()
        cms_config.update_luckyDip_BetSharing_configuration(enable = True, openBetControl_list = openBetControl_list)

    def enter_value_using_keyboard(self, value, on_betslip=True):
        keyboard = self.get_betslip_content().keyboard if on_betslip \
            else self.site.quick_bet_panel.selection.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=value)

    def get_luckydip_market(self):
        query_params = (self.ss_query_builder.add_filter(simple_filter(LEVELS.CLASS,ATTRIBUTES.CATEGORY_ID,OPERATORS.EQUALS,self.ob_config.football_config.category_id))
                        .add_filter(simple_filter(LEVELS.CLASS,ATTRIBUTES.IS_ACTIVE))
                        .add_filter(simple_filter(LEVELS.CLASS,ATTRIBUTES.SITE_CHANNELS,OPERATORS.CONTAINS,'M'))
                        .add_filter(simple_filter(LEVELS.CLASS,ATTRIBUTES.HAS_OPEN_EVENT)))
        class_req = self.ss_req.ss_class(query_builder = query_params)
        class_ids = [req.get('class').get('id') for req in class_req]
        query_builder = (self.ss_query_builder.add_filter(simple_filter(LEVELS.EVENT,ATTRIBUTES.SITE_CHANNELS,OPERATORS.CONTAINS,'M'))
                         .add_filter(simple_filter(LEVELS.EVENT,ATTRIBUTES.EVENT_SORT_CODE,OPERATORS.INTERSECTS,
                                                   'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20'))
                         .add_filter(simple_filter(LEVELS.EVENT,ATTRIBUTES.SUSPEND_AT_TIME,OPERATORS.GREATER_THAN, self.start_date_minus)))
        events = self.ss_req.ss_event_to_outcome_for_class(class_id = class_ids,query_builder = query_builder)
        lucky_dip_event = []
        for event in events:
            markets = event.get('event').get('children')
            if markets:
                for market in markets:
                    if market.get('market').get('templateMarketName') == 'LUCKY DIP':
                        lucky_dip_event.append(event)
                        break
        if not lucky_dip_event:
            raise SiteServeException('no events is available with luckydip market')
        else:
            return lucky_dip_event

    def get_open_bet_share_Preferences_in_cms(self):
        bet_sharing_config = self.cms_config.get_bet_sharing_configuration()
        openBet_Control_list = bet_sharing_config.get("luckyDipBetSharingConfigs").get('openBetControl')
        open_bet_Sharing_preferences = [openBet_Control['name'].upper() for openBet_Control in openBet_Control_list if
                                          openBet_Control['isSelected']]
        return open_bet_Sharing_preferences

    def get_open_bet_sharing_button_components_in_FE(self):
        self.execute_bet_placement()
        luckey_dip_got_it_panel = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5), timeout=5)
        self.assertTrue(luckey_dip_got_it_panel, msg='Lucky Dip Animation is not displayed to the user')
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        self.site.quick_bet_panel.lucky_dip_outright_bet_receipt.lucky_dip_close_button.click()
        self.site.open_my_bets_open_bets()
        open_bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list,
                                    name='waiting for bets found on "Open Bets" page', expected_result=True,
                                    timeout=20)
        self.assertTrue(open_bets, msg='No bets found in open bet')
        open_bet_items = open_bets.items_as_ordered_dict
        lucky_dip_section = next((open_bet_item for open_bet_item_name, open_bet_item in open_bet_items.items() if
                                  open_bet_item_name.startswith('LUCKY DIP')), None)
        bet_name = lucky_dip_section.items_as_ordered_dict
        self.assertTrue(bet_name, msg='No open bets are available for lucky dip')
        bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        share_button = bet.bet_share_button
        self.assertTrue(share_button, msg='share button is not present in open bet page')
        share_button.click()
        self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_SHARE, timeout=5)
        share_dialog = self.site.dialog_manager.items_as_ordered_dict.get(vec.dialogs.DIALOG_MANAGER_SHARE)
        actual_share_components = share_dialog.items_as_ordered_dict.keys()
        actual_share_components_list = [''.join(actual_share_component.split(" ")[1:]).upper() for actual_share_component in actual_share_components]
        return actual_share_components_list

    def execute_bet_placement(self):
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state('EVENTDETAILS')
        edp_market_sections = wait_for_result(lambda :self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict,timeout=10)
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),None)
        lucky_dip_section = edp_market_sections.get(market_key)
        lucky_dip_section.scroll_to()
        lucky_dip_section.expand()
        lucky_dip_section.odds.click()

        # quick_bet = self.site.quick_bet_panel.selection
        quick_bet = wait_for_result(lambda: self.site.quick_bet_panel.selection, timeout=5)
        self.assertTrue(quick_bet, msg="lucky dip landing page is not displayed for place bet")
        wait_for_haul(3)
        quick_bet_input = quick_bet.content.amount_form.input
        quick_bet_input.click()
        if not quick_bet.keyboard.is_displayed():
            quick_bet_input.click()
        self.assertTrue(quick_bet.content.amount_form.is_active(), msg='"Stake" box is not highlighted')
        self.assertTrue(quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10),
                        msg='Numeric keyboard is not opened')
        self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
        place_bet_button = self.site.quick_bet_panel.place_bet
        self.assertTrue(place_bet_button, msg="place bet button is not available")
        self.site.quick_bet_panel.place_bet.click()
        lucky_dip_got_it_animation = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=10),
                                                     bypass_exceptions=VoltronException, timeout=5)
        self.assertTrue(lucky_dip_got_it_animation, msg='Lucky Dip Animation is not displayed to the user')

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Go to General Configuration
        EXPECTED: Able to see the general configuration details
        """
        # self.get_luckydip_market()
        bet_sharing_config = self.cms_config.get_bet_sharing_configuration()
        lucky_dip_bet_share_config = bet_sharing_config.get("luckyDipBetSharingConfigs")
        lucky_dip_bet_share_enable = lucky_dip_bet_share_config.get('enable')
        if lucky_dip_bet_share_enable == False:
            self.cms_config.update_luckyDip_BetSharing_configuration(enable = True)
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'Lucky Dip is not Enabled in CMS')
        # event = self.get_active_lucky_dip_events(number_of_events=1, all_available_events=True, category_id =self.ob_config.football_config.category_id)[0]['event']
        event = self.get_luckydip_market()[0]['event']
        self.__class__.sport_name = event['categoryCode'].upper()
        self.__class__.event_name = event['name'].upper()
        self.__class__.event_section_name = event['className'].upper() + " - " + event['typeName'].upper()
        self.__class__.eventID = event['id']

    def test_001_launch_the_cms_url(self):
        """
        DESCRIPTION: Launch the CMS url
        EXPECTED: CMS url should launch successfully.
        """
        # already covered

    def test_002_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should able to login successfully
        """
        # already covered

    def test_003_click_on_bet_sharing_under_main_section(self):
        """
        DESCRIPTION: Click on Bet Sharing under Main section
        EXPECTED: Should able to navigate Bet Sharing menu configuration page
        """
        # already covered

    def test_004_go_to_general_configuration(self):
        """
        DESCRIPTION: Go to General Configuration
        EXPECTED: Able to see the general configuration details
        """
        # already covered

    def test_005_enter_in_the_bet_sharing_tab(self):
        """
        DESCRIPTION: Enter in the Bet sharing tab
        EXPECTED: User will be having the flexibility to configure bet sharing FTP configurations, copy and link to images
        """
        self.site.login()
        self.execute_bet_placement()
        luckey_dip_got_it_panel = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5),timeout=5)
        self.assertTrue(luckey_dip_got_it_panel, msg='Lucky Dip Animation is not displayed to the user')
        lucky_Dip_share_button = self.site.lucky_dip_got_it_panel.has_lucky_Dip_share_button()
        self.assertTrue(lucky_Dip_share_button, msg='lucky dip share button is not available')
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        self.site.quick_bet_panel.lucky_dip_outright_bet_receipt.lucky_dip_close_button.click()
        self.cms_config.update_luckyDip_BetSharing_configuration(enable=False)
        wait_for_haul(30)
        self.execute_bet_placement()
        luckey_dip_got_it_panel = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5), timeout=5)
        self.assertTrue(luckey_dip_got_it_panel, msg='Lucky Dip Animation is not displayed to the user')
        lucky_Dip_share_button = self.site.lucky_dip_got_it_panel.has_lucky_Dip_share_button(expected_result=False)
        self.assertFalse(lucky_Dip_share_button, msg='lucky dip share button is available')
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        self.site.quick_bet_panel.lucky_dip_outright_bet_receipt.lucky_dip_close_button.click()

    def test_006_verify_open_betswon_betslost_bets_user_preferences(self):
        """
        DESCRIPTION: Verify Open bets/Won bets/Lost bets user preferences
        EXPECTED: Able to enable and disable the preferences, saved and reflected in FE successfully
        """
        openBetControl_list = {
                                "DATE":{"isSelected":False},
                                "SELECTIONNAME":{"isSelected":False}
                                }
        self.cms_config.update_luckyDip_BetSharing_configuration(enable=True,openBetControl_list = openBetControl_list)
        wait_for_haul(30)
        actual_share_components = self.get_open_bet_sharing_button_components_in_FE()
        sorted_actual_share_components = sorted(actual_share_components)
        expected_share_components = self.get_open_bet_share_Preferences_in_cms()
        sorted_expected_share_components = sorted(expected_share_components)
        self.assertListEqual(sorted_actual_share_components,sorted_expected_share_components,msg=f'actual share component {sorted_actual_share_components} is '
                            f'not equal to expected share component {sorted_expected_share_components}')
        modified_openBetControl_list = {
                                        "DATE": {"isSelected": True},
                                        "SELECTIONNAME": {"isSelected": True}
                                        }
        self.cms_config.update_luckyDip_BetSharing_configuration(openBetControl_list = modified_openBetControl_list)
        wait_for_haul(30)
        actual_modified_share_components = self.get_open_bet_sharing_button_components_in_FE()
        sorted_actual_modified_share_components = sorted(actual_modified_share_components)
        expected_modified_share_components = self.get_open_bet_share_Preferences_in_cms()
        sorted_expected_modified_share_components = sorted(expected_modified_share_components)
        self.assertListEqual(sorted_actual_modified_share_components, sorted_expected_modified_share_components,msg=f'actual share component {sorted_actual_modified_share_components} is '
                                 f'not equal to expected share component {sorted_expected_modified_share_components}')
