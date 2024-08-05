import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - only applicable for QA2 as we need a ACCA insurance offer to be active
@pytest.mark.uat
@pytest.mark.h1
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870227_Acca_Insurance__Verify_upsell_messaging_with_valid_and_invalid_selections(BaseCashOutTest):
    """
    TR_ID: C44870227
    NAME: Acca Insurance - Verify upsell messaging with valid and invalid selections
    PRECONDITIONS: - Football only.
    PRECONDITIONS: - W-D-W only
    PRECONDITIONS: - 5+ selections minimum.
    PRECONDITIONS: - Valid on only 1st acca placed during the day.
    PRECONDITIONS: - Minimum selection price 1/10.
    PRECONDITIONS: - Minimum acca price 3/1.
    PRECONDITIONS: - Up to Â£10 returned if 1 selection lets you down as a freebet
    """
    keep_browser_open = True
    prices_5th = OrderedDict([('odds_home', '1/12'),
                              ('odds_draw', '1/17'),
                              ('odds_away', '1/4')])
    prices_6th = OrderedDict([('odds_home', '2/1'),
                              ('odds_draw', '1/17'),
                              ('odds_away', '1/4')])

    def validate_acca_offer(self):
        self.multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(self.multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(vec.betslip.ACC5 in self.multi_section, msg=f'No "{vec.betslip.ACC5}" found')
        stake = self.multi_section[vec.betslip.ACC5]
        stake.scroll_to()
        self.assertFalse(stake.has_acca_insurance_offer(expected_result=False),
                         msg=f'"{vec.betslip.ACC5}" stake has  "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS}" offer')

    def test_001_launch_the_site_and_add_4_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Launch the site and add 4 selections to the Bet slip
        EXPECTED: 4 selections added to bet slip (User should see add 1 more selection to qualify for 5+ acca insurance prompt on bet slip)
        """
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=4)
        self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.register_new_user()
        self.site.wait_content_state("HomePage")
        self.device.driver.implicitly_wait(1)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_counter_before = self.get_betslip_content().selections_count
        self.__class__.multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(self.multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(vec.betslip.ACC4 in self.multi_section, msg=f'No "{vec.betslip.ACC4}" found')
        stake = self.multi_section[vec.betslip.ACC4]
        stake.scroll_to()
        self.assertTrue(stake.has_acca_insurance_offer(),
                        msg=f'"{vec.betslip.ACC4}" stake does not have '
                            f'Multiples "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS}" offer')

    def test_002_add_one_more_selection_with_price_is_less_than_110(self):
        """
        DESCRIPTION: Add one more selection with price is less than 1/10
        EXPECTED: Selection has been added to bet slip
        """
        selection_ids_5 = self.ob_config.add_autotest_cricket_event(lp=self.prices_5th).selection_ids
        selection_id_5 = (list(selection_ids_5.values())[0])
        self.open_betslip_with_selections(selection_ids=selection_id_5)
        bet_counter_after = self.get_betslip_content().selections_count
        self.assertGreater(bet_counter_after, self.bet_counter_before,
                           msg=f'Selections count "{bet_counter_after}" is same as expected "{self.bet_counter_before}"')

    def test_003_check_user_is_able_to_see_the_acca_insurance_or_not(self):
        """
        DESCRIPTION: Check user is able to see the Acca Insurance or not.
        EXPECTED: User should not see the "Your selections qualify for Acca Insurance" when 1 selection is less than 1/10
        """
        self.validate_acca_offer()

    def test_004_add_one_selection_with_price_less_than_31(self):
        """
        DESCRIPTION: Add one selection with price less than 3/1
        EXPECTED: Added selection with price less than 3/1
        """
        self.__class__.bet_counter_before = self.get_betslip_content().selections_count
        selection_ids_6 = self.ob_config.add_autotest_cricket_event(lp=self.prices_6th).selection_ids
        selection_id_6 = (list(selection_ids_6.values())[0])
        self.open_betslip_with_selections(selection_ids=selection_id_6)
        bet_counter_after = self.get_betslip_content().selections_count
        self.assertGreater(bet_counter_after, self.bet_counter_before,
                           msg=f'Selections count "{bet_counter_after}" is same as expected "{self.bet_counter_before}"')

    def test_005_check_user_is_able_to_see_the_acca_insurance_or_not(self):
        """
        DESCRIPTION: Check user is able to see the Acca Insurance or not.
        EXPECTED: User should not see the "Your selections qualify for Acca Insurance"  when acca price is less than 3/1
        """
        self.validate_acca_offer()
