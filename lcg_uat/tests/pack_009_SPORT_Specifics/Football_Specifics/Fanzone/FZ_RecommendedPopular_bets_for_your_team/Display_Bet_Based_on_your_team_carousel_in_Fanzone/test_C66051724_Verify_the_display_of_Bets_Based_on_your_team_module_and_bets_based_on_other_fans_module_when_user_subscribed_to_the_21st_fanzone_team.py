import tests
import pytest
from time import sleep
from tests.base_test import vtest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import get_response_url, do_request
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.fanzone_popular_bets
@pytest.mark.fanzone_reg_tests
@pytest.mark.popular_bets
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66051724_Verify_the_display_of_Bets_Based_on_your_team_module_and_bets_based_on_other_fans_module_when_user_subscribed_to_the_21st_fanzone_team(BaseBetSlipTest):
    """
    TR_ID: C66051724
    NAME: Verify the display of Bets Based on your team module and bets based on other fans module when user subscribed to the 21st fanzone team
    DESCRIPTION: This test case is to verify the display of Bets Based on your team module and bets based on other fans module when user subscribed to the 21st fanzone team
    PRECONDITIONS: Bet Based on your team and Bets based on other fans modules is configured and enabled in CMS
    """
    keep_browser_open = True
    fanzone_name = "Fanzone FC"

    def email_opt_and_fanzone_games_popup_handeling(self):
        # **********************************************************************************
        dialog_alert_email = wait_for_result(
            lambda: self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN,
                                              verify_name=False),
            timeout=3,
            name=f'Dialog "{vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN}" to display',
            bypass_exceptions=VoltronException)
        if dialog_alert_email and dialog_alert_email.name.title() == vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN.title():
            dialog_alert_email.remind_me_later.click()
        # **********************************************************************************
        dialog_alert_fanzone_game = wait_for_result(
            lambda: self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES,
                                              verify_name=False),
            timeout=3,
            name=f'Dialog "{vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES}" to display',
            bypass_exceptions=VoltronException)
        if dialog_alert_fanzone_game and dialog_alert_fanzone_game.name.title() == vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES.title():
            dialog_alert_fanzone_game.close_btn.click()

    def fanzone_21st_team_popular_bets_modules_bet_placement(self, module_name):
        # quickbet and single bet placement
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            module_name).items_as_ordered_dict_inc_dup
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
            # placing single bet
            for section in sections:
                sections.get(section).bet_button.click()
                break
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            wait_for_haul(3)
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

        # Multiple betplacement
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            module_name).items_as_ordered_dict_inc_dup
        count = 0
        for section in sections:
            sections.get(section).scroll_to_we()
            sections.get(section).bet_button.click()
            if self.device_type == "mobile" and count == 0:
                self.site.quick_bet_panel.close()
                wait_for_haul(3)
            count += 1
            if count == 2:
                break
        self.site.open_betslip()
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_000_precondition(self):
        """
        Description : Checking whether Fanzone is enabled in cms or not.
        Description : and checking whether yor team module is enabled or not for 21st team in cms.
        Description : and also checking whether other team module is enabled or not for 21st team in cms.
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_YOUR_TEAM')[0]
        is_disabled_popular_bets = popular_bets.get('disabled')
        self.__class__.popular_bets_your_team_title = popular_bets.get('title').upper()
        self.__class__.popular_bets_your_team_no_of_max_selections = popular_bets.get('teamAndFansBetsConfig').get(
            'noOfMaxSelections')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)
        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_OTHER_FANS')[0]
        is_disabled_popular_bets = popular_bets.get('disabled')
        self.__class__.popular_bets_other_team_title = popular_bets.get('title').upper()
        self.__class__.popular_bets_other_team_no_of_max_selections = popular_bets.get('teamAndFansBetsConfig').get(
            'noOfMaxSelections')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)
        teams = self.cms_config.get_fanzones()
        for item in teams:
            if item.get('name').upper() == self.fanzone_name.upper():
                self.__class__.fanzone_team_name = item.get('name')
        fanzone_data = self.cms_config.get_fanzone(self.fanzone_team_name)['fanzoneConfiguration']
        if not fanzone_data['showNowNext'] or not fanzone_data['showBetsBasedOnYourTeam'] or not fanzone_data['showBetsBasedOnOtherFans']:
            self.cms_config.update_fanzone(self.fanzone_team_name, showNowNext=True , showBetsBasedOnOtherFans=True, showBetsBasedOnYourTeam=True)

    def test_001_launch_the_ladbrokes_application_and_login_with_new_user(self):
        """
        DESCRIPTION: Launch the ladbrokes application and login with new user
        EXPECTED: User could be able to launch the application and login successfully
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard', expiry_month='12',
                                                                     expiry_year='2080', cvv='111')
        self.site.login(username=username)

    def test_002_navigate_to_the_football_page_and_verify_the_fanzone_syc_pop_up_display(self):
        """
        DESCRIPTION: Navigate to the football page and verify the fanzone syc pop-up display
        EXPECTED: User can navigate to the football page and can see the fanzone syc pop-up
        """
        self.device.navigate_to(url=f'https://{tests.HOSTNAME}/sport/football')
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        self.assertTrue(self.dialog_fb.is_displayed(),
                        msg='"SYC overlay"is not displayed on Football landing page for new user')

    def test_003_click_on_im_in_cta_and_select_the_21st_fanzone_team(self):
        """
        DESCRIPTION: Click on I'm in CTA and select the 21st fanzone team
        EXPECTED: user could be able to click on the "I'm" in CTA and can select the 21st fanzone team
        """
        self.dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, name='All Fanzones are displayed',
                        timeout=5)
        # # ******** checking "i_dont_support_any_teams" is there or not in front end ********
        i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')
        self.site.show_your_colors.scroll_to_we(self.site.show_your_colors.i_dont_support_any_teams)
        self.site.show_your_colors.i_dont_support_any_teams.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                           verify_name=False)
        self.assertTrue(dialog.select_custom_team_name_input, msg='Choice name has not Displayed to entered input')
        self.assertTrue(dialog.exit_button.is_displayed(), msg='CTA Exit Button Not Displayed')
        self.assertTrue(dialog.confirm_button.is_displayed(), msg='CTA Confirm Button Not Displayed')
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS, verify_name=False)
        # *************************************************************************
        self.dialog.select_custom_team_name_input = 'ABC'
        self.dialog.confirm_button.click()
        sleep(3)
        msg_dialog = wait_for_result(
            lambda: self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_THANK_YOU, verify_name=False),
            timeout=3,
            name=f'Dialog "{vec.dialogs.DIALOG_MANAGER_THANK_YOU}" to display',
            bypass_exceptions=VoltronException)
        self.assertTrue(msg_dialog, msg="Thank you message pop up is not displayed")
        msg_dialog.exit_button.click()
        self.email_opt_and_fanzone_games_popup_handeling()

    def test_004_click_on_submit_cta(self):
        """
        DESCRIPTION: click on submit CTA
        EXPECTED: User could submit and subscribed to the 21st fanzone team successfully
        """
        # covered in above step [test_003]

    def test_005_navigate_to_the_fanzone_page(self):
        """
        DESCRIPTION: Navigate to the Fanzone page
        EXPECTED: User can navigate to the fanzone page successfully
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
        else:
            self.device.refresh_page()
            self.navigate_to_page('Homepage')
            self.site.wait_content_state('Homepage')
            self.assertTrue(self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE).click()
            self.email_opt_and_fanzone_games_popup_handeling()
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}" is not same expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_006_verify_the_display_of_bets_based_on_your_team_module_and_bets_based_on_other_fans_modules(self):
        """
        DESCRIPTION: Verify the display of Bets based on your team module and Bets based on other fans modules
        EXPECTED: user can see the Bets based on your team module and Bets based on other fans modules
        """
        modules_data = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict
        self.assertTrue(modules_data.get(self.popular_bets_your_team_title),
                        msg=f'"Bets based on your team" module "{self.popular_bets_your_team_title}" is not present in front end')
        self.assertTrue(modules_data.get(self.popular_bets_other_team_title),
                        msg=f'"Bets based on other fans" module "{self.popular_bets_other_team_title}" is not present in front end')

        # ***********verifying Bets based on your team module data in front end **************
        team_id = self.cms_config.get_fanzone(self.fanzone_team_name)['teamId']
        # Create the URL for the request
        request_url = f'https://trending-bets.beta.ladbrokes.com/api/fanzone/tb/{team_id}'
        # Send a GET request to the URL and store the response
        fanzone_your_team_positions_events = do_request(method='GET', url=request_url)['fzYourTeamPositions'][:self.popular_bets_your_team_no_of_max_selections]
        fanzone_your_team_positions_event_response_data = []
        for event in fanzone_your_team_positions_events:
            event_name = event.get('event').get('markets')[0].get('outcomes')[0].get('name')
            handicap_value = event.get('event').get('markets')[0].get('rawHandicapValue')
            template_market_name = event.get('event').get('markets')[0].get('name')
            expected_event_name = f'{event_name} ({handicap_value})' if handicap_value else event_name
            fanzone_your_team_positions_event_response_data.append(f'{expected_event_name} {template_market_name}')

        actual_your_team_module_event_data_fe = []
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.popular_bets_your_team_title)
        events = sections.items_as_ordered_dict_inc_dup
        for event in events.values():
            event.scroll_to_we()
            expected_event_name = event.name
            actual_your_team_module_event_data_fe.append(expected_event_name)

        self.assertListEqual(actual_your_team_module_event_data_fe, fanzone_your_team_positions_event_response_data,
                             msg=f'expected event name and market name from '
                                 f'frontend:{actual_your_team_module_event_data_fe} is not available'
                                 f' in response:{fanzone_your_team_positions_event_response_data}')
        self.assertLessEqual(len(events), int(self.popular_bets_your_team_no_of_max_selections),
                             msg=f'the number of bets in a card view as per the figma frontend:{len(events)}'
                                 f'and max number configured in the cms{int(self.popular_bets_your_team_no_of_max_selections)}')

        # ************* verifying Bets based on other fans module data in front end **************
        fanzone_your_team_positions_events = do_request(method='GET', url=request_url)['fzOtherTeamPositions'][
                                             :self.popular_bets_other_team_no_of_max_selections]
        fanzone_other_team_module_event_response_data = []
        for event in fanzone_your_team_positions_events:
            team_name = event.get('event').get('name')
            event_name = event.get('event')['markets'][0]['outcomes'][0]['name']
            handicap_value = event.get('event').get('markets')[0].get('rawHandicapValue')
            expected_event_name = f'{event_name} ({handicap_value})' if handicap_value else event_name
            fanzone_other_team_module_event_response_data.append(f'{expected_event_name} {team_name}')

        actual_other_team_module_event_data_fe = []
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.popular_bets_other_team_title)
        events = sections.items_as_ordered_dict_inc_dup
        for event in events.values():
            event.scroll_to_we()
            template_market_name = event.market_name.split(' - ')[1].split('|')[0].strip()
            expected_event_name = event.name
            actual_other_team_module_event_data_fe.append(f'{expected_event_name} {template_market_name}')

        self.assertListEqual(fanzone_other_team_module_event_response_data, actual_other_team_module_event_data_fe,
                             msg=f'expected event name and market name from '
                                 f'frontend:{fanzone_other_team_module_event_response_data} is not available'
                                 f' in response:{actual_other_team_module_event_data_fe}')
        self.assertLessEqual(len(events), int(self.popular_bets_other_team_no_of_max_selections),
                             msg=f'the number of bets in a card view as per the figma frontend:{len(events)}'
                                 f'and max number configured in the cms{int(self.popular_bets_other_team_no_of_max_selections)}')

        # Placing single nad multiple bet for both "your team" and "other team "modules
        self.fanzone_21st_team_popular_bets_modules_bet_placement(module_name=self.popular_bets_your_team_title)
        self.fanzone_21st_team_popular_bets_modules_bet_placement(module_name=self.popular_bets_other_team_title)
