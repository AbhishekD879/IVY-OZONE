import pytest
import tests
import voltron.environments.constants as vec
from faker import Faker
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.promotions
@pytest.mark.login
@vtest
class Test_C16268968_Vanilla_Accessing_Log_In_popup_in_Quick_Bet_Betslip_view_BYB_tab(BaseBetSlipTest, BaseBanachTest):
    """
    TR_ID: C16268968
    NAME: [Vanilla] Accessing Log In popup in Quick Bet, Betslip view, BYB tab
    DESCRIPTION: This test case verifies accessing Log In popup from different places of the application
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Home page (with Vanilla) is opened
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True
    fake_name = Faker()
    button_name = 'Unique Opt In' + fake_name.city()

    def verification_login_dialog(self, login=False):
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        if login:
            dialog.username = tests.settings.default_username
            dialog.password = tests.settings.default_password
            dialog.click_login()
            dialog_closed = dialog.wait_dialog_closed(timeout=20)
            self.assertTrue(dialog_closed, msg='Login dialog was not closed')
            try:
                self.site.close_all_dialogs(async_close=False)
            except Exception as e:
                self._logger.warning(e)
            self.site.wait_content_state('EventDetails')
            self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
        else:
            dialog.close_dialog()
            dialog_closed = dialog.wait_dialog_closed(timeout=20)
            self.assertTrue(dialog_closed, msg='Login dialog was not closed')

    def test_000_preconditions(self):
        """
        Event creation
        """
        self.__class__.proxy = None
        self.__class__.byb_eventID = self.get_ob_event_with_byb_market()

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            market_name = next((market['market']['name'] for market in event['event']['children']
                                if market.get('market').get('templateMarketName') == 'Match Betting'), None)
            self._logger.info(f'*** Found football event with event id "{self.eventID}"')
            outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('No outcomes available')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self._logger.info(
                f'*** Found Football event with id "{self.eventID}" with selection ids: "{self.selection_ids}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_ids = event_params.selection_ids
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|',
                                                                                                                    '')

            # Creation of Promotions
            opt_in_messagging_config = self.get_initial_data_system_configuration().get('OptInMessagging', {})
            if not opt_in_messagging_config:
                opt_in_messagging_config = self.cms_config.get_system_configuration_item('OptInMessagging')
            successful_opt_in_text = opt_in_messagging_config.get('successMessage')
            already_opt_in_text = opt_in_messagging_config.get('alreadyOptedInMessage')
            if not successful_opt_in_text or not already_opt_in_text:
                raise CmsClientException('Opt-in messages not configured in CMS')
            opt_in_promo_request_id = self.ob_config.backend.ob.opt_in_offer.default_offer.id
            promotion = self.cms_config.add_promotion(requestId=opt_in_promo_request_id,
                                                      promo_description=[{'button_name': f'{self.button_name}',
                                                                          'button_link': '',
                                                                          'is_it_opt_in_button': True}])
            self.__class__.promotion_title, self.__class__.promo_key = \
                promotion.title.upper(), promotion.key

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_selection_from_football_to_quick_betadd_a_stake_to_selectiontap_loginplace_bet_button(self):
        """
        DESCRIPTION: Add selection from Football to Quick Bet
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Tap 'Login&Place Bet' button
        EXPECTED: Log in pop-up appears
        """
        self.site.wait_content_state('homepage')
        self.assertTrue(self.site.wait_logged_out(), "User is not logged out")
        self.navigate_to_edp(event_id=self.eventID)
        if self.brand == 'mobile':
            self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
            self.site.wait_for_quick_bet_panel(timeout=10)
            self.site.quick_bet_panel.selection.content.amount_form.input.value = 0.03
            self.site.quick_bet_panel.place_bet.click()
        else:
            self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_002_close_log_in_pop_uptap_add_to_betslip_button(self):
        """
        DESCRIPTION: Close Log in pop-up
        DESCRIPTION: Tap 'Add to betslip' button
        EXPECTED: One selection is added to Betslip
        """
        if self.brand == 'mobile':
            self.verification_login_dialog()
            self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                            msg='Add to betslip button is not disabled')
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.open_betslip()

    def test_003_tap_betslip_iconadd_a_stake_to_selectiontap_loginplace_bet_button(self):
        """
        DESCRIPTION: Tap Betslip icon
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Tap 'Login&Place Bet' button
        EXPECTED: Log in pop-up appears
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)
        betnow_btn = self.get_betslip_content().bet_now_button
        betnow_btn.click()
        self.verification_login_dialog()

    def test_004_close_log_in_pop_upnavigate_to_promotion_with_opt_in_button(self):
        """
        DESCRIPTION: Close Log in pop-up
        DESCRIPTION: Navigate to Promotion with Opt In button
        EXPECTED: Opt In button is enabled
        """
        if tests.settings.backend_env != 'prod':
            self.navigate_to_page('promotions')
            self.site.wait_content_state(state_name='Promotions')
            promotions = self.site.promotions.tab_content.items_as_ordered_dict
            self.assertTrue(self.promotion_title in list(promotions.keys()),
                            msg=f'Test promotion: "{self.promotion_title}" was not found in "{list(promotions.keys())}"')
            self.navigate_to_promotion(promo_key=self.promo_key)
            opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
            self.assertTrue(opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')
            self.assertEqual(opt_in_button.name, self.button_name,
                             msg=f'Actual button name: "{opt_in_button.name}"'
                                 f'is not equal to expected: "{self.button_name}"')
            opt_in_button.click()

    def test_005_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on Opt In button
        EXPECTED: Log in pop-up appears
        """
        if tests.settings.backend_env != 'prod':
            self.verification_login_dialog()

    def test_006_close_log_in_pop_uptap_on_the_build_your_bet_tabadd_at_least_two_selectionstap_place_bet_button_in_the_right_bottom_corner(
            self):
        """
        DESCRIPTION: Close Log in pop-up
        DESCRIPTION: Tap on the 'Build Your Bet' tab
        DESCRIPTION: Add at least two selections
        DESCRIPTION: Tap Place Bet button in the right bottom corner
        EXPECTED: Log in pop-up appears
        """
        self.navigate_to_edp(event_id=self.byb_eventID)
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')

        match_betting_selection_names = match_betting.set_market_selection(count=1)
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)

        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(count=1)
        both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary

        odds = summary_block.place_bet.value
        self.assertTrue(odds, msg='Can not get odds for given selections')

        summary_block.place_bet.scroll_to()
        summary_block.place_bet.click()

    def test_007_enter_valid_username_and_password_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid username and password. Tap Log in button
        EXPECTED: User is logged in and stays at the same page
        """
        self.verification_login_dialog(login=True)
