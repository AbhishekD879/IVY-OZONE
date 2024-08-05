import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_beta2
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.race_form
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.reg157_fix
@vtest
class Test_C10436245_Ladbrokes_Verify_detailed_information_for_each_selection_on_the_Race_Card_EDP(BaseRacing):
    """
    TR_ID: C10436245
    NAME: [Ladbrokes] Verify detailed information for each selection on the Race Card (EDP)
    DESCRIPTION: This test case verifies 'SHOW MORE'/'SHOW LESS' button and info that it expands for each selection on the Race Card (EDP)
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get an event with race information and navigating to HorseRacing EDP page
        """
        self.__class__.expected_star_ratings = ['1', '2', '3', '4', '5']
        self.__class__.event_info = self.get_racing_event_with_form_details(star_rating=self.expected_star_ratings)
        if not self.event_info:
            raise SiteServeException('Star rating racing events are not available')
        self.__class__.event_id = self.event_info[0]
        self.__class__.horses_details = self.event_info[1]
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_001_verify_the_show_more__button_is_present_after_form_value_text_for_the_specific_horse(self):
        """
        DESCRIPTION: Verify the 'SHOW MORE ⋁' button is present after 'Form: [value]' text for the specific horse
        EXPECTED: * The blue 'SHOW MORE ⋁' button is displayed
        EXPECTED: * No more text below 'SHOW MORE ⋁' button for the horse
        """
        self.__class__.markets = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg=f'No markets found for event {self.event_id}')
        market = self.markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        market.click()
        self.device.refresh_page()
        self.__class__.outcomes = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.get(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB).items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No outcomes found for event {self.event_id}')

    def test_002_tap_show_more__button(self):
        """
        DESCRIPTION: Tap 'SHOW MORE ⋁' button
        EXPECTED: * The 'SHOW MORE ⋁' button is changed to 'SHOW LESS ⋀'
        EXPECTED: * The further information from Racing Post is displayed:
        EXPECTED: **Mobile**
        EXPECTED: - Runner Age
        EXPECTED: - Runner Weight
        EXPECTED: - RPR
        EXPECTED: - Runner Comment
        EXPECTED: - CD/C/BF (if a course winner and/or if a beaten favorite)
        EXPECTED: - Star Rating
        EXPECTED: **Desktop**
        EXPECTED: - Runner Age
        EXPECTED: - Runner Weight
        EXPECTED: - RPR
        EXPECTED: - Runner Comment
        EXPECTED: - CD/C/BF (if a course winner and/or if a beaten favorite)
        EXPECTED: - Star Rating (aligned to the right)
        EXPECTED: - Detailed Form
        """
        for horse_name, horse_details in self.horses_details.items():
            if not self.outcomes[horse_name].is_non_runner:
                if self.horses_details[horse_name].get('formfigs'):
                    expected_form = "Form: " + self.horses_details[horse_name]['formfigs']
                else:
                    expected_form = "Form: -"
                actual_form = self.outcomes[horse_name].form
                self.assertEqual(expected_form, actual_form,
                                 msg=f"expected {horse_name} horse Form is {expected_form} but actual is {actual_form}")
                if not self.outcomes[horse_name].has_expanded_summary():
                    self.outcomes[horse_name].show_summary_toggle.click()
                result = wait_for_result(lambda: self.outcomes[horse_name].toggle_icon_name.upper() == vec.racing.SHOW_LESS.upper(),
                                         name=f'Button name {vec.racing.SHOW_LESS}',
                                         timeout=1)
                self.assertTrue(result, msg=f'Expected toggle icon "{vec.racing.SHOW_LESS.upper()}" but actual is "{self.outcomes[horse_name].toggle_icon_name.upper()}"')
                if self.horses_details[horse_name].get('horseAge'):
                    expected_horse_age = str(self.horses_details[horse_name].get('horseAge'))
                    actual_horse_age = self.outcomes[horse_name].spotlight_overview.age.value
                    self.assertEqual(expected_horse_age, actual_horse_age,
                                     msg=f"expected {horse_name} horse age is {expected_horse_age} but actual is {actual_horse_age}")
                if self.horses_details[horse_name].get('weight'):
                    runner_weight = self.horses_details[horse_name]['weight']
                    st, lb = runner_weight.split('-')
                    expected_horse_weight = f'{st}st' if lb == '0' else f'{st}st-{lb}lb'
                    actual_horse_weight = self.outcomes[horse_name].spotlight_overview.weight.value
                    self.assertEqual(expected_horse_weight, actual_horse_weight,
                                     msg=f"expected {horse_name} horse weight is {expected_horse_weight} but actual is {actual_horse_weight}")
                if self.horses_details[horse_name].get('rating'):
                    expected_horse_rating = self.horses_details[horse_name]['rating']
                    actual_horse_rating = self.outcomes[horse_name].spotlight_overview.official_rating.value
                    self.assertEqual(expected_horse_rating, actual_horse_rating,
                                     msg=f"expected {horse_name} horse rating is {expected_horse_rating} but actual is {actual_horse_rating}")
                if self.horses_details[horse_name].get('spotlight'):
                    expected_horse_summary = self.horses_details[horse_name]['spotlight']
                    actual_horse_summary = self.outcomes[horse_name].spotlight_overview.summary_text.value
                    self.assertEqual(expected_horse_summary, actual_horse_summary,
                                     msg=f"expected {horse_name} horse summary is {expected_horse_summary} but actual is {actual_horse_summary}")
                if self.horses_details[horse_name].get('courseDistanceWinner'):
                    expected_horse_course_distance_winner = self.horses_details[horse_name]['courseDistanceWinner']
                    actual_horse_course_distance_winner = ','.join(self.outcomes[horse_name].course_distance_winner)
                    self.assertEqual(expected_horse_course_distance_winner, actual_horse_course_distance_winner,
                                     msg=f"expected {horse_name} horse course distance winner is {expected_horse_course_distance_winner} but actual is {actual_horse_course_distance_winner}")
                if self.horses_details[horse_name].get('starRating'):
                    expected_horse_star_rating = self.horses_details[horse_name]['starRating']
                    actual_horse_star_rating = self.outcomes[horse_name].stars_container.get_star_rating(is_active=True)
                    self.assertEqual(expected_horse_star_rating, str(actual_horse_star_rating),
                                     msg=f'f"expected {horse_name} horse star rating is {expected_horse_star_rating} but actual is {actual_horse_star_rating}')
                if self.outcomes[horse_name].has_expanded_summary():
                    self.outcomes[horse_name].show_summary_toggle.click()
                result = wait_for_result(lambda: self.outcomes[horse_name].toggle_icon_name.upper() == vec.racing.SHOW_MORE.upper(),
                                         name=f'Button to have name {vec.racing.SHOW_MORE}',
                                         timeout=1)
                self.assertTrue(result, msg=f'Expected toggle icon "{self.outcomes[horse_name].toggle_icon_name.upper()}" but actual is "{vec.racing.SHOW_MORE.upper()}" ')
                self.assertFalse(self.outcomes[horse_name].has_spotlight_overview(expected_result=False, timeout=3),
                                 msg='Spotlight overview is shown')

    def test_003_verify_runner_age(self):
        """
        DESCRIPTION: Verify Runner Age
        EXPECTED: Runner Age = 'horseAge' attribute from Racing Post response
        """
        pass
        # This step is covered in scope of step 2

    def test_004_verify_runner_weight(self):
        """
        DESCRIPTION: Verify Runner Weight
        EXPECTED: Runner Weight = 'weight' attribute from Racing Post response
        """
        pass
        # this step is covered in scope of test step 2

    def test_005_verify_rpr(self):
        """
        DESCRIPTION: Verify RPR
        EXPECTED: PRP = 'rating' attribute from the Racing Post response
        """
        pass
        # this step is covered in scope of test step 2

    def test_006_verify_runner_comment(self):
        """
        DESCRIPTION: Verify Runner Comment
        EXPECTED: Runner Comment = 'spotlight' attribute from the Racing Post response
        """
        pass
        # this step is covered in scope of test step 2

    def test_007_verify_cdcbf(self):
        """
        DESCRIPTION: Verify CD/C/BF
        EXPECTED: CD/C/BF = 'courseDistanceWinner' attribute from the Racing Post response
        """
        pass
        # this step is covered in scope of test step 2

    def test_008_verify_star_rating(self):
        """
        DESCRIPTION: Verify Star Rating
        EXPECTED: Star Rating = 'starRating' attribute from the Racing Post response
        """
        pass
        # this step is covered in scope of test step 2

    def test_009_verify_detailed_form(self):
        """
        DESCRIPTION: Verify Detailed Form
        EXPECTED: * Information in the table view
        EXPECTED: * Detailed Form = 'formfigs' array from the Racing Post response
        """
        pass
        # this step is covered in scope of test step 2

    def test_010_tap_show_less__button(self):
        """
        DESCRIPTION: Tap 'SHOW LESS ⋀' button
        EXPECTED: * The blue 'SHOW MORE ⋁' button is displayed
        EXPECTED: * No more text below 'SHOW MORE ⋁' button for the horse
        """
        pass
        # this step is covered in scope of test step 2