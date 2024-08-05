import pytest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_response_url, do_request
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import  wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone_popular_bets
@pytest.mark.fanzone_reg_tests
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.other
@vtest
class Test_C66044313_Verify_adding_a_selection_to_betslip_from_Bets_based_on_other_fans_module(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C66044313
    NAME: Verify adding a selection to betslip from Bets based on other fans module
    DESCRIPTION: This testcase verifies adding a selection to betslip from Bets based on other fans module
    PRECONDITIONS: 1. Navigation in CMS -> CMS -> Sports categories page->Fanzone- Bets based on other fans module should be enabled.
    PRECONDITIONS: 2. CMS -> Fanzone -> Fanzones -> Click on Fanzone name -> Go to Fanzone configurations -> Toggle should be on for -> Show bets based on your team and Show bets based on other Fanzone Team
    """
    keep_browser_open = True
    fanzone_your_fellow_team_bet_events_names = {}
    fe_fanzone_your_fellow_team_bet_events_names = {}
    bet_amount = 0.1

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
        self.__class__.popular_bets_title_sub_team = popular_bets.get('title').upper()
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)

        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_OTHER_FANS')[0]
        is_disabled_popular_bets = popular_bets.get('disabled')
        self.__class__.popular_bets_title_fan_bets = popular_bets.get('title').upper()


        self.__class__.popular_bets_no_of_max_selections = popular_bets.get('teamAndFansBetsConfig').get(
            'noOfMaxSelections')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)
        home_team = vec.fanzone.TEAMS_LIST.liverpool.upper()
        self.__class__.team_id = self.cms_config.get_fanzone(home_team.title())['teamId']
    def test_001_launch_and_log_in_to_the_application(self):
        """
        DESCRIPTION: Launch and log in to the Application
        EXPECTED: User should launch and log in to the Application Successfully
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard', expiry_month='12',
                                                                     expiry_year='2080', cvv='111')
        self.site.login(username=username)

    def test_002_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: Fanzone page should load successfully
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
        syc_selection = self.site.show_your_colors.items_as_ordered_dict.get('Liverpool')
        syc_selection.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(4)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed()
        wait_for_haul(4)
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

        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        # Create the URL for the request
        request_url = get_response_url(self, url=f'/api/fanzone/tb/{self.team_id}')
        # Send a GET request to the URL and store the response
        #checking that premier league events are available or not if not then the module wont be displayed
        fanzone_response = do_request(method='GET', url=request_url)
        your_team = len(fanzone_response.get('fzYourTeamPositions', []))
        other_team = len(fanzone_response.get('fzOtherTeamPositions', []))
        if your_team == 0 or other_team == 0:
            raise SiteServeException("No premier league events available so fan team module wont be displayed")

        fan_team_module_tab = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_sub_team)
        self.assertTrue(fan_team_module_tab, msg=f' fan team module is not available IN FRONT END')

        team = self.site.fanzone.fanzone_heading.split('\n')
        team_name = team[0].upper()
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_sub_team).items_as_ordered_dict_inc_dup
        for section_name, section in sections.items():
            section.scroll_to_we()
            event_name = section.event_name.upper().split()
            self.assertIn(team_name, event_name,
                             msg=f' team_name : "{team_name}" is not present on "{section.name}"')

    def test_003_verify_the_display_of_bets_based_on_other_fans_carousel_in_fanzone(self):
        """
        DESCRIPTION: Verify the Display of Bets based on other Fans Carousel in Fanzone
        EXPECTED: User should be able to see "Bets based on other fans" module
        """
        #covered in below step


    def test_004_verify_the_module(self):
        """
        DESCRIPTION: Verify the module
        EXPECTED: It should be in Open mode by default
        """
        fan_bets_module_tab = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_fan_bets)
        self.assertTrue(fan_bets_module_tab, msg=f' fan bets module is not available IN FRONT END')

        request_url = get_response_url(self, url=f'/api/fanzone/tb/{self.team_id}')
        fanzone_your_fellow_team_bet_events = do_request(method='GET', url=request_url)['fzOtherTeamPositions'][
                                              :self.popular_bets_no_of_max_selections]
        for event in fanzone_your_fellow_team_bet_events:
            outcome_name = event.get('event').get('markets')[0].get('outcomes')[0].get('name')
            handicap_value = event.get('event').get('markets')[0].get('rawHandicapValue')
            event_name = event.get('event').get('name')
            template_market_name = event.get('event').get('markets')[0].get('name')
            expected_event_name = f'{outcome_name} ({handicap_value})' if handicap_value else outcome_name

            event_name = expected_event_name + " " + event_name
            self.fanzone_your_fellow_team_bet_events_names[event_name] = template_market_name

        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_fan_bets).items_as_ordered_dict_inc_dup
        for section_name, section in sections.items():
            outcome_name = section.name
            market = section.market_name
            event_name = market.split(' - ')[1].split('|')[0].strip()
            market_name = market.split(' - ')[0].strip()
            expected_event_name = outcome_name + " " + event_name
            self.fe_fanzone_your_fellow_team_bet_events_names[expected_event_name] = market_name

        self.assertEqual(self.fanzone_your_fellow_team_bet_events_names,
                         self.fe_fanzone_your_fellow_team_bet_events_names,
                         msg=f'actual events {self.fanzone_your_fellow_team_bet_events_names} are not equal to expected events {self.fe_fanzone_your_fellow_team_bet_events_names} in front end')

    def test_005_verify_the_option_to_open_and_collapse_the_module_by_clicking_the_chevron(self):
        """
        DESCRIPTION: Verify the option to open and collapse the module by clicking the chevron
        EXPECTED: User should be able to open and collapse the module
        """
        other_fans_bets = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_fan_bets)
        other_fans_bets.collapse()
        self.assertFalse(other_fans_bets.is_expanded(), msg=f'section is not Collapsed')
        other_fans_bets.expand()
        self.assertTrue(other_fans_bets.is_expanded(), msg=f'section is not expanded')

    def test_006_verify_adding_a_selection_to_betslip_from_bets_based_on_other_fans_module(self):
        """
        DESCRIPTION: Verify adding a selection to betslip from Bets based on other fans module
        EXPECTED: Selection should be added successfully to Betslip and able to place a bet
        """
        # bet placement
        # quickbet and single bet placement
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_fan_bets)
        bet_button = sections.first_item[1].bet_button
        bet_button.click()
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

        ##############bet_placement from betslip#################
        if self.device_type == 'mobile':
            sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
                self.popular_bets_title_fan_bets)
            bet_button = sections.first_item[1].bet_button
            bet_button.click()
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            wait_for_haul(3)
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.close_button.click()


    def test_007_verify_adding_multiple_selections_to_betslip(self):
        """
        DESCRIPTION: Verify adding multiple selections to Betslip
        EXPECTED: All the multiples should form like Double,Treble, Acca and so on and able to place a bet successfully
        """
        # Multiple betplacement
        sections = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(
            self.popular_bets_title_fan_bets).items_as_ordered_dict_inc_dup
        count = 0
        for section_key, section_value in sections.items():
            section_value.bet_button.click()
            count += 1
            if self.device_type == 'mobile' and count == 1:
                self.site.wait_for_quick_bet_panel()
                self.site.quick_bet_panel.add_to_betslip_button.click()
                self.site.wait_quick_bet_overlay_to_hide()
                wait_for_haul(3)
            if count == 2:
                break
        self.site.open_betslip()
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()

    def test_008_log_out_and_login_with_newly_created_user(self):
        """
        DESCRIPTION: Log out and Login with newly created user
        EXPECTED: User should be created successfully
        """
        #covered in above step

    def test_009_subscribe_to_any_of_the_fanzone_team(self):
        """
        DESCRIPTION: Subscribe to any of the Fanzone team
        EXPECTED: After subscription--user should be able to see both the modules
        """
        #covered in above step

    def test_010_verify_adding_selection_to_betslip_from_bets_based_on_other_fans_module_and_place_multiple_bets(self):
        """
        DESCRIPTION: Verify adding selection to Betslip from Bets based on other fans module and place multiple bets
        EXPECTED: Selections should be added successfully and able to place a bet
        """
        #covered in above step
