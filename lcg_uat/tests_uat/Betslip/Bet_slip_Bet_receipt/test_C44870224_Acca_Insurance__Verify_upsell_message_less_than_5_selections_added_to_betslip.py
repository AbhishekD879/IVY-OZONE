import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - This test case is limited to QA2 only as we cannot create offers in prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.acca
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870224_Acca_Insurance__Verify_upsell_message_less_than_5_selections_added_to_betslip(BaseBetSlipTest):
    """
    TR_ID: C44870224
    NAME: Acca Insurance - Verify upsell message less than 5 selections added to betslip
    PRECONDITIONS: Football only.
    PRECONDITIONS: W-D-W only
    PRECONDITIONS: 5+ selections minimum.
    PRECONDITIONS: Valid on only 1st acca placed during the day.
    PRECONDITIONS: Minimum selection price 1/10.
    PRECONDITIONS: Minimum acca price 3/1.
    PRECONDITIONS: Up to Â£10 returned if 1 selection lets you down as a free bet
    PRECONDITIONS: - User should login
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '3/1'),
                          ('odds_draw', '1/17'),
                          ('odds_away', '1/4')])
    currency = '£'
    selections_id = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Football only.
        DESCRIPTION: W-D-W only
        DESCRIPTION: 5+ selections minimum.
        DESCRIPTION: Valid on only 1st acca placed during the day..
        DESCRIPTION: Minimum selection price 1/10.
        DESCRIPTION: Minimum acca price 3/1.
        DESCRIPTION: Up to Â£10 returned if 1 selection lets you down as a free bet
        """
        for i in range(4):
            selection_ids = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, default_market_name='|Draw No Bet|').selection_ids
            self.selections_id.append(list(selection_ids.values())[0])

    def test_001_launch_the_site_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the site and login with valid credentials.
        EXPECTED: User is logged in
        """
        self.site.register_new_user()
        self.site.wait_content_state("HomePage")

    def test_002_add_less_than_5_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add less than 5 selections to bet slip
        EXPECTED: Selections is added to bet slip
        """
        self.open_betslip_with_selections(selection_ids=self.selections_id)

    def test_003_go_to_bet_slip_page(self):
        """
        DESCRIPTION: Go to bet slip page
        EXPECTED: User should see prompt
        EXPECTED: to'Add 1 more selection to qualify for 5+ acca insurance' .
        """
        multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(vec.betslip.ACC4 in multi_section, msg=f'No "{vec.betslip.ACC4}" found')
        stake = multi_section[vec.betslip.ACC4]
        stake.scroll_to()
        self.assertTrue(stake.has_acca_insurance_offer(),
                        msg=f'"{vec.betslip.ACC4}" stake does not have '
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
