import pytest
import tests
from tests.base_test import vtest
from time import sleep
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C2988033_Verify_the_flow_after_tapping_RE_BOOST_button_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C2988033
    NAME: Verify the flow after tapping RE-BOOST button in Betslip
    DESCRIPTION: This test case verifies the flow after tapping RE-BOOST button in Betslip
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to the Betslip
    PRECONDITIONS: Add Stake and tap 'Boost' button
    PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Tap 'Re-boost' button
    """
    keep_browser_open = True
    change_price = '5/3'

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Enable Odds Boost in CMS
        PRECONDITIONS: Load Application
        PRECONDITIONS: Login into App by user with Odds boost token generated
        PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Add selection to the Betslip
        PRECONDITIONS: Add Stake and tap 'Boost' button
        PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
        PRECONDITIONS: Tap 'Re-boost' button
        """
        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.home_team_selection_id = list(selection_ids.values())[0]
        username = tests.settings.odds_boost_user
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=self.home_team_selection_id)
        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=self.home_team_selection_id)
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        self.stake = list(selections.values())[0]
        self.stake.amount_form.input.value = 1
        self.__class__.est_returns_bfr_bst = float(self.stake.est_returns)
        self.__class__.old_price = self.stake.odds
        odds_boost_header.boost_button.click()
        self.__class__.est_returns_aftr_bst = float(self.stake.est_returns)
        self.__class__.new_price = self.stake.boosted_odds_container.price_value
        self.assertNotEqual(self.old_price, self.new_price,
                            msg=f'Actual price"{self.old_price}" is same as updated price "{self.new_price}')
        self.ob_config.change_price(selection_id=self.home_team_selection_id, price=self.change_price)
        sleep(10)  # Price change is taking time to reflect on betslip
        odds_boost_header.boost_button.click()

    def test_001_verify_that_non_boosted_prices_are_updated(self):
        """
        DESCRIPTION: Verify that non-boosted prices are updated
        EXPECTED: Non-boosted prices are updated
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.home_team_selection_id,
                                                                 price=self.change_price,
                                                                 multi_update=True)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.home_team_selection_id}" is not received')

    def test_002_verify_that_the_boosted_prices_are_updated(self):
        """
        DESCRIPTION: Verify that the boosted prices are updated
        EXPECTED: The boosted prices are updated
        """
        self.assertNotEqual(self.new_price, self.old_price,
                            msg='Boosted odds is not shown for decimal odds')

    def test_003_verify_the_boost_button(self):
        """
        DESCRIPTION: Verify the 'Boost' button
        EXPECTED: - The boost button text changes to 'BOOSTED'
        EXPECTED: - The boost button remains selected
        """
        odds_boost_header_name = self.get_betslip_content().odds_boost_header.boost_button.name
        self.assertEqual(odds_boost_header_name, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg=f'"{vec.odds_boost.BOOST_BUTTON.enabled}" is not as same as "{odds_boost_header_name}"')

    def test_004_verify_that_the_returns_values_are_updated(self):
        """
        DESCRIPTION: Verify that the returns values are updated
        EXPECTED: The returns values are updated
        """
        self.assertNotEqual(self.est_returns_bfr_bst, self.est_returns_aftr_bst,
                            msg=f'Estimated returns before odd boost "{self.est_returns_bfr_bst}" '
                                f'are same after updating with odd boost "{self.est_returns_aftr_bst}"')

    def test_005_verify_that_the_header_notification_message_the_price_has_changed_and_new_boosted_odds_will_be_applied_to_your_bet_hit_re_boost_to_see_your_new_boosted_price_is_removed(self):
        """
        DESCRIPTION: Verify that the header notification message 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted price' is removed
        EXPECTED: The header notification message is removed
        """
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertFalse(info_popup, msg='Information pop-up is shown')

    def test_006_check_accept__place_bet_button(self):
        """
        DESCRIPTION: Check 'ACCEPT & PLACE BET' button
        EXPECTED: The 'ACCEPT & PLACE BET' button returns to 'PLACE BET'
        """
        place_bet_button = self.get_betslip_content().bet_now_button.name
        self.assertEqual(place_bet_button.upper(), vec.quickbet.BUTTONS.place_bet.upper(),
                         msg=f'Actual text: "{place_bet_button.upper()}" is not same as the '
                             f'Expected text: "{vec.quickbet.BUTTONS.place_bet.upper()}"')
