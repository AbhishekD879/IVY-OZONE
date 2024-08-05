import re
import pytest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_response_url, do_request
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.popular_bets
@pytest.mark.fanzone_popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
# This test case covers C66043619
class Test_C66043618_Verify_the_display_of_bets_based_on_your_team_module_for_the_Brand_New_user(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C66043618
    NAME: Verify the display of bets based on your team module for the Brand New user
    DESCRIPTION: This test case is to verify the display of bets based on your team module for the Brand New user
    PRECONDITIONS: 1. Bets Based On Your Team Module and Bets Based On Other Fans Module is configured and Enabled in Fanzone.
    PRECONDITIONS: 2. CMS Navigations --
    PRECONDITIONS: CMS -> Sports Pages -> Sport Categories -> Fanzone -> Bets Based On Your Team Module & Bets Based On Other Fans Module
    PRECONDITIONS: 3. CMS -> Fanzone-> Fanzones -> Fanzone Name -> Fanzone Configurations -> ON/OFF Toggle for Show Bets Based On Your Team & Show Bets Based on Other Fanzone Team.
    PRECONDITIONS: 4. User should Subscribe to any Fanzone team
    """
    keep_browser_open = True
    fanzone_your_team_positions_event_names = {}
    fe_fanzone_your_team_bet_events_names = {}
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load app and log in with a user that has at list one credit card added
        PRECONDITIONS: 2. Add selection to Betslip
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_YOUR_TEAM')[0]
        is_disabled_popular_bets = popular_bets.get('disabled')
        self.__class__.popular_bets_title = popular_bets.get('title').upper()
        self.__class__.popular_bets_no_of_max_selections = popular_bets.get('teamAndFansBetsConfig').get('noOfMaxSelections')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)

        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_OTHER_FANS')[0]
        is_disabled_popular_bets = popular_bets.get('disabled')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)

        teams = self.cms_config.get_fanzones()
        self.__class__.fanzone_team_name = next(item['name'] for item in teams)
        self.__class__.team_id = next(item.get('teamId') for item in teams)
        fanzone_data = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())['fanzoneConfiguration']
        if not fanzone_data['showBetsBasedOnYourTeam'] and not fanzone_data['showBetsBasedOnOtherFans']:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                showBetsBasedOnOtherFans=True, showBetsBasedOnYourTeam=True)

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and Login with Valid Credentials
        EXPECTED: User should launch the Application and Login Successfully
        """
        # username = self.gvc_wallet_user_client.register_new_user().username
        # self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
        #                                                              card_number='5137651100600001',
        #                                                              card_type='mastercard', expiry_month='12',
        #                                                              expiry_year='2080', cvv='111')
        # self.site.login(username=username)
        self.site.login()

    def test_002_verify_user_subscription_for_fanzone(self):
        """
        DESCRIPTION: Verify user subscription for fanzone
        EXPECTED: User should Subscribe to any Fanzone team
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # ********* Checking Team Selection page is displaying properly or not***********
        promotion_details = self.site.promotion_details.tab_content.promotion
        fanzone_syc_button = promotion_details.detail_description.fanzone_syc_button
        fanzone_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        syc_selection = self.site.show_your_colors.items_as_ordered_dict.get(self.fanzone_team_name)
        syc_selection.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(4)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        wait_for_haul(3)
        try:
            dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
            if dialog_alert_email:
                dialog_alert_email.remind_me_later.click()
        except:
            pass
        wait_for_haul(3)
        try:
            dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
            if dialog_alert_fanzone_game:
                dialog_alert_fanzone_game.close_btn.click()
        except:
            pass

    def test_003_navigate_to_fanzone(self):
        """
        DESCRIPTION: Navigate to Fanzone
        EXPECTED: Able to naviagte to the Fanzone page, and by default Now &amp; Next Tab should open
        """
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        # Create the URL for the request
        request_url = get_response_url(self, url=f'/api/fanzone/tb/{self.team_id}')
        # Send a GET request to the URL and store the response
        fanzone_response = do_request(method='GET', url=request_url)
        your_team = len(fanzone_response.get('fzYourTeamPositions', []))
        other_team = len(fanzone_response.get('fzOtherTeamPositions', []))
        if your_team == 0 or other_team == 0:
            raise SiteServeException("No premier league events available so fan team module wont be displayed")
        fan_team_module_tab = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title)
        self.assertTrue(fan_team_module_tab, msg=f' fan team module is not available IN FRONT END')

        team = self.site.fanzone.fanzone_heading.split('\n')
        team_name = team[0].upper()
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title).items_as_ordered_dict_inc_dup
        for section_name, section in sections.items():
            section.scroll_to_we()
            event_name = section.event_name.upper().split()
            self.assertIn(team_name, event_name, msg=f' team_name : "{team_name}" is not present on "{section.name}"')


    def test_004_verify_display_of_bets_based_on_your_team_module(self):
        """
        DESCRIPTION: Verify display of bets based on your team module
        EXPECTED: Able to see the bets based on your team module as per the CMS configurations
        """
        team_id = self.cms_config.get_fanzone(self.fanzone_team_name.title())['teamId']
        # Create the URL for the request
        request_url = get_response_url(self, url=f'/api/fanzone/tb/{team_id}')
        # Send a GET request to the URL and store the response
        fanzone_your_team_positions_events = do_request(method='GET', url=request_url)['fzYourTeamPositions'][:self.popular_bets_no_of_max_selections]

        for event in fanzone_your_team_positions_events:
            outcome_name = event.get('event').get('markets')[0].get('outcomes')[0].get('name')
            handicap_value = event.get('event').get('markets')[0].get('rawHandicapValue')
            template_market_name = event.get('event').get('markets')[0].get('name')
            event_name = event.get('event').get('name')

            expected_event_name = f'{outcome_name} ({handicap_value})' if handicap_value else outcome_name
            expected_outcome_name = expected_event_name + " " + template_market_name

            self.fanzone_your_team_positions_event_names[expected_outcome_name] = event_name

        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.popular_bets_title).items_as_ordered_dict_inc_dup
        for section_name, section in sections.items():
            section.scroll_to_we()
            outcome_name = section.name
            event_data = section.event_name
            pattern = r'(\w+) v (\w+)'
            team = re.search(pattern, event_data)
            if team:
                event_name = team.group(0)

            self.fe_fanzone_your_team_bet_events_names[outcome_name] = event_name

        self.assertEqual(self.fanzone_your_team_positions_event_names, self.fe_fanzone_your_team_bet_events_names, msg=f'actual events {self.fanzone_your_team_positions_event_names} are not equal to expected events {self.fe_fanzone_your_team_bet_events_names} in front end')

    def test_005_verify_the_display_of_max_number_of_betsselections_in_a_card_view_as_per_the_figma_design(self):
        """
        DESCRIPTION: Verify the display of max number of bets/selections in a card view as per the figma design
        EXPECTED: User could able to see the max number of bets in a card view as per the figma and max number configured in the cms
        """
        # covered in above step
        pass

    def test_006_click_on_any_selection(self):
        """
        DESCRIPTION: Click on any selection
        EXPECTED: User can able to add the selections to the betslip successfully
        """
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.popular_bets_title).items_as_ordered_dict_inc_dup
        for section in sections:
            sections.get(section).bet_button.click()
            break
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            quick_bet.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.close()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

    def test_007_navigate_to_betslip_page_and_place_a_bet(self):
        """
        DESCRIPTION: Navigate to Betslip page and place a bet
        EXPECTED: Able to navigate and place a bet successfully
        """
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title).items_as_ordered_dict_inc_dup
        for section in sections:
            sections.get(section).bet_button.click()
            break
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            wait_for_haul(3)
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

        # covered in above step
        pass

    def test_008_add_multiple_selections_to_the_betslip_and_verify_place_a_bet(self):
        """
        DESCRIPTION: Add multiple selections to the betslip and verify place a bet
        EXPECTED: Multiple bets are formed and able to place a bets successfully
        """
        #multiple bet placement is not possible as bets are maximum from same team

