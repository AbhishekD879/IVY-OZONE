import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.helpers import get_response_url , do_request
from voltron.utils.waiters import wait_for_haul, wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod # Ladbrokes only functionality
# @pytest.mark.hl
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.fanzone_popular_bets
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66067965_Verify_Bets_Based_on_your_team_module_and_Bets_based_on_other_fans_module_in_CMS(BaseBetSlipTest,BaseDataLayerTest,BaseUserAccountTest):
    """
    TR_ID: C66067965
    NAME: Verify "Bets Based on your team module" and "Bets based on other fans module" in CMS
    DESCRIPTION: This testcase verifies Bets based on your team and Bets based on other fans module in CMS
    PRECONDITIONS: CMS is launched and login with Valid Credentials
    """
    keep_browser_open = True

    def test_001_launch_the_cms_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the CMS and login with valid credentials
        EXPECTED: Able to launch CMS and login successfully
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_YOUR_TEAM')[0]
        self.__class__.your_team_module_name = popular_bets.get('title').upper()
        self.__class__.count_of_items_based_on_your_team = popular_bets.get('teamAndFansBetsConfig').get('noOfMaxSelections')
        is_disabled_popular_bets = popular_bets.get('disabled')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)

        popular_bets = self.cms_config.get_sport_module(sport_id=160, module_type='BETS_BASED_ON_OTHER_FANS')[0]
        self.__class__.other_team_module_name = popular_bets.get('title').upper()
        self.__class__.count_of_items_based_on_other_team = popular_bets.get('teamAndFansBetsConfig').get('noOfMaxSelections')
        is_disabled_popular_bets = popular_bets.get('disabled')
        if is_disabled_popular_bets:
            self.cms_config.change_sport_module_state(sport_module=popular_bets)

        teams = self.cms_config.get_fanzones()
        self.__class__.fanzone_team_name = teams[0]['name']
        self.__class__.team_id = teams[0]['teamId']
        fanzone_data = self.cms_config.get_fanzone(self.fanzone_team_name)['fanzoneConfiguration']
        if not fanzone_data['showBetsBasedOnYourTeam'] or not fanzone_data['showBetsBasedOnOtherFans']:
            self.cms_config.update_fanzone(self.fanzone_team_name, showBetsBasedOnOtherFans=True, showBetsBasedOnYourTeam=True)

    def test_002_navigate_to_the_fanzone_in_the_sports_categories__ampgt_sports__ampgt_sports_category__ampgt_fanzone(self):
        """
        DESCRIPTION: Navigate to the Fanzone in the Sports Categories -&amp;gt; Sports -&amp;gt; Sports Category -&amp;gt; Fanzone
        EXPECTED: Able to navigate to the Fanzone page
        """
        # already covered in above steps

    def test_003_verify_the_display_of_bet_based_on_your_team_and_bets_based_on_other_fans_modules(self):
        """
        DESCRIPTION: Verify the display of Bet Based on your team and Bets based on other fans modules
        EXPECTED: Able to see the Bet Based on your team and Bets based on other fans modules
        """
        # already covered in above steps

    def test_004_click_on_bet_based_on_your_team_module(self):
        """
        DESCRIPTION: Click on Bet Based on your team module
        EXPECTED: Able to navigate to the Bet Based on your team module page
        """
        # already covered in above steps

    def test_005_verify_the_activeinactive_check_box_in_bet_based_on_your_team_module(self):
        """
        DESCRIPTION: Verify the Active/Inactive check box in Bet Based on your team module
        EXPECTED: Able to check/Uncheck the Active check box
        """
        # already covered in above steps

    def test_006_click_on_save_changes_and_verify(self):
        """
        DESCRIPTION: Click on Save Changes and Verify
        EXPECTED: Able to Save the Changes Successfully and reflected in FE
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard', expiry_month='12',
                                                                     expiry_year='2080', cvv='111')
        self.site.login(username=username)
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
        try :
            dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
            if dialog_alert_fanzone_game:
                dialog_alert_fanzone_game.close_btn.click()
        except:
            pass
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT, msg=f'Actual Tab "{current_tab}", is not same expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        # Create the URL for the request
        request_url = get_response_url(self, url=f'/api/fanzone/tb/{self.team_id}')
        # Send a GET request to the URL and store the response
        fanzone_response = do_request(method='GET', url=request_url)
        your_team = len(fanzone_response.get('fzYourTeamPositions', []))
        other_team = len(fanzone_response.get('fzOtherTeamPositions', []))
        if your_team == 0 or other_team == 0:
            raise SiteServeException("No premier league events available so fan team module wont be displayed")
        popular_bets_based_on_your_team = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.your_team_module_name)
        self.assertTrue(popular_bets_based_on_your_team, msg='"popular_bets_based_on_your_team" item is not present ')
        fanzone_heading = self.site.fanzone.fanzone_heading.split('\n')[0]
        self.assertEqual(fanzone_heading, self.fanzone_team_name,
                         msg=f"Actual heading is {fanzone_heading} expected is not same as "f"{self.fanzone_team_name}")
        # checking whether selected fanzone teams data is correct or not
        events_data = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.your_team_module_name).items_as_ordered_dict
        for event_name, event in events_data.items():
            event.scroll_to()
            backed_text = event.event_name.upper()
            self.assertIn(self.fanzone_team_name.upper(), backed_text,
                          msg=f"Fanzone team name {self.fanzone_team_name.upper()} not found in {backed_text} ")

        count_on_fe_your_team = popular_bets_based_on_your_team.count_of_items
        self.assertEqual(count_on_fe_your_team, self.count_of_items_based_on_your_team,msg=f"Count of items on front end is {count_on_fe_your_team} expected from cms" f"{self.count_of_items_based_on_your_team}")

        popular_bets_based_on_other_fans = self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.other_team_module_name)
        self.assertTrue(popular_bets_based_on_other_fans, msg='"popular_bets_based_on_other_fans" module is not present ')
        count_items_on_fe = popular_bets_based_on_other_fans.count_of_items
        self.assertEqual(count_items_on_fe, self.count_of_items_based_on_other_team,
                         msg=f"Count of items on front end is {count_items_on_fe} expected from cms"
                             f"{self.count_of_items_based_on_other_team}")

        # verifying GA Tracking after bet placement covering  test case C66044316
        self.site.fanzone.tab_content.popular_bets.items_as_ordered_dict.get(self.your_team_module_name).items_as_ordered_dict_inc_dup[0].odd.click()
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.close()
            self.site.open_betslip()
        self.place_single_bet()
        response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent').get('ecommerce').get('purchase').get('products')[0]
        Actual_dimension64 = response.get('dimension64')
        Actual_dimension65 = response.get('dimension65')
        expected_response = {'event': "trackEvent",
                             'eventCategory': 'betslip',
                             'dimension64': 'Fanzone',
                             'dimension65': 'ADA Recommended bets carousel',
                             'category': "16",
                             }
        # Compare dimension64 and dimension65 values with expected_response
        self.assertEqual(Actual_dimension64, expected_response['dimension64'],
                         msg=f"Actual dimension64: {Actual_dimension64} does not match expected dimension64: {expected_response['dimension64']}")
        self.assertEqual(Actual_dimension65, expected_response['dimension65'],
                         msg=f"Actual dimension65: {Actual_dimension65} does not match expected dimension65: {expected_response['dimension65']}")

        # Not automable :the Fanzone team(If user is Arsenal fan change to some other fan) and Verify the fan selections in both the modules. because we need to wait another 1 days to change the team

    def test_007_verify_the_module_name_field_in_bets_based_on_your_team_module(self):
        """
        DESCRIPTION: Verify the Module Name field in Bets based on your team module
        EXPECTED: Module Name should accept only with 50 Characters. Throws error msg after 50 chars
        """
        # CMS front end validation not automate

    def test_008_verify_the_module_type_field(self):
        """
        DESCRIPTION: Verify the Module Type field
        EXPECTED: Module Type fiels should be greyed out, non-editable field, default to bet based on your team (Feed from SIA model/ADA Team)
        """
        # Not automate

    def test_009_verify_the_max_no_of_selections(self):
        """
        DESCRIPTION: Verify the Max no of selections
        EXPECTED: User can give the number of tiles/cards should be displayed in front end application
        """
        # Covered in above step

    def test_010_click_on_save_changes(self):
        """
        DESCRIPTION: Click on Save changes
        EXPECTED: Changes should be saved and reflected in FE
        """
        # Covered in above step

    def test_011_verify_the_display_order_of_fanzone_modules_in_fanzone_page(self):
        """
        DESCRIPTION: Verify the display order of fanzone modules in fanzone page
        EXPECTED: First the surface bet modules should display and next highlight carousel should display and next Bets based on your team module and followed by Bets based on other fans module
        """
        # Not automated

    def test_012_repeat_the_above_same_steps_for_bets_based_on_other_fans_module(self):
        """
        DESCRIPTION: Repeat the above same steps for "Bets based on other fans" module
        EXPECTED: All changes made should be saved and reflected in FE
        """
        # Covered in above steps

    def test_013_navigate_to_the_fanzone_in_the_sports_categories__ampgt_fanzone__ampgt_fanzones__ampgt_fanzone_configurations(self):
        """
        DESCRIPTION: Navigate to the Fanzone in the Sports Categories -&amp;gt; Fanzone -&amp;gt; Fanzones -&amp;gt; Fanzone Configurations
        EXPECTED: Able to navigate to the Fanzone page
        """
        # Covered in above steps

    def test_014_verify_the_toggle_displaying_for_show_bets_based_on_your_team_and_show_bets_based_on_other_fanzone_team_modules(self):
        """
        DESCRIPTION: Verify the Toggle displaying for Show Bets Based On Your Team and Show bets based on other Fanzone team modules
        EXPECTED: Able to see the Toggle for Show Bets Based On Your Team and Show bets based on other Fanzone team modules
        """
        # Covered in above steps

    def test_015_onoff_the_toggle_and_verify(self):
        """
        DESCRIPTION: ON/OFF the Toggle and verify
        EXPECTED: Able to Turn on/off the Toggle successfully
        """
        # Covered in above steps

    def test_016_click_on_save_changes_and_verify(self):
        """
        DESCRIPTION: Click on Save Changes and Verify
        EXPECTED: Able to save the changes and changes should be reflected in FE
        """
        # Covered in above steps

