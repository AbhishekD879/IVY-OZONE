import pytest
import tests
import voltron.environments.constants as vec
import datetime
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.lad_tst2
@pytest.mark.lad_uat    # signposting functionality is not applicable for coral
@pytest.mark.desktop
# @pytest.mark.prod - It doesnt applicable for prod as settlement of selection is not done in prod
@pytest.mark.medium
@pytest.mark.acca
@pytest.mark.slow
@pytest.mark.sports
@pytest.mark.betslip
@vtest
class Test_C44870359_Verify_user_sees_Acca_Insurance_signposting_on_five_fold_Acca_bet(BaseCashOutTest):
    """
    TR_ID: C44870359
    NAME: Verify user sees Acca Insurance signposting on five fold Acca bet
    DESCRIPTION: "Verify user sees Acca Insurance signposting only when placed five fold Acca bet. Verify user sees signposting on Open Bets and Settled Bets"
    PRECONDITIONS: UserName: goldenbuild1  Password: password1
    PRECONDITIONS: To qualify for Acca Insurance, place a cash bet on football, in any of the following markets:
    PRECONDITIONS: Match Betting
    PRECONDITIONS: Both Teams To Score
    PRECONDITIONS: Match Result & Both Teams to Score
    PRECONDITIONS: Correct Score
    PRECONDITIONS: Total Goals Over/Under markets
    PRECONDITIONS: Condition:1. cumulative odds of 3/1, and 2. individual odds of 1/10 or greater, with five selections or more it can qualify.
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '3/1'),
                          ('odds_draw', '1/17'),
                          ('odds_away', '1/4')])
    suspension_status = False
    selection_status = False
    betslip_selection_status = False
    deposit_amount = 20.00

    def registering_for_acca_user(self):
        self.site.wait_content_state('Homepage')
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        username = self.gvc_wallet_user_client.register_new_user().username
        status = self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount,
                                                                          card_number=tests.settings.visa_card,
                                                                          card_type='visa',
                                                                          expiry_month=f'{now.month:02d}',
                                                                          expiry_year=shifted_year,
                                                                          cvv=tests.settings.visa_card_cvv)
        self.assertTrue(status, msg='The card is not added successfully')
        self.site.login(username)
        self.site.wait_content_state("HomePage")

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case verifies that ACCA Insurance signposting is displayed for bets which qualify for ACCA insurance.
        PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
        PRECONDITIONS: 2. Configure ACCA offer using the following instruction: https://confluence.egalacoral.com/display/SPI/How+to+setup+ACCA+offers
        RECONDITIONS:  3. create test events
        PRECONDITIONS: 4. Login into App
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ems_status=True)
        if not self.cms_config.get_system_configuration_structure()['Betslip']['superAcca']:
            self.cms_config.set_super_acca_toggle_component_status(super_acca_component_status=True)
        event_params1 = self.create_several_autotest_premier_league_football_events(number_of_events=4,
                                                                                    is_upcoming=True, lp=self.prices)
        event2 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('match_result_and_both_teams_to_score', {'cashout': True})], is_upcoming=True, lp=self.prices)
        event3 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('both_teams_to_score', {'cashout': True})], is_upcoming=True, lp=self.prices)
        event4 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('over_under_total_goals', {'cashout': True})], is_upcoming=True, lp=self.prices)
        event5 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('correct_score', {'cashout': True})], is_upcoming=True, lp=self.prices)
        event6 = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, lp=self.prices)
        event7 = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, lp=self.prices)

        self.__class__.selection_ids1 = [list(event.selection_ids.values())[0] for event in event_params1]
        self.__class__.selection_ids2 = list(event2.selection_ids['match_result_and_both_teams_to_score'].values())[0]
        self.__class__.selection_ids3 = list(event3.selection_ids['both_teams_to_score'].values())[0]
        self.__class__.selection_ids4 = list(event4.selection_ids['over_under_total_goals'].values())[0]
        self.__class__.selection_ids5 = list(event5.selection_ids['correct_score'].values())[0]
        self.__class__.event_id6 = event6.event_id
        self.__class__.market_id6 = event6.default_market_id
        self.__class__.selection_ids6 = list(event6.selection_ids.values())[0]
        self.__class__.event_id7 = event7.event_id
        self.__class__.market_id7 = event6.default_market_id
        self.__class__.selection_ids7 = list(event7.selection_ids.values())[0]

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        self.registering_for_acca_user()
        self.assertTrue(self.site.wait_content_state('HOMEPAGE', timeout=5), msg='User is not navigated to homepage')

    def test_002_add_four_selection_from_football_match_betting_market_to_betslip_and_verify_upsell_message(self):
        """
        DESCRIPTION: Add four selection from Football, Match betting market to betslip and verify upsell message
        EXPECTED: 'Add one more selection to qualify Acca Insurance' Message is displayed in betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        if not self.betslip_selection_status:
            self.open_betslip_with_selections(selection_ids=[self.selection_ids1[0], self.selection_ids1[1],
                                                             self.selection_ids1[2], self.selection_ids1[3]])
            self.__class__.betslip_selection_status = True
        else:
            self.site.wait_content_state_changed()
            self.open_betslip_with_selections(selection_ids=[self.selection_ids2, self.selection_ids3,
                                                             self.selection_ids4, self.selection_ids5])
        multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(vec.betslip.ACC4 in multi_section, msg=f'No "{vec.betslip.ACC4}" found')
        stake = multi_section[vec.betslip.ACC4]
        stake.scroll_to()
        self.assertTrue(stake.has_acca_insurance_offer(), msg=f'"{vec.betslip.ACC4}" stake does not have '
                                                              f'Multiples "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_4_PLUS}" offer')

    def test_003_add_one_more_selection_and_verify_acca_insurance_icon_on_five_fold_accumulator(self):
        """
        DESCRIPTION: Add one more selection and verify Acca Insurance icon on Five fold accumulator
        EXPECTED: '5+ Acca' icon is displayed in betslip
        """
        if not self.selection_status:
            self.open_betslip_with_selections(selection_ids=self.selection_ids6)
            self.__class__.selection_status = True
        else:
            self.open_betslip_with_selections(selection_ids=self.selection_ids7)
        multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(vec.betslip.ACC5 in multi_section, msg=f'No "{vec.betslip.ACC5}" found')
        stake = multi_section[vec.betslip.ACC5]
        stake.scroll_to()
        self.assertTrue(stake.has_acca_insurance_icon(), msg='"5+" acca signposting is not shown')
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_004_verify_acca_insurance_icon_in_bet_receipt(self):
        """
        DESCRIPTION: Verify Acca Insurance icon in Bet receipt
        EXPECTED: '5+ Acca' icon is displayed in bet receipt
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        first_section = list(betreceipt_sections.values())[0]
        self.assertTrue(first_section)
        self.assertTrue(first_section.has_acca_sign_post(),
                        msg='"5+ Acca Insurance" Sign post is not present on betreceipt')
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state_changed()

    def test_005_verify_acca_insurance_icon_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Verify Acca Insurance icon in My bets open bets
        EXPECTED: '5+ Acca' icon is displayed in My bets Open bets
        """
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_page('open-bets')
        self.site.close_all_dialogs()
        self.site.wait_content_state('open-bets')
        open_bets = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(open_bets, msg='No bets found in open bet')
        self.assertTrue(open_bets.has_acca_insurance_icon(), msg='"5+" Acca issurance signpost icon is not shown')
        if not self.suspension_status:
            self.ob_config.update_selection_result(event_id=self.event_id6, market_id=self.market_id6,
                                                   selection_id=self.selection_ids6, result='L')
            self.__class__.suspension_status = True
        else:
            self.ob_config.update_selection_result(event_id=self.event_id7, market_id=self.market_id7,
                                                   selection_id=self.selection_ids7, result='L')
        self.device.refresh_page()

    def test_006_verify_acca_insurance_icon_in_my_bets_settle_bets(self):
        """
        DESCRIPTION: Verify Acca Insurance icon in My bets Settle bets
        EXPECTED: '5+ Acca' icon is displayed in My bets > settle bets
        """
        self.site.wait_content_state_changed()
        if self.device_type == 'mobile':
            self.site.open_my_bets_settled_bets()
        else:
            self.navigate_to_page('bet-history')
            self.site.wait_content_state('bet-history')
        self.site.close_all_dialogs()
        self.device.refresh_page()
        self.device.refresh_page()
        settled_bets = list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(settled_bets, msg='No bets found in open bet')
        self.site.wait_content_state_changed(timeout=10)
        self.assertTrue(settled_bets.has_acca_insurance_icon(timeout=10),
                        msg='"5+" Acca insurance signpost is not shown')

    def test_007_repeat_step_2_to_6_for_different_or_combination_of_below_football_marketsboth_teams_to_scorematch_result__both_teams_to_scorecorrect_scoretotal_goals_overunder_markets(self):
        """
        DESCRIPTION: Repeat step #2 to #6 for different or combination of below football markets
        DESCRIPTION: Both Teams To Score
        DESCRIPTION: Match Result & Both Teams to Score
        DESCRIPTION: Correct Score
        DESCRIPTION: Total Goals Over/Under markets
        """
        self.test_002_add_four_selection_from_football_match_betting_market_to_betslip_and_verify_upsell_message()
        self.test_003_add_one_more_selection_and_verify_acca_insurance_icon_on_five_fold_accumulator()
        self.test_004_verify_acca_insurance_icon_in_bet_receipt()
        self.test_005_verify_acca_insurance_icon_in_my_bets_open_bets()
        self.test_006_verify_acca_insurance_icon_in_my_bets_settle_bets()
