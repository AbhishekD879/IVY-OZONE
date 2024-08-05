import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.prod - # This test case is limited to QA2 only.For Prod users, acca offer has to be granted from OB
@pytest.mark.medium
@pytest.mark.acca
@pytest.mark.betslip
@vtest
class Test_C44870225_Acca_Insurance__Verify_upsell_message_when_5_selections_added_to_betslip(BaseCashOutTest, BaseSportTest):
    """
    TR_ID: C44870225
    NAME: Acca Insurance - Verify upsell message when 5 selections added to betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create test events
        """
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=4)
        self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.__class__.football_event = self.ob_config.add_autotest_premier_league_football_event()
        expected_market = normalize_name(
            self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)

    def test_001_user_launches_the_siteapp_and_logs_in(self):
        """
        DESCRIPTION: User launches the site/app and logs in
        EXPECTED: User is able to place a bet as logged in customer
        """
        self.site.register_new_user()
        self.site.wait_content_state("HomePage")

    def test_002_user_adds_4_selections_in_the_betslip_and_does_not_see_an_acca_insurance_qualification(self):
        """
        DESCRIPTION: User adds 4 selections in the betslip and does not see an Acca Insurance Qualification
        EXPECTED: User has added 4 selections in the betslip and does not see an Acca Insurance Qualification
        """
        if self.device_type == 'mobile':
            self.site.header.bet_slip_counter.click()
        initial_BC = len(self.get_betslip_content().betslip_sections_list)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.BC_after_4_Sel = self.get_betslip_content().selections_count
        self.assertEqual(int(initial_BC + 4), int(self.BC_after_4_Sel),
                         msg=f'Selection count "{self.BC_after_4_Sel}" is not same as "{initial_BC + 4}"')

        multi_section = self.get_betslip_sections(multiples=True).Multiples
        stake = multi_section[vec.betslip.ACC4]
        stake.scroll_to()
        self.assertTrue(stake.has_acca_insurance_offer(),
                        msg=f'"{vec.betslip.ACC4}" stake does not have '
                            f'Multiples "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_4_PLUS}" offer')
        acca_offer_text = stake.acca_insurance_offer.text
        actual_acca_offer_text = acca_offer_text.replace("£25.00", "£")
        if actual_acca_offer_text == vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS.replace("£25.00", "£"):
            self.assertNotEqual(actual_acca_offer_text, vec.betslip.ACCA_SUGGESTED_OFFER_FOR_4_PLUS,
                                msg=f'\nActual ACCA offer text "{acca_offer_text}"\nExpected ACCA '
                                    f'offer text "{ vec.betslip.ACCA_SUGGESTED_OFFER_FOR_4_PLUS}"')
        else:
            self.assertNotEqual(actual_acca_offer_text, vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS.replace("£25.00", "£"),
                                msg=f'\nActual ACCA offer text "{acca_offer_text}"\nExpected ACCA '
                                    f'offer text "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS.replace("£25.00", "£")}"')

    def test_003_user_adds_a_fifth_selection_to_the_betslip(self):
        """
        DESCRIPTION: User adds a fifth selection to the betslip
        EXPECTED: A new selection has been selected and added to betslip
        """
        self.navigate_to_edp(event_id=self.football_event.event_id)
        bet_button = self.get_selection_bet_button(market_name=self.expected_market)
        bet_button.click()
        self.site.header.bet_slip_counter.click()
        BC_after_5_sel = self.get_betslip_content().selections_count
        self.assertGreater(BC_after_5_sel, self.BC_after_4_Sel,
                           msg=f'Selections count "{BC_after_5_sel}" is same as expected {self.BC_after_4_Sel}')

    def test_004_user_navigates_to_the_betslip_and_verifies_that_the_following_message_appearyour_selections_qualify_for_acca_insurance(self):
        """
        DESCRIPTION: User navigates to the betslip and verifies that the following message appear:
        DESCRIPTION: "Your selections qualify for Acca Insurance"
        EXPECTED: hen betslip is displayed to the user, the following message must be displayed:
        EXPECTED: "Your selections qualify for Acca Insurance"
        """
        multi_section = self.get_betslip_sections(multiples=True).Multiples
        stake = multi_section[vec.betslip.ACC5]
        stake.scroll_to()
        self.assertTrue(stake.has_acca_insurance_offer(),
                        msg=f'"{vec.betslip.ACC5}" stake does not have '
                            f'Multiples "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS}" offer')
        acca_offer_text = stake.acca_insurance_offer.text
        actual_acca_offer_text = acca_offer_text.replace("£25.00", "£")
        if actual_acca_offer_text == vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS.replace("£25.00", "£"):
            self.assertEqual(actual_acca_offer_text, vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS.replace("£25.00", "£"),
                             msg=f'\nActual ACCA offer text "{acca_offer_text}"\nExpected ACCA '
                                 f'offer text "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS.replace("£25.00", "£")}"')
        else:
            self.assertEqual(actual_acca_offer_text, vec.betslip.ACCA_SUGGESTED_OFFER_FOR_4_PLUS,
                             msg=f'\nActual ACCA offer text "{acca_offer_text}"\nExpected ACCA '
                                 f'offer text "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_4_PLUS}"')
