from collections import OrderedDict
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import convert_weight_pounds_to_stones
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2  # Coral only as race_form_info not available for Ladbrokes right now
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.race_form
@pytest.mark.medium
@pytest.mark.races
@vtest
# TODO: "race_form_info" is not available in Ladbrokes right now. Test should be verified in ladbrokes once it is
#  available.
class Test_C1056144_Verify_Race_Spotlight_Overview(BaseRacing):
    """
    TR_ID: C1056144
    NAME: Verify Race Spotlight Overview
    DESCRIPTION: This test case verifies Horse Racing post overview
    """
    keep_browser_open = True
    price_types = ['SP', 'LP', 'S']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event with RacingPost info
        """
        self.__class__.event_info = self.get_racing_event_with_form_details(distance=True, going=True)
        if not self.event_info:
            raise SiteServeException('Racing events with distance and going details are not available')
        self.__class__.event_id = list(self.event_info.keys())[0]
        self.__class__.horses = self.event_info[self.event_id]['horses']
        self.__class__.racing_form_outcomes_info = OrderedDict()
        for horse in self.horses:
            self.__class__.racing_form_outcomes_info.update({horse['horseName']: horse})
        self.__class__.is_mobile = True if self.device_type in ['mobile'] else False

    def test_001_open_event_details_page_with_silks_available(self):
        """
        DESCRIPTION: Go to the event details page for the Event which has SILKS available
        EXPECTED: 'Horse Racing' landing page is opened
        EXPECTED: Generic Silks are displayed for missed mappings
        EXPECTED: Correct silks are displayed for mapped selections (silkName)
        EXPECTED: Runner number and Draw are correct and displayed only if not = '0' and are present in response (runnerNumber, draw)
        EXPECTED: Horse name (name)
        EXPECTED: Jockey/Trainer
        EXPECTED: Form (formGuide)
        EXPECTED: Course (C), Course and Distance (CD) or Distance (D) winner badge (courseDistanceWinner)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.racing_form_outcomes_keys = self.racing_form_outcomes_info.keys()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')

        market = list(markets.values())[0]
        self.__class__.outcomes = market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')

        for outcome_name, outcome in self.outcomes.items():
            if outcome_name in self.racing_form_outcomes_keys:
                self.assertIn(outcome_name, self.racing_form_outcomes_keys,
                              msg=f'Outcome "{outcome_name}" is not present in SS response')
                if not outcome.is_odds_button_disabled:
                    self.assertTrue(outcome.has_silks, msg=f'No silk present for outcome "{outcome_name}"')

                if self.racing_form_outcomes_info[outcome_name] != 'generic':
                    runner_number = self.racing_form_outcomes_info[outcome_name]['saddle']
                    self.assertEqual(runner_number, outcome.runner_number,
                                     msg=f'Runner number "{runner_number}" for outcome "{outcome_name}" '
                                         f'is not the same as expected "{outcome.runner_number}"')

                    if self.racing_form_outcomes_info[outcome_name].get('draw'):
                        draw_number = self.racing_form_outcomes_info[outcome_name]['draw']
                        self.assertEqual(draw_number, outcome.draw_number,
                                         msg=f'Draw number "{draw_number}" for outcome "{outcome_name}" '
                                             f'is not the same as expected "{outcome.draw_number}"')
                    else:
                        self._logger.warning(f'*** No draw number for outcome "{outcome_name}"')

                    self.assertTrue(outcome.horse_name, msg=f'Horse name is not present for outcome "{outcome_name}"')
                    if self.racing_form_outcomes_info[outcome_name].get('trainer'):
                        expected_trainer = self.racing_form_outcomes_info[outcome_name]['trainer']
                        actual_trainer = outcome.trainer_name.split(':')[1].strip()
                        self.assertEqual(actual_trainer, expected_trainer,
                                         msg=f'Trainer name "{actual_trainer}" for outcome "{outcome_name}" '
                                             f'is not the same as expected "{expected_trainer}"')
                    else:
                        self._logger.warning(f'*** No trainer name for outcome "{outcome_name}"')

                    if self.racing_form_outcomes_info[outcome_name].get('jockey'):
                        expected_jockey = self.racing_form_outcomes_info[outcome_name].get('jockey')
                        actual_jockey = outcome.jockey_name.split(':')[1].split('(')[0].strip()

                        self.assertEqual(actual_jockey, expected_jockey,
                                         msg=f'Jockey name "{actual_jockey}" for outcome "{outcome_name}" '
                                             f'is not the same as expected "{expected_jockey}"')
                    else:
                        self._logger.warning(f'*** No jockey name for outcome "{outcome_name}"')

                    if self.racing_form_outcomes_info[outcome_name].get('formfigs'):
                        form = self.racing_form_outcomes_info[outcome_name]['formfigs']
                        form = f'Form: {form}'
                        self.assertEqual(form, outcome.form,
                                         msg=f'Form "{form}" for outcome "{outcome_name}" '
                                             f'is not the same as expected "{outcome.form}"')
                    else:
                        self._logger.warning(f'*** No jockey name for outcome "{outcome_name}"')
                else:
                    self._logger.warning(f'*** No spotlight overview for generic outcome "{outcome_name}"')

    def test_002_go_to_the_event_selection_area_and_tap_within_the_area(self):
        """
        DESCRIPTION: Go to the Event selection area and tap within the area (or on the arrow on the right side)
        EXPECTED: Horse information is expanded showing information about the runner
        EXPECTED: *OR (officialRating)
        EXPECTED: *Age # yo (age)
        EXPECTED: *Weight
        """
        for outcome_name, outcome in self.outcomes.items():
            if outcome_name in self.racing_form_outcomes_keys:
                if self.racing_form_outcomes_info[outcome_name] != 'generic':
                    outcome.scroll_to()
                    outcome.click()
                    if self.racing_form_outcomes_info[outcome_name].get('formProviderRating'):
                        actual_rating = outcome.spotlight_overview.official_rating.value
                        expected_rating = self.racing_form_outcomes_info[outcome_name]['formProviderRating']
                        self.assertEqual(actual_rating, expected_rating,
                                         msg=f'Rating "{actual_rating}" for outcome "{outcome_name}" '
                                             f'is not the same as expected "{expected_rating}"')
                    else:
                        self._logger.warning(f'*** No OR for outcome "{outcome_name}" available')

                    if self.racing_form_outcomes_info[outcome_name].get('age'):
                        actual_age = outcome.spotlight_overview.age.value
                        expected_age = self.racing_form_outcomes_info[outcome_name]['age']
                        self.assertEqual(actual_age, expected_age,
                                         msg=f'Age "{actual_age}" for outcome "{outcome_name}" '
                                             f'is not the same as expected "{expected_age}"')
                    else:
                        self._logger.warning(f'*** No Age for outcome "{outcome_name}" available')

                    if self.racing_form_outcomes_info[outcome_name].get('weightLbs'):
                        ss_weight = self.racing_form_outcomes_info[outcome_name]['weightLbs']
                        st, lb = convert_weight_pounds_to_stones(ss_weight)
                        expected_weight = f'{st}st-{lb}lb' if lb else f'{st}st'
                        self.assertEqual(outcome.spotlight_overview.weight.value, expected_weight,
                                         msg=f'Weight "{outcome.spotlight_overview.weight.value}" for '
                                             f'outcome "{outcome_name}"is not the same as expected "{expected_weight}"')
                    else:
                        self._logger.warning(f'*** No Weight for outcome "{outcome_name}" available')
                else:
                    self._logger.warning(f'*** No spotlight overview for generic outcome "{outcome_name}"')

    def test_003_verify_info_for_spotlight_section(self):
        """
        DESCRIPTION: Verify info for 'Spotlight' section
        EXPECTED: For mobile&tablet:
        EXPECTED: * 100 characters <Race> information for Horse is displayed, followed by 'Show More' link
        EXPECTED: * Tapping on 'Show More' link, shows the whole information text, link is changed to 'Show Less'
        EXPECTED: * Information corresponds to the one in 'overview' attribute
        EXPECTED: For desktop:
        EXPECTED: * The whole information text is shown
        """
        for outcome_name, outcome in self.outcomes.items():
            if outcome_name in self.racing_form_outcomes_keys:
                if self.racing_form_outcomes_info[outcome_name] != 'generic':
                    outcome.scroll_to()
                    outcome.show_summary_toggle.click()
                    overview = next((horse.get('spotlight') for horse in self.event_info[self.event_id]['horses']
                                     if horse['horseName'] == outcome_name.rstrip(' N/R')), False)
                    if overview:
                        if self.is_mobile:
                            expected_button_name = 'Show More'
                            result = wait_for_result(
                                lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                                name=f'Button name {vec.racing.SHOW_MORE}',
                                timeout=1)
                            self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                        f'is not the same as expected "{expected_button_name}"')
                            outcome.show_summary_toggle.click()
                            expected_button_name = 'Show Less'
                            result = wait_for_result(
                                lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                                name=f'Button name {vec.racing.SHOW_LESS}',
                                timeout=1)
                            self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                        f'is not the same as expected "{expected_button_name}"')

                            self.assertEqual(overview, outcome.spotlight_overview.summary_text.value,
                                             msg=f'Summary text "{overview}" is not the same '
                                                 f'as expected "{outcome.spotlight_overview.summary_text.value}" '
                                                 f'for outcome "{outcome_name}"')

                            spotlight_overview = outcome.spotlight_overview
                            self.assertFalse(spotlight_overview.summary_text.is_truncated(),
                                             msg=f'Spotlight overview summary text is truncated for outcome '
                                                 f'"{outcome_name}" after expanding')
                            outcome.show_summary_toggle.click()
                            expected_button_name = 'Show More'
                            result = wait_for_result(
                                lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                                name=f'Button name {vec.racing.SHOW_MORE}',
                                timeout=1)
                            self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" '
                                                        f'is not the same as expected "{expected_button_name}"')
                        else:
                            outcome.click()
                            self.assertEqual(overview, outcome.spotlight_overview.summary_text.value,
                                             msg=f'Summary text "{overview}" is not the same '
                                                 f'as expected "{outcome.spotlight_overview.summary_text.value}" '
                                                 f'for outcome "{outcome_name}"')
                    else:
                        self._logger.warning(f'*** No overview for outcome "{outcome_name}" available')
                else:
                    self._logger.warning(f'*** No spotlight overview for generic outcome "{outcome_name}"')

    def test_004_verify_price_odds_buttons(self):
        """
        DESCRIPTION: Verify 'Price/Odds' buttons
        EXPECTED: Price / odds buttons are shown near each selection
        EXPECTED: 3 types of price type can be shown near selection: SP LP S
        """
        for outcome_name, outcome in self.outcomes.items():
            if outcome_name in self.racing_form_outcomes_keys:
                self.assertTrue(outcome.bet_button.is_displayed(),
                                msg=f'Outcome "{outcome_name}" has no bet button"')
