import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - only applicable for QA2 as we need a ACCA insurance offer to be active
@pytest.mark.uat
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870228_Acca_Insurance__Verify_upsell_messaging_with_different_parameters(BaseCashOutTest):
    """
    TR_ID: C44870228
    NAME: Acca Insurance - Verify upsell messaging with different parameters
    PRECONDITIONS: Football only.
    PRECONDITIONS: Preplay only.
    PRECONDITIONS: W-D-W only
    PRECONDITIONS: 5+ selections minimum.
    PRECONDITIONS: Valid on only 1st acca placed during the day.
    PRECONDITIONS: Minimum selection price 1/10.
    PRECONDITIONS: Minimum acca price 3/1.
    PRECONDITIONS: Up to Â£10 returned if 1 selection lets you down as a free bet
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '3/1'),
                          ('odds_draw', '1/17'),
                          ('odds_away', '1/4')])

    def test_001_user_launches_the_siteapp_and_logs_in(self):
        """
        DESCRIPTION: User launches the site/app and logs in
        EXPECTED: User can able to place a bet as logged in customers
        """
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=4)
        self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.register_new_user()
        self.site.wait_content_state("HomePage")

    def test_002_user_adds_4_selections_in_the_bet_slip(self):
        """
        DESCRIPTION: User adds 4 selections in the bet slip
        EXPECTED: User has added 4 selections in the bet slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_counter_before = self.get_betslip_content().selections_count

    def test_003_user_adds_a_fifth_selection_to_the_bet_slip_from_any_other_parametereg__take_horse_race(self):
        """
        DESCRIPTION: User adds a fifth selection to the bet slip from Any other parameter(Eg : Take Horse race)
        EXPECTED: A new selection has been selected and added to bet slip
        """
        selection_ids_5 = self.ob_config.add_autotest_cricket_event(lp=self.prices).selection_ids
        selection_id_5 = (list(selection_ids_5.values())[0])
        self.open_betslip_with_selections(selection_ids=selection_id_5)
        bet_counter_after = self.get_betslip_content().selections_count
        self.assertGreater(bet_counter_after, self.bet_counter_before,
                           msg=f'Selections count "{bet_counter_after}" is same as expected {self.bet_counter_before}')

    def test_004_check_user_is_able_to_see_the_acca_insurance_or_not(self):
        """
        DESCRIPTION: Check user is able to see the Acca Insurance or not.
        EXPECTED: User should not see the Acca Insurance acca insurance qualify message' when parameters are different which is not qualify for acca insurance
        """
        multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(vec.betslip.ACC5 in multi_section, msg=f'No "{vec.betslip.ACC5}" found')
        stake = multi_section[vec.betslip.ACC5]
        stake.scroll_to()
        self.assertFalse(stake.has_acca_insurance_offer(expected_result=False),
                         msg=f'"{vec.betslip.ACC5}" stake has  "{vec.betslip.ACCA_SUGGESTED_OFFER_FOR_5_PLUS}" offer')
