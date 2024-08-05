import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't grant odds boost tokens on prod
# @pytest.mark.hl - Can't grant odds boost tokens on prod
@pytest.mark.betslip
@pytest.mark.odds_boost
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.slow  # ladbrokes
@pytest.mark.login
@vtest
class Test_C2594362_Verify_displaying_odds_boost_button_in_the_betslip_Single_selection_for_logged_in_user(BaseBetSlipTest, BaseSportTest, BaseUserAccountTest):
    """
    TR_ID: C2594362
    NAME: Verify displaying odds boost button in the betslip (Single selection) for logged in user
    DESCRIPTION: This test case verifies that Odds Boost button displaying in the Betslip with Single selection for logged in user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Fractional odds format selected for User1
    PRECONDITIONS: Add a single selection with added Stake to the Betslip
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True
    odds_boost_header = None
    bet_amount = 3
    initial_home_team_stake_est_returns = None
    initial_away_team_stake_est_returns = None
    initial_total_est_returns = None
    info_pop_up_title = vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP.replace("lad", "")

    def verify_odds_boost_remains_boosted(self):
        """
        This method verifies following points:
        - 'BOOSTED' button is shown
        - Boosted odds (fractional) is shown
        - Original odds (fractional) is displayed as crossed out
        - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown
        """
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.enabled}" button is not displayed')
        self.assertEqual(odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg='Button text label "%s" is not the same as expected "%s"' %
                             (odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled))

        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.home_team, singles_section, msg=f'"{self.home_team}" stake is not available')
        stake = singles_section[self.home_team]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.check_odds_format(odds=stake.boosted_odds_container.price_value)

        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

        boosted_home_team_stake_est_returns = stake.est_returns
        self.assertNotEqual(boosted_home_team_stake_est_returns, self.initial_home_team_stake_est_returns,
                            msg='Boosted Est. Returns value "%s" is the same as initial value "%s"' %
                                (boosted_home_team_stake_est_returns, self.initial_home_team_stake_est_returns))
        boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg='Boosted Total Est. Returns value "%s" is the same as initial value "%s"' %
                                (boosted_total_est_returns, self.initial_total_est_returns))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Log in as a user from preconditions
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.home_team, self.__class__.home_team_selection_id = list(selection_ids.items())[0]
        self.__class__.away_team, self.__class__.away_team_selection_id = list(selection_ids.items())[2]
        self.__class__.username = tests.settings.odds_boost_user
        self.site.login(username=self.username)
        self.__class__.offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=self.username, id=self.home_team_selection_id, level='selection', offer_id=self.offer_id)

    def test_001_navigate_to_betslip_verify_that_odds_boost_button_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Odds Boost button is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' button with hint text: 'Hint Boost to increase the odds of the bets in your betslip! You can boost up to 50.00 total stake'
        EXPECTED: - Potential returns/ total potential returns
        """
        self.open_betslip_with_selections(selection_ids=self.home_team_selection_id)
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg='Button text "%s" is not the same as expected "%s"' %
                             (self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))

        label_text = self.odds_boost_header.tap_to_boost_your_betslip_label.text
        self.assertEqual(label_text, vec.odds_boost.BETSLIP_HEADER.subtitle,
                         msg=f'"{label_text}" does not equal expected text "{vec.odds_boost.BETSLIP_HEADER.subtitle}"')

        self.assertTrue(self.odds_boost_header.info_button.is_displayed(), msg='"i" button is not displayed')
        self.odds_boost_header.info_button.click()
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertTrue(info_popup, msg='Information pop-up is not shown')
        self.assertEqual(info_popup.name, self.info_pop_up_title,
                         msg=f'"{info_popup.name}" is not the same as expected "{self.info_pop_up_title}"')
        self.assertEqual(info_popup.description.replace('\n', ' '), vec.odds_boost.INFO_DIALOG.text,
                         msg='Hint text \n"%s" is not the same as expected \n"%s"' %
                             (info_popup.description, vec.odds_boost.INFO_DIALOG.text))
        info_popup.click_ok()
        self.assertFalse(self.site.wait_for_dialog(self.info_pop_up_title, timeout=10),
                         msg='Information pop-up is not closed')
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.home_team, singles_section,
                      msg=f'"{self.home_team}" stake is not available')
        stake = singles_section[self.home_team]
        self.enter_stake_amount(stake=(stake.name, stake))
        self.__class__.initial_home_team_stake_est_returns = stake.est_returns
        self.assertTrue(self.initial_home_team_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{self.home_team}" stake')
        self.__class__.initial_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertTrue(self.initial_total_est_returns, msg='Total Est. Returns is not shown')

    def test_002_tap_boost_button_verify_that_odds_are_boosted_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted and odds boost button is displaying with animation
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        self.odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header

        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        if not self.brand == 'ladbrokes':
            self.assertTrue(odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('enabled', odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')

        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.home_team, singles_section, msg=f'"{self.home_team}" stake is not available')
        stake = singles_section[self.home_team]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.check_odds_format(odds=stake.boosted_odds_container.price_value)

        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

        boosted_home_team_stake_est_returns = stake.est_returns
        self.assertNotEqual(boosted_home_team_stake_est_returns, self.initial_home_team_stake_est_returns,
                            msg='Boosted Est. Returns value "%s" is the same as initial value "%s"' %
                                (boosted_home_team_stake_est_returns, self.initial_home_team_stake_est_returns))
        boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg='Boosted Total Est. Returns value "%s" is the same as initial value "%s"' %
                                (boosted_total_est_returns, self.initial_total_est_returns))

    def test_003_refresh_page_verify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Refresh page
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - "BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_betslip()

        self.verify_odds_boost_remains_boosted()

    def test_004_navigate_to_any_other_page_reopen_betslip_verify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - "BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

        self.site.open_betslip()
        self.verify_odds_boost_remains_boosted()

    def test_005_add_one_more_selection_with_odds_boost_available_navigate_to_betslip_verify_that_odds_boost_remains_boosted_and_new_selection_displaying_boosted(
            self):
        """
        DESCRIPTION: Add one more selection with Odds Boost available
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost remains boosted and new selection displaying boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown
        """
        self.open_betslip_with_selections(selection_ids=self.away_team_selection_id)

        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.enabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg='Button text label "%s" is not the same as expected "%s"' %
                             (self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled))

        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[1]
        self.enter_stake_amount(stake=stake)

        self.__class__.home_team_stake = singles_section[self.home_team]
        self.__class__.away_team_stake = singles_section[self.away_team]
        for bet in [self.home_team, self.away_team]:
            self.assertIn(bet, singles_section, msg=f'"{bet}" bet is not available')
            stake = singles_section[bet]
            self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
            self.check_odds_format(odds=stake.boosted_odds_container.price_value)

            self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

        self.__class__.initial_away_team_stake_est_returns = self.away_team_stake.est_returns
        self.assertTrue(self.initial_away_team_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{self.away_team}" stake')

        boosted_home_team_stake_est_returns = self.home_team_stake.est_returns
        self.assertNotEqual(boosted_home_team_stake_est_returns, self.initial_home_team_stake_est_returns,
                            msg='Boosted Est. Returns value "%s" is the same as initial value "%s"' %
                                (boosted_home_team_stake_est_returns, self.initial_home_team_stake_est_returns))

        self.__class__.final_boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(self.final_boosted_total_est_returns, self.initial_total_est_returns,
                            msg='Boosted Total Est. Returns value "%s" is the same as initial value "%s"' %
                                (self.final_boosted_total_est_returns, self.initial_total_est_returns))

    def test_006_tap_boosted_button_verify_that_odds_boost_are_removed_and_odds_boost_button_is_displaying_with_animation(
            self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost are removed and odds boost button is displaying with animation
        EXPECTED: - 'BOOSTED' button is changed back to 'BOOST' button with animation
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Potential returns/ total potential returns are updated back
        """
        self.odds_boost_header.boost_button.click()

        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
            name='"BOOSTED" button to become "BOOST" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')
        if not self.brand == 'ladbrokes':
            self.assertTrue(self.odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('disabled', self.odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boost reverting')

        for stake in [self.home_team_stake, self.away_team_stake]:
            self.assertFalse(stake.has_boosted_odds, msg=f'"{stake.name}" should not have boosted odds')

        home_team_stake_est_returns = self.home_team_stake.est_returns
        self.assertEqual(home_team_stake_est_returns, self.initial_home_team_stake_est_returns,
                         msg='Est. Returns value "%s" is not the same as initial value "%s"' %
                             (home_team_stake_est_returns, self.initial_home_team_stake_est_returns))

        away_team_stake_est_returns = self.away_team_stake.est_returns
        self.assertNotEqual(away_team_stake_est_returns, self.initial_away_team_stake_est_returns,
                            msg='Est. Returns value "%s" is the same as initial value "%s"' %
                                (away_team_stake_est_returns, self.initial_away_team_stake_est_returns))

        total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(total_est_returns, self.final_boosted_total_est_returns,
                            msg='Total Est. Returns value "%s" is the same as value with boosted odds "%s"' %
                                (total_est_returns, self.final_boosted_total_est_returns))

    def test_007_navigate_to_any_other_page_reopen_betslip_verify_that_odds_boost_remains_unboosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains Unboosted
        EXPECTED: Odds boost 'Off' status is remembered:
        EXPECTED: - 'BOOST' button is shown
        EXPECTED: - Original odds is shown
        EXPECTED: - Original potential returns/ total potential returns is shown
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name='tennis')

        self.site.open_betslip()

        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg='Button text label "%s" is not the same as expected "%s"' %
                             (odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))

        singles_section = self.get_betslip_sections().Singles
        self.__class__.home_team_stake = singles_section[self.home_team]
        self.__class__.away_team_stake = singles_section[self.away_team]

        home_team_stake_est_returns = self.home_team_stake.est_returns
        self.assertEqual(home_team_stake_est_returns, self.initial_home_team_stake_est_returns,
                         msg='Est. Returns value "%s" is not the same as initial value "%s"' %
                             (home_team_stake_est_returns, self.initial_home_team_stake_est_returns))

        away_team_stake_est_returns = self.away_team_stake.est_returns
        self.assertNotEqual(away_team_stake_est_returns, self.initial_away_team_stake_est_returns,
                            msg='Est. Returns value "%s" is the same as initial value with boosted odds "%s"' %
                                (away_team_stake_est_returns, self.initial_away_team_stake_est_returns))

        total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(total_est_returns, self.final_boosted_total_est_returns,
                            msg='Total Est. Returns value "%s" is the same as value with boosted odds "%s"' %
                                (total_est_returns, self.final_boosted_total_est_returns))

    def test_008_change_odd_format_to_decimal_verify_that_this_functionality_works_the_same_with_decimal_odds(self):
        """
        DESCRIPTION: Change odd format to Decimal
        DESCRIPTION: Verify that this functionality works the same with decimal odds
        EXPECTED: - Boosted odds is shown in decimal
        EXPECTED: - Original odds is displayed as crossed out in decimal
        """
        self.site.close_betslip()
        is_format_changed = self.site.change_odds_format(odds_format='DECIMAL')
        self.assertTrue(is_format_changed, msg='Odds format is not changed to Decimal')
        self.site.go_to_home_page()
        self.site.open_betslip()
        self.get_betslip_content().odds_boost_header.boost_button.click()

        singles_section = self.get_betslip_sections().Singles
        for bet in [self.home_team, self.away_team]:
            self.assertIn(bet, singles_section, msg=f'"{bet}" bet is not available')
            stake = singles_section[bet]
            self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
            self.check_odds_format(odds=stake.boosted_odds_container.price_value, expected_odds_format='decimal')
            self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')
