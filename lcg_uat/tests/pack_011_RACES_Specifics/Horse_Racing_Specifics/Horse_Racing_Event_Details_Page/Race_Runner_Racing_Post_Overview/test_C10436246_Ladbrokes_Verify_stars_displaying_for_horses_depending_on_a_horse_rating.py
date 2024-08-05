import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_tst2  # Ladbrokes only
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_beta2
@pytest.mark.reg165_fix
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.high
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.reg157_fix
@vtest
class Test_C10436246_Ladbrokes_Verify_stars_displaying_for_horses_depending_on_a_horse_rating(BaseRacing,
                                                                                              BaseBetSlipTest):
    """
    TR_ID: C10436246
    NAME: [Ladbrokes] Verify stars displaying for horses depending on a horse rating
    DESCRIPTION: This test case verifies displaying of rating for horses with a 5-star rating and with less than 5-star rating
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get an event with race information and navigating to HorseRacing EDP page
        """
        self.__class__.expected_star_ratings = ['5']
        self.__class__.event_info = self.get_racing_event_with_form_details(star_rating=self.expected_star_ratings)
        if not self.event_info:
            raise SiteServeException('5 Star rating racing events are not available')
        self.__class__.event_id = self.event_info[0]
        self.__class__.star_rating_horses_details = self.event_info[1]
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_001_verify_displaying_stars_for_horses_selections_with_a_5_star_rating(self):
        """
        DESCRIPTION: Verify displaying stars for horses (selections) with a 5-star rating
        EXPECTED: * The number of stars is equal to the star rating retrieved from 'Racing Post' response
        EXPECTED: * There is a '★5' in a rectangle sign next to selection name
        EXPECTED: * Stars correspond to "StarRating" attribute from 'Racing Post' response
        """
        self.__class__.markets = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg=f'No markets found for event {self.event_id}')
        market = self.markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        market.click()
        self.__class__.outcomes = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.get(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB).items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No outcomes found for event {self.event_id}')
        expected_five_star_horse_name, self.__class__.expected_horse_rating = next(
            (horse_name, horse_details['starRating']) for horse_name, horse_details in
            self.star_rating_horses_details.items() if horse_details['starRating'] in self.expected_star_ratings)
        self.__class__.actual_five_star_horse_name, self.__class__.actual_five_star_horse = next(
            ((horse_name, self.outcomes[horse_name]) for horse_name in self.outcomes.keys() if
             horse_name.upper() == expected_five_star_horse_name.upper()), False)
        self.assertTrue(self.actual_five_star_horse, msg=f'"{expected_five_star_horse_name}" horse is not available')
        if not self.actual_five_star_horse.is_non_runner:
            self.assertTrue(self.actual_five_star_horse.has_stars(),
                            msg=f'"{expected_five_star_horse_name}" horse is not having 5 star rating')
            actual_horse_rating = self.actual_five_star_horse.stars_rating_value.name
            self.assertEqual(actual_horse_rating, self.expected_horse_rating,
                             msg=f'Expected horse star rating is "{self.expected_horse_rating}" but actual rating is "{actual_horse_rating}"')

    def test_002__tap_show_more_button_verify_stars_for_horses_selections_with_a_5_star_rating(self):
        """
        DESCRIPTION: * Tap 'SHOW MORE' button
        DESCRIPTION: * Verify stars for horses (selections) with a 5-star rating
        EXPECTED: * 5 yellow stars are displayed below 'Odds' button, on the same level as Age, Weight, RPR CD/C/BF info
        """
        if not self.actual_five_star_horse.is_non_runner:
            self.actual_five_star_horse.show_summary_toggle.click()
            self.assertTrue(self.actual_five_star_horse.has_expanded_summary(),
                            msg='Summary is not shown after expanding selection')
            active_horse_rating = self.actual_five_star_horse.stars_container.get_star_rating(is_active=True)
            self.assertEqual(str(active_horse_rating), self.expected_horse_rating,
                             msg=f'"{str(active_horse_rating)}" Yellow stars are not '
                                 f'matched with expected: "{self.expected_horse_rating}" stars')
            self.actual_five_star_horse.show_summary_toggle.click()
            self.assertFalse(self.actual_five_star_horse.has_expanded_summary(expected_result=False),
                             msg='Summary is shown after collapsing selection')

    def test_003__verify_displaying_stars_for_horses_with_less_than_a_5_star_rating(self):
        """
        DESCRIPTION: * Verify displaying stars for horses with less than a 5-star rating
        EXPECTED: * Stars are displayed below 'Odds' button, on the same level as Age, Weight, RPR CD/C/BF info
        EXPECTED: * 5 stars are displayed for all horses (selections).
        EXPECTED: * The yellow stars show the rating of the horse
        EXPECTED: * Yellow stars correspond to "StarRating" attribute from 'Racing Post' response
        """
        self.__class__.expected_star_ratings = ['1', '2', '3', '4']
        self.__class__.event_info = self.get_racing_event_with_form_details(star_rating=self.expected_star_ratings)
        if not self.event_info:
            raise SiteServeException('Less than 5 Star rating horse racing events are not available')
        self.__class__.event_id = self.event_info[0]
        self.__class__.star_rating_horses_details = self.event_info[1]
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.markets = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.assertTrue(self.markets, msg=f'No markets found for event {self.event_id}')
        self.__class__.outcomes = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.get(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB).items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No outcomes found for event {self.event_id}')

        expected_star_horse_name, self.__class__.expected_horse_rating = next(
            (horse_name, horse_details['starRating']) for horse_name, horse_details in
            self.star_rating_horses_details.items() if horse_details['starRating'] in self.expected_star_ratings)
        self.__class__.actual_star_horse_name, self.__class__.actual_star_horse = next(
            ((horse_name, self.outcomes[horse_name]) for horse_name in self.outcomes.keys() if
             horse_name.upper() == expected_star_horse_name.upper()), False)
        self.assertTrue(self.actual_star_horse, msg=f'"{expected_star_horse_name}" horse is not available')
        if not self.actual_star_horse.is_non_runner:
            self.actual_star_horse.scroll_to()
            if not self.actual_star_horse.has_expanded_summary():
                self.actual_star_horse.show_summary_toggle.click()
                self.assertTrue(self.actual_star_horse.has_expanded_summary(),
                                msg='Summary is not shown after expanding selection')
            active_horse_rating = self.actual_star_horse.stars_container.get_star_rating(is_active=True)
            self.assertEqual(str(active_horse_rating), self.expected_horse_rating,
                             msg=f'"{str(active_horse_rating)}" Yellow stars are not '
                                 f'matched with expected: "{self.expected_horse_rating}" stars')