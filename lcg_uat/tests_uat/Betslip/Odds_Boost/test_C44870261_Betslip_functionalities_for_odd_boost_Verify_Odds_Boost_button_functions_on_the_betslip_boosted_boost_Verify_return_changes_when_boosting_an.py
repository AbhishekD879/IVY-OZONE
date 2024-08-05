import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod     cannot grant odd boost offer for user in prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870261_Betslip_functionalities_for_odd_boost_Verify_Odds_Boost_button_functions_on_the_betslip_boosted_boost_Verify_return_changes_when_boosting_and_unboosting_Verify_boosting_boosted_price_appears_with_the_animation_also_shows_the_previous_price_v(BaseBetSlipTest):
    """
    TR_ID: C44870261
    NAME: "Betslip functionalities for odd boost -Verify Odds Boost button functions on the betslip (boosted/boost) -Verify return changes when boosting and unboosting -Verify boosting boosted price appears with the animation (also shows the previous price , v
    DESCRIPTION: "Betslip functionalities for odd boost
    DESCRIPTION: -Verify Odds Boost button functions on the betslip (boosted/boost)
    DESCRIPTION: -Verify return changes when boosting and unboosting
    DESCRIPTION: -Verify boosting boosted price appears with the animation (also shows the previous price , verify for decimal and fraction both)
    DESCRIPTION: -Verify Odds Boost Betslip - Info icon and tooltip ('i' icon is tappable and user sees tool tip when tapping only, verify tooltip close)"
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Odds Boost' Feature Toggle is enabled in CMS
        PRECONDITIONS: Odds Boost' item is enabled in Right menu in CMS
        PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
        PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        self.assertTrue(odds_boost, msg='Odds boost is not enabled in CMS')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.home_team_selection_id = list(selection_ids.values())[0]
        username = tests.settings.odds_boost_user
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=self.home_team_selection_id)
        self.site.login(username=username)

    def test_001_verify_odds_boost_button_functions_on_the_betslip_boostedboost(self):
        """
        DESCRIPTION: Verify Odds Boost button functions on the betslip (boosted/boost)
        EXPECTED: Odds should be boosted when user clicks on the Odds
        """
        self.open_betslip_with_selections(selection_ids=self.home_team_selection_id)
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        self.__class__.stake = list(selections.values())[0]
        self.stake.amount_form.input.value = 1
        self.__class__.est_returns_bfr_bst = float(self.stake.est_returns)
        old_price = self.stake.odds
        self.odds_boost_header.boost_button.click()
        self.__class__.est_returns_aftr_bst = float(self.stake.est_returns)
        new_price = self.stake.boosted_odds_container.price_value
        self.assertNotEqual(old_price, new_price,
                            msg=f'Actual price"{old_price}" is same as updated price "{new_price}')

    def test_002_verify_boosting_boosted_price_appears_with_the_animation_verify_for_decimal_and_fraction_both(self):
        """
        DESCRIPTION: Verify boosting boosted price appears with the animation, verify for decimal and fraction both
        EXPECTED: Boosted price appears with the animation (also shows the previous price , )
        """
        self.assertTrue(self.stake.is_original_odds_crossed,
                        msg='Original odds are not crossed out and previous price is not shown for fractional odds')
        self.assertTrue(self.stake.has_boosted_odds, msg='Boosted odds with animation is not shown for fractional odds')
        self.navigate_to_page('Homepage')
        self.site.navigate_to_right_menu_item('Settings')
        self.site.right_menu.click_item(item_name='Betting Settings')
        self.site.settings.decimal_btn.click()
        self.site.open_betslip()
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        self.__class__.stake = list(selections.values())[0]
        self.assertTrue(self.stake.is_original_odds_crossed,
                        msg='Original odds are not crossed out and previous price is not shown for decimal odds')
        self.assertTrue(self.stake.has_boosted_odds, msg='Boosted odds with animation is not shown for decimal odds')

    def test_003_verify_return_changes_when_boosting_and_unboosting(self):
        """
        DESCRIPTION: Verify return changes when boosting and unboosting
        EXPECTED: Boosted odds when unboosted should display the boost symbol
        """
        self.assertNotEqual(self.est_returns_bfr_bst, self.est_returns_aftr_bst,
                            msg=f'Estimated returns before odd boost "{self.est_returns_bfr_bst}" '
                                f'are same after updating with odd boost "{self.est_returns_aftr_bst}"')
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.odds_boost_header.boost_button.click()
        est_returns_aftr_rebst = float(self.stake.est_returns)
        self.assertNotEqual(self.est_returns_aftr_bst, est_returns_aftr_rebst,
                            msg=f'Estimated returns after odd boost "{self.est_returns_aftr_bst}" '
                                f'are same after updating with reodd boost "{est_returns_aftr_rebst}"')
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')

    def test_004_verify_odds_boost_betslip(self):
        """
        DESCRIPTION: Verify Odds Boost Betslip
        EXPECTED: Odds Boost- Info icon and tooltip ('i' icon is tappable and user sees tool tip when tapping only, verify tooltip close)"
        """
        self.assertTrue(self.odds_boost_header.info_button.is_displayed(), msg='"i" button is not displayed')
        self.odds_boost_header.info_button.click()
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertTrue(info_popup, msg='Information pop-up is not shown')
        info_pop_up_title = vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP.replace("lad", "")
        self.assertEqual(info_popup.name, info_pop_up_title,
                         msg=f'"{info_popup.name}" is not the same as expected "{info_pop_up_title}"')
        info_popup_description = info_popup.description
        self.assertEqual(info_popup_description, vec.odds_boost.INFO_DIALOG.text,
                         msg=f'Hint text "{info_popup_description}" is not the same as expected "{vec.odds_boost.INFO_DIALOG.text}"')
        info_popup.click_ok()
        self.assertTrue(info_popup.wait_dialog_closed(timeout=1), msg='Information pop-up is not closed')
