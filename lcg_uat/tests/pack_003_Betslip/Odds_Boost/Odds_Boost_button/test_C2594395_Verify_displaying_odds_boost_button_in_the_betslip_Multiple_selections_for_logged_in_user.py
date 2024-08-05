import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
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
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.slow  # slow for both for ladbrokes 11 min of run
@pytest.mark.timeout(800)
@pytest.mark.login
@vtest
class Test_C2594395_Verify_displaying_odds_boost_button_in_the_betslip_Multiple_selections_for_logged_in_user(
        BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2594395
    NAME: Verify displaying odds boost button in the betslip (Multiple selections) for logged in user
    DESCRIPTION: This test case verifies that Odds Boost button displaying in the Betslip with Multiple selection for logged in user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Fractional odds format selected for User1
    PRECONDITIONS: Load application and login with User1
    PRECONDITIONS: Add Multiple selections with added Stake to the Betslip
    PRECONDITIONS: One of the selections is with unavailable Odds Boost
    """
    keep_browser_open = True
    bet_amount = 3
    info_pop_up_title = vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP.replace("lad", "")
    odds_boost_header = None
    first_team = first_team_stake = initial_first_team_stake_est_returns = boosted_first_team_stake_est_returns = None
    second_team = second_team_stake = second_team_selection_id = boosted_second_team_stake_est_returns = None
    third_team = third_team_stake = initial_third_team_stake_est_returns = None
    first_team_original_odds = second_team_original_odds = third_team_original_odds = treble_original_odds = None
    double_stake = initial_double_stake_est_returns = None
    treble_stake = boosted_treble_stake_est_returns = None
    initial_total_est_returns = boosted_total_est_returns = None

    def verify_odds_boost_remains_boosted(self):
        """
        This method verifies following points:
        - 'BOOSTED' button is shown
        - Boosted odds (fractional) are shown for singles and for multiples section
        - Original odds (fractional) is displayed as crossed out
        - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown for singles and for multiples section section
        """
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.enabled}" button is not displayed')
        self.assertEqual(odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg=f'Button text label "{odds_boost_header.boost_button.name}" is not the same as '
                             f'expected "{vec.odds_boost.BOOST_BUTTON.enabled}"')

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        self.assertIn(self.first_team, singles_section, msg=f'"{self.first_team}" stake is not available')
        self.__class__.first_team_stake = singles_section[self.first_team]

        self.assertIn(self.third_team, singles_section, msg=f'"{self.third_team}" stake is not available')
        self.__class__.third_team_stake = singles_section[self.third_team]

        self.assertIn(vec.betslip.DBL, multiples_section,
                      msg=f'"{vec.betslip.DBL}" stake is not available')
        self.__class__.double_stake = multiples_section[vec.betslip.DBL]

        self.assertTrue(self.first_team_stake.boosted_odds_container.is_displayed(),
                        msg=f'Boosted odds are not shown for "{self.first_team}" stake')
        self.check_odds_format(odds=self.first_team_stake.boosted_odds_container.price_value)
        self.assertTrue(self.double_stake.boosted_odds_container.is_displayed(),
                        msg=f'Boosted odds are not shown for "{vec.betslip.DBL}" stake')
        self.check_odds_format(odds=self.double_stake.boosted_odds_container.price_value)

        self.assertTrue(self.first_team_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{self.first_team}" stake')
        self.assertTrue(self.double_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{vec.betslip.DBL}" stake')

        boosted_first_team_stake_est_returns = self.first_team_stake.est_returns
        self.assertNotEqual(
            boosted_first_team_stake_est_returns, self.initial_first_team_stake_est_returns,
            msg=f'"{self.first_team}" stake: boosted Est. Returns value "{boosted_first_team_stake_est_returns}" '
                f'is the same as initial value "{self.initial_first_team_stake_est_returns}"')

        boosted_double_stake_est_returns = self.double_stake.est_returns
        self.assertNotEqual(
            boosted_double_stake_est_returns, self.initial_double_stake_est_returns,
            msg=f'"{vec.betslip.DBL}" stake: boosted Est. Returns value "{boosted_double_stake_est_returns}" '
                f'is the same as initial value "{self.initial_double_stake_est_returns}"')

        boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{boosted_total_est_returns}" is the same as '
                                f'initial value "{self.initial_total_est_returns}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create necessary test events, add two selections with added stake amounts to the Betslip
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost['enabled']:
            raise CmsClientException('Odds Boost is disabled in CMS')
        params = self.ob_config.add_football_event_to_spanish_la_liga()
        self.__class__.first_team = params.team1
        first_team_selection_id = params.selection_ids[self.first_team]

        params = self.ob_config.add_football_event_to_spanish_la_liga()
        self.__class__.second_team = params.team2
        self.__class__.second_team_selection_id = params.selection_ids[self.second_team]

        event_without_odds_boost = self.ob_config.add_baseball_event_to_autotest_league()
        self.__class__.third_team = event_without_odds_boost.team1
        third_selection_id = event_without_odds_boost.selection_ids[self.third_team]

        username = tests.settings.odds_boost_user
        self.site.login(username=username)
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=username, level='selection', offer_id=offer_id)

        self.open_betslip_with_selections(selection_ids=[first_team_selection_id, third_selection_id])
        self.site.close_all_dialogs(async_close=False)

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)
        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)

        self.assertIn(self.first_team, singles_section, msg=f'"{self.first_team}" stake is not available')
        self.__class__.first_team_stake = singles_section[self.first_team]
        self.__class__.first_team_original_odds = self.first_team_stake.odds

        self.assertIn(self.third_team, singles_section, msg=f'"{self.third_team}" stake is not available')
        self.__class__.third_team_stake = singles_section[self.third_team]
        self.__class__.third_team_original_odds = self.third_team_stake.odds

        self.assertIn(vec.betslip.DBL, multiples_section,
                      msg=f'"{vec.betslip.DBL}" stake is not available')
        self.__class__.double_stake = multiples_section[vec.betslip.DBL]
        self.enter_stake_amount(stake=(self.double_stake.name, self.double_stake))

    def test_001_navigate_to_betslip_verify_that_odds_boost_button_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Odds Boost button is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (tooltip)
        EXPECTED: - Potential returns/ total potential returns
        """
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg=f'Button text "{self.odds_boost_header.boost_button.name}" '
                             f'is not the same as expected "{vec.odds_boost.BOOST_BUTTON.disabled}"')

        label_text = self.odds_boost_header.tap_to_boost_your_betslip_label.text
        self.assertEqual(label_text, vec.odds_boost.BETSLIP_HEADER.subtitle,
                         msg=f'"{label_text}" does not equal expected text "{vec.odds_boost.BETSLIP_HEADER.subtitle}"')

        self.assertTrue(self.odds_boost_header.info_button.is_displayed(), msg='"i" button is not displayed')

        self.__class__.initial_first_team_stake_est_returns = self.first_team_stake.est_returns
        self.assertTrue(self.initial_first_team_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{self.first_team}" stake')

        self.__class__.initial_third_team_stake_est_returns = self.third_team_stake.est_returns
        self.assertTrue(self.initial_third_team_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{self.third_team_stake}" stake')

        self.__class__.initial_double_stake_est_returns = self.double_stake.est_returns
        self.assertTrue(self.initial_double_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{vec.betslip.DBL}" stake')

        self.__class__.initial_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertTrue(self.initial_total_est_returns, msg='Total Est. Returns is not shown')

    def test_002_tap_a_boost_button_verify_that_odds_are_boosted_for_odds_with_available_odds_boost_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Tap a 'BOOST' button
        DESCRIPTION: Verify that odds are boosted for odds with available odds boost and odds boost button is displaying with animation
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) are shown for singles and for multiples section
        EXPECTED: - 'i' button with hint text: "Odds Boost is unavailable for this selection' is shown for selection w/o availability Odds Boost
        EXPECTED: - Original odds (fractional)is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns are shown for singles and for multiples section section
        """
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        if self.brand == 'bma':
            self.assertTrue(self.odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('enabled', self.odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')

        self.assertTrue(self.first_team_stake.boosted_odds_container.is_displayed(timeout=3),
                        msg=f'Boosted odds are not shown for "{self.first_team}" stake')
        self.check_odds_format(odds=self.first_team_stake.boosted_odds_container.price_value)
        self.assertTrue(self.double_stake.boosted_odds_container.is_displayed(),
                        msg=f'Boosted odds are not shown for "{vec.betslip.DBL}" stake')
        self.check_odds_format(odds=self.double_stake.boosted_odds_container.price_value)

        self.assertTrue(self.first_team_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{self.first_team}" stake')
        self.assertTrue(self.double_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{vec.betslip.DBL}" stake')

        boosted_first_team_stake_est_returns = self.first_team_stake.est_returns
        self.assertNotEqual(
            boosted_first_team_stake_est_returns, self.initial_first_team_stake_est_returns,
            msg=f'"{self.first_team}" stake: boosted Est. Returns value "{boosted_first_team_stake_est_returns}" is '
                f'the same as initial value "{self.initial_first_team_stake_est_returns}"')

        boosted_double_stake_est_returns = self.double_stake.est_returns
        self.assertNotEqual(
            boosted_double_stake_est_returns, self.initial_double_stake_est_returns,
            msg=f'"{vec.betslip.DBL}" stake: boosted Est. Returns value "{boosted_double_stake_est_returns}" '
            f'is the same as initial value "{self.initial_double_stake_est_returns}"')

        boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{boosted_total_est_returns}" is the same '
                                f'as initial value "{self.initial_total_est_returns}"')
        self.site.close_betslip()

    def test_003_navigate_to_any_other_page_reopen_betslip_verify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) are shown for singles and for multiples section
        EXPECTED: - 'i' button with hint text: "Odds Boost is unavailable for this selection' is shown for selection w/o availability to Odds Boost
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown for singles and for multiples section section
        """
        self.site.go_to_home_page()
        self.site.open_betslip()
        self.verify_odds_boost_remains_boosted()

    def test_004_refresh_page_verify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Refresh page
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown for singles and for multiples section
        EXPECTED: - 'i' button with hint text: "Odds Boost is unavailable for this selection' is shown for selection w/o availability to Odds Boost
        EXPECTED: - Original odds (fractional) are displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown for singles and for multiples section section
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_betslip()

        self.verify_odds_boost_remains_boosted()

    def test_005_add_one_more_selection_with_odds_boost_available_navigate_to_betslip_verify_that_odds_boost_remains_boosted_and_new_selection_displaying_boosted(self):
        """
        DESCRIPTION: Add one more selection with Odds Boost available
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost remains boosted and new selection displaying boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown for singles and for multiples section
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/ total potential returns are shown for singles and for multiples section section
        """
        # This is workaround to not have problem with deeplinks
        self.site.close_betslip()
        self.open_betslip_with_selections(selection_ids=self.second_team_selection_id, timeout=5)

        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')

        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.enabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg=f'Button text label "{self.odds_boost_header.boost_button.name}" '
                             f'is not the same as expected "{vec.odds_boost.BOOST_BUTTON.enabled}"')

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        stake = list(singles_section.items())[2]
        self.enter_stake_amount(stake=stake)

        self.assertIn(self.first_team, singles_section, msg=f'"{self.first_team}" stake is not available')
        self.__class__.first_team_stake = singles_section[self.first_team]
        self.assertIn(self.second_team, singles_section, msg=f'"{self.second_team}" stake is not available')
        self.__class__.second_team_stake = singles_section[self.second_team]
        self.__class__.second_team_original_odds = self.second_team_stake.odds
        self.assertIn(self.third_team, singles_section, msg=f'"{self.third_team}" stake is not available')
        self.__class__.third_team_stake = singles_section[self.third_team]

        self.assertIn(vec.betslip.TBL, multiples_section,
                      msg=f'"{vec.betslip.TBL}" stake is not available')
        self.__class__.treble_stake = multiples_section[vec.betslip.TBL]
        self.__class__.treble_original_odds = self.treble_stake.odds
        self.enter_stake_amount(stake=(self.treble_stake.name, self.treble_stake))

        self.assertTrue(self.first_team_stake.boosted_odds_container.is_displayed(),
                        msg=f'Boosted odds are not shown for "{self.first_team}" stake')
        self.check_odds_format(odds=self.first_team_stake.boosted_odds_container.price_value)
        self.assertTrue(self.second_team_stake.boosted_odds_container.is_displayed(),
                        msg=f'Boosted odds are not shown for "{self.second_team}" stake')
        self.check_odds_format(odds=self.second_team_stake.boosted_odds_container.price_value)
        self.assertTrue(self.treble_stake.boosted_odds_container.is_displayed(),
                        msg=f'Boosted odds are not shown for "{vec.betslip.TBL}" stake')
        self.check_odds_format(odds=self.treble_stake.boosted_odds_container.price_value)

        self.assertTrue(self.first_team_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{self.first_team}" stake')
        self.assertTrue(self.second_team_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{self.second_team}" stake')
        self.assertTrue(self.treble_stake.is_original_odds_crossed,
                        msg=f'Original odds are not crossed out for "{vec.betslip.TBL}" stake')

        self.__class__.boosted_first_team_stake_est_returns = self.first_team_stake.est_returns
        self.assertNotEqual(
            self.boosted_first_team_stake_est_returns, self.initial_first_team_stake_est_returns,
            msg=f'"{self.first_team}" stake: boosted Est. Returns value "{self.boosted_first_team_stake_est_returns}" '
                f'is the same as initial value "{self.initial_first_team_stake_est_returns}"')
        self.__class__.boosted_second_team_stake_est_returns = self.second_team_stake.est_returns
        self.assertTrue(self.boosted_second_team_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{self.second_team}" stake')
        self.__class__.boosted_treble_stake_est_returns = self.treble_stake.est_returns
        self.assertTrue(self.boosted_treble_stake_est_returns,
                        msg=f'Est. Returns is not shown for "{vec.betslip.TBL}" stake')
        self.__class__.boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(self.boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{self.boosted_total_est_returns}" is the same '
                                f'as initial value "{self.initial_total_est_returns}"')

    def test_006_tap_boosted_button_verify_that_odds_boost_are_removed_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost are removed and odds boost button is displaying with animation
        EXPECTED: Betslip is displayed with the following elements:
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
        if self.brand == 'bma':
            self.assertTrue(self.odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('disabled', self.odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boost reverting')

        for stake in [self.first_team_stake, self.second_team_stake, self.treble_stake]:
            self.assertFalse(stake.has_boosted_odds, msg=f'"{stake.name}" should not have boosted odds')

        first_team_stake_est_returns = self.first_team_stake.est_returns
        self.assertEqual(first_team_stake_est_returns, self.initial_first_team_stake_est_returns,
                         msg=f'"{self.first_team}" stake: Est. Returns value "{first_team_stake_est_returns}" is not '
                             f'the same as initial value "{self.initial_first_team_stake_est_returns}"')

        second_team_stake_est_returns = self.second_team_stake.est_returns
        self.assertNotEqual(
            second_team_stake_est_returns, self.boosted_second_team_stake_est_returns,
            msg=f'"{self.second_team}" stake: Est. Returns value "{second_team_stake_est_returns}" is the same as '
                f'initial value with boosted odds "{self.boosted_second_team_stake_est_returns}"')

        treble_stake_est_returns = self.treble_stake.est_returns
        self.assertNotEqual(
            treble_stake_est_returns, self.boosted_treble_stake_est_returns,
            msg=f'"{vec.betslip.TBL}" stake: Est. Returns value "{treble_stake_est_returns}" is the '
                f'same as initial value with boosted odds "{self.boosted_treble_stake_est_returns}"')

        total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(total_est_returns, self.boosted_total_est_returns,
                            msg=f'Total Est. Returns value "{total_est_returns}" is the same as value with '
                                f'boosted odds "{self.boosted_total_est_returns}"')

    def test_007_navigate_to_any_other_page_reopen_betslip_verify_that_odds_boost_remains_unboosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains UNboosted
        EXPECTED: Odds boost 'Off' status is remembered:
        EXPECTED: - 'BOOST' button is shown
        EXPECTED: - Original odds is shown
        EXPECTED: - Original potential returns/ total potential returns is shown
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')

        self.site.open_betslip()

        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg=f'Button text label "{odds_boost_header.boost_button.name}" is not '
                             f'the same as expected "{vec.odds_boost.BOOST_BUTTON.disabled}"')

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        self.assertIn(self.first_team, singles_section, msg=f'"{self.first_team}" stake is not available')
        first_team_odds = singles_section[self.first_team].odds
        self.assertEqual(first_team_odds, self.first_team_original_odds,
                         msg=f'"{self.first_team}" stake: odds value "{first_team_odds}" is not the '
                             f'same as expected "{self.first_team_original_odds}"')

        self.assertIn(self.second_team, singles_section, msg=f'"{self.second_team}" stake is not available')
        second_team_odds = singles_section[self.second_team].odds
        self.assertEqual(second_team_odds, self.second_team_original_odds,
                         msg=f'"{self.second_team}" stake: odds value "{second_team_odds}" is not '
                             f'the same as expected "{self.second_team_original_odds}"')

        self.assertIn(self.third_team, singles_section, msg=f'"{self.third_team}" stake is not available')
        third_team_odds = singles_section[self.third_team].odds
        self.assertEqual(third_team_odds, self.third_team_original_odds,
                         msg=f'"{self.third_team}" stake: odds value "{third_team_odds}" is not the '
                             f'same as expected "{self.third_team_original_odds}"')

        self.assertIn(vec.betslip.TBL, multiples_section,
                      msg=f'"{vec.betslip.TBL}" stake is not available')
        treble_odds = multiples_section[vec.betslip.TBL].odds
        self.assertEqual(treble_odds, self.treble_original_odds,
                         msg=f'"{vec.betslip.TBL}" stake: odds value "{treble_odds}" is not '
                             f'the same as expected "{self.treble_original_odds}"')

    def test_008_change_odd_format_to_decimal_verify_that_this_functionality_works_the_same_with_decimal_odds(self):
        """
        DESCRIPTION: Change odd format to Decimal
        DESCRIPTION: Verify that this functionality works the same with decimal odds
        EXPECTED: - Boosted odds is shown for singles and for multiples section in decimal
        EXPECTED: - Original odds is displayed as crossed out in decimal
        """
        self.site.close_betslip()
        is_format_changed = self.site.change_odds_format(odds_format='DECIMAL')
        self.assertTrue(is_format_changed, msg='Odds format is not changed to Decimal')
        self.site.go_to_home_page()
        self.site.open_betslip()
        self.get_betslip_content().odds_boost_header.boost_button.click()

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        self.assertIn(self.first_team, singles_section, msg=f'"{self.first_team}" stake is not available')
        first_team_stake = singles_section[self.first_team]
        self.assertIn(self.second_team, singles_section, msg=f'"{self.second_team}" stake is not available')
        second_team_stake = singles_section[self.second_team]
        self.assertIn(vec.betslip.TBL, multiples_section,
                      msg=f'"{vec.betslip.TBL}" stake is not available')
        treble_stake = multiples_section[vec.betslip.TBL]

        for stake in [first_team_stake, second_team_stake, treble_stake]:
            self.assertTrue(stake.boosted_odds_container.is_displayed(),
                            msg=f'Boosted odds are not shown for "{stake.name}" stake')
            self.check_odds_format(odds=stake.boosted_odds_container.price_value, expected_odds_format='decimal')
            self.assertTrue(stake.is_original_odds_crossed,
                            msg=f'Original odds are not crossed out for "{stake.name}" stake')
