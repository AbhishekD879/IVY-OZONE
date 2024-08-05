import pytest
import random
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from time import sleep


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sanity
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C874356_Horse_Racing_Bet_Filter(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C874356
    NAME: Horse Racing Bet Filter
    PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
    PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
    PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
    PRECONDITIONS: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=739471&group_order=asc
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
        PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
        PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
        """
        cms_config = self.get_initial_data_system_configuration().get('BetFilterHorseRacing')
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
        if not cms_config:
            raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
        if not cms_config.get('enabled'):
            raise CmsClientException('"Horseracing Bet Filter" is disabled')

    def test_001_load_oxygen_app___go_to_horse_racing(self):
        """
        DESCRIPTION: Load Oxygen App -> Go to Horse racing
        EXPECTED: * Horse landing page is opened
        EXPECTED: * 'Bet Filter' link on the Horse Racing header in the right
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('horse-racing')
        self.assertTrue(self.site.horse_racing.bet_filter_link.is_displayed(),
                        msg='The bet filter button is not displayed on the Horse Racing Landing page')

    def test_002_tap_bet_filter_link(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link
        EXPECTED: Bet finder page contains:
        EXPECTED: * Text 'BET FILTER ...'
        EXPECTED: * Following Filters groups:
        EXPECTED: * Meetings
        EXPECTED: * Odds
        EXPECTED: * Form
        EXPECTED: * Going (Ground Type)
        EXPECTED: * Digital Tipster Filters
        EXPECTED: * Select Star Rating
        EXPECTED: * --------------------
        EXPECTED: * 'Save selection' button
        EXPECTED: * 'Find bets' button
        """
        self.openBetFilterPage()
        self.__class__.bet_filter = self.site.horseracing_bet_filter
        actual_title = self.bet_filter.content_title_text
        self.assertEqual(actual_title, vec.bet_finder.BF_HEADER_TITLE,
                         msg=f'Actual text: "{actual_title}" is not same as '
                             f'Expected text: "{vec.bet_finder.BF_HEADER_TITLE}"')
        filter_groups = self.bet_filter.filter_groups_names
        actual_filter_groups = [filter.text for filter in filter_groups]
        expected_bma_filter_groups = [vec.bet_finder.MEETINGS, vec.bet_finder.ODDS, vec.bet_finder.FORM,
                                      vec.bet_finder.GOING_GROUND_TYPE, vec.bet_finder.SUPERCOMPUTER_FILTERS,
                                      vec.bet_finder.SELECT_STAR_RATING]
        expected_lad_filter_groups = [vec.bet_finder.ODDS_RANGE, vec.bet_finder.FORM, vec.bet_finder.PROVEN_GROUND,
                                      vec.bet_finder.FORM, vec.bet_finder.SELECT_STAR_RATING]
        self.assertListEqual(actual_filter_groups, expected_bma_filter_groups if self.brand == 'bma' else expected_lad_filter_groups,
                             msg=f'Actual Filter groups: "{actual_filter_groups}" are not same as Expected Filter groups: '
                                 f'"{expected_bma_filter_groups if self.brand == "bma" else expected_lad_filter_groups}"')
        self.assertTrue(self.bet_filter.save_selection_button.is_displayed(),
                        msg='The Save Selection button is not displayed')
        self.assertTrue(self.bet_filter.find_bets_button.is_displayed(),
                        msg='The Find Bets button is not displayed')

    def test_003_verify_meetings_filter(self):
        """
        DESCRIPTION: Verify Meetings filter
        EXPECTED: * 'All meetings' value selected by default
        EXPECTED: * Select any value -> Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"course": "combobox_value"} param
        """
        self.__class__.bet_filter = self.site.horseracing_bet_filter
        meetings = self.bet_filter.meetings_drop_down
        self.assertTrue(meetings, msg='The meetings dropdown is not displayed')
        self.assertTrue(meetings.is_option_selected(option=vec.bet_finder.ALL_MEETINGS),
                        msg='The meeting option is not selected')
        sleep(4)  # getting empty list for meetings drop down options
        options = self.bet_filter.meetings_drop_down.available_options
        if not options:
            options = self.bet_filter.meetings_drop_down.available_options
        self.assertTrue(options, msg='No available options found')
        random_option = random.choice(options)
        self.bet_filter.meetings_drop_down.select_value(random_option.title())
        self.site.wait_splash_to_hide(timeout=5)
        self.assertTrue(self.bet_filter.meetings_drop_down.is_option_selected(option=random_option.title() if self.brand == 'bma' else random_option.upper()),
                        msg=f'Selected option is not "{random_option}"')
        expected_number_of_bets = self.get_number_of_bets(course=random_option)
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
            name='Number of bets to change',
            timeout=3)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{random_option}".'
                            f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(expected_number_of_bets)
        self.bet_filter.reset_link.click()

    def test_004_verify_odds_filter(self):
        """
        DESCRIPTION: Verify Odds filter
        EXPECTED: * Filter contains options:
        EXPECTED: -Odds On
        EXPECTED: -Evens - 7/2
        EXPECTED: -4/1 - 15/2
        EXPECTED: -8/1 - 14/1
        EXPECTED: -16/1 - 28/1
        EXPECTED: -33/1 or Bigger
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"odds": "between selected values"} param
        """
        initial, final = 0, len(vec.bet_finder.ODDS_LIST)
        bet_filter_options = self.bet_filter.items_as_ordered_dict
        actual_odds_filters = list(bet_filter_options.keys())[:final]
        self.assertListEqual(actual_odds_filters, vec.bet_finder.ODDS_LIST,
                             msg=f'Actual Odds Filters: "{actual_odds_filters}" are not same as Expected Odds Filters : "{vec.bet_finder.ODDS_LIST}"')
        random_option = random.choice(actual_odds_filters)
        bet_filter_options[random_option].click()
        self.site.wait_splash_to_hide(timeout=5)
        self.assertTrue(bet_filter_options[random_option].is_selected(),
                        msg=f'Odds filter: "{random_option}" is not selected')

        expected_number_of_bets = self.get_number_of_bets(odds=[random_option])
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
            name='Number of bets to change', poll_interval=1,
            timeout=10)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{random_option}".'
                            f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(expected_number_of_bets)
        self.bet_filter.reset_link.click()

        # ---Verification of Form filters---
        expected_form_filters = [vec.bet_finder.COURSE_DISTANCE_WINNER, vec.bet_finder.COURSE_WINNER, vec.bet_finder.DISTANCE_WINNER, vec.bet_finder.WINNER_LAST_TIME,
                                 vec.bet_finder.WINNER_LAST_3_STARTS, vec.bet_finder.PLACED_LAST_TIME, vec.bet_finder.PLACED_LAST_3_STARTS]
        initial, final = final, final + len(expected_form_filters)
        bet_filter_options = self.bet_filter.items_as_ordered_dict
        actual_form_filters = list(bet_filter_options.keys())[initial:final]
        self.assertListEqual(actual_form_filters, expected_form_filters if self.brand == 'bma' else self.bet_filter.FORM,
                             msg=f'Actual Form Filters: "{actual_form_filters}" are not same as Expected Form Filters :'
                                 f' "{expected_form_filters if self.brand == "bma" else self.bet_filter.FORM}"')
        random_option = random.choice(actual_form_filters)
        bet_filter_options[random_option].click()
        self.assertTrue(bet_filter_options[random_option].is_selected(),
                        msg=f'Odds filter: "{random_option}" is not selected')

        expected_number_of_bets = self.get_number_of_bets(filters=[random_option])
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
            name='Number of bets to change', poll_interval=1,
            timeout=10)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{random_option}".'
                            f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(expected_number_of_bets)
        self.bet_filter.reset_link.click()

        # ---Verification of Going (Ground Type) filter---
        bet_filter_options = self.bet_filter.items_as_ordered_dict
        actual_proven_filter = list(bet_filter_options.keys())[final]
        self.assertEqual(actual_proven_filter, vec.bet_finder.PROVEN_GOING if self.brand == 'bma' else vec.bet_finder.PROVEN_GOING.upper(),
                         msg=f'Actual Proven Filter: "{actual_proven_filter}" are not same as Expected OddsFilters : '
                             f'"{vec.bet_finder.PROVEN_GOING if self.brand == "bma" else vec.bet_finder.PROVEN_GOING.upper()}"')
        bet_filter_options[vec.bet_finder.PROVEN_GOING if self.brand == 'bma' else vec.bet_finder.PROVEN_GOING.upper()].click()
        self.assertTrue(bet_filter_options[vec.bet_finder.PROVEN_GOING if self.brand == 'bma' else vec.bet_finder.PROVEN_GOING.upper()].is_selected(),
                        msg=f'Odds filter: "{vec.bet_finder.PROVEN_GOING if self.brand == "bma" else vec.bet_finder.PROVEN_GOING.upper()}" is not selected')

        expected_number_of_bets = self.get_number_of_bets(filters=[vec.bet_finder.PROVEN_GOING])
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
            name='Number of bets to change', poll_interval=1,
            timeout=10)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{random_option}".'
                            f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(expected_number_of_bets)
        self.bet_filter.reset_link.click()

        # ---Verification of Digital Tipster Filters---
        initial, final = final + 1, len(bet_filter_options.keys()) + 1
        bet_filter_options = self.bet_filter.items_as_ordered_dict
        actual_dtf_filters = list(bet_filter_options.keys())[initial:final]
        self.assertListEqual(actual_dtf_filters, vec.bet_finder.DTF,
                             msg=f'Actual Odds Filters: "{actual_dtf_filters}" are not same as Expected OddsFilters : "{vec.bet_finder.DTF}"')
        random_option = random.choice(actual_dtf_filters)
        bet_filter_options[random_option].click()
        self.assertTrue(bet_filter_options[random_option].is_selected(),
                        msg=f'Odds filter: "{random_option}" is not selected')

        expected_number_of_bets = self.get_number_of_bets(digital_tipster_filter=[random_option])
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
            name='Number of bets to change', poll_interval=1,
            timeout=10)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{random_option}".'
                            f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(expected_number_of_bets)
        self.bet_filter.reset_link.click()

    def test_005_verify_form_filter(self):
        """
        DESCRIPTION: Verify Form filter
        EXPECTED: * Filter contains options:
        EXPECTED: -Course and Distance Winner (long button, as compared to the rest Form buttons that are 1/2 of this)
        EXPECTED: -Course Winner
        EXPECTED: -Winner Last Time
        EXPECTED: -Placed Last Time
        EXPECTED: -Distance Winner
        EXPECTED: -Winner Within Last 3
        EXPECTED: -Placed Within Last 3
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"filters option (from above)": "Y"} param
        """
        # covered in step test_004

    def test_006_verify_going_ground_type_filter(self):
        """
        DESCRIPTION: Verify Going (Ground Type) filter
        EXPECTED: * Filter contains option: Proven
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"provenGoing": "Y"} param / {"provenGoing": "N"} param
        """
        # covered in step test_004

    def test_007_verify_digital_tipster_filters_filter(self):
        """
        DESCRIPTION: Verify Digital Tipster Filters filter
        EXPECTED: * Filter contains options:
        EXPECTED: -Selection
        EXPECTED: -Alternative
        EXPECTED: -Each-Way
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"supercomputerSelection": "S"} param / {"supercomputerSelection": "A"} param / {"supercomputerSelection": "E"} param
        """
        # covered in step test_004

    def test_008_verify_select_star_rating_filter(self):
        """
        DESCRIPTION: Verify Select Star Rating filter
        EXPECTED: * Filter contains options:
        EXPECTED: - 5 starts (unselected by default)
        EXPECTED: * Select several  selections ->  Proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: * Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"starRating": "number of selected stars"} param
        """
        star_rating_filter = self.bet_filter.stars_container
        self.assertTrue(star_rating_filter.is_displayed(),
                        msg=f'"{vec.bet_finder.SELECT_STAR_RATING}" is not displayed')
        self.bet_filter.set_stars_rating(rating=3)
        result = wait_for_result(lambda: self.site.horseracing_bet_filter.get_star_rating() == 3, timeout=10)
        self.assertTrue(result, msg=f'Actual stars are not same as Expetced stars: "3"')

        expected_number_of_bets = self.get_number_of_bets(star=str(3))
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
            name='Number of bets to change', poll_interval=1,
            timeout=10)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{3}".'
                            f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(expected_number_of_bets)
        self.bet_filter.reset_link.click()

    def test_009__select_any_options_from_several_filters_groups_and_tapclick__save_selection_button_refresh_page(self):
        """
        DESCRIPTION: * Select any options from several filters groups and tap/click  'Save selection' button
        DESCRIPTION: * Refresh page
        EXPECTED: All selected options are saved
        """
        selected_filters = []
        bet_filter_options = self.bet_filter.items_as_ordered_dict
        for item_name, item in list(bet_filter_options.items())[::4]:
            item.click()
            sleep(2)  # click operation to be reflected in FE (for LAD)
            if not self.site.horseracing_bet_filter.find_bets_button.is_enabled():
                item.click()
            else:
                selected_filters.append(item_name)
        self.bet_filter.save_selection_button.click()
        self.device.refresh_page()
        bet_filter_options = self.site.horseracing_bet_filter.items_as_ordered_dict
        for filter_name, filter_value in bet_filter_options.items():
            if filter_name in selected_filters:
                self.assertTrue(filter_value.is_selected(), msg=f'Filter: "{filter_name}" is not selected')

    def test_010_tapclick_find_bets_button_and_verify_results_page(self):
        """
        DESCRIPTION: Tap/click 'Find bets' button and verify results page
        EXPECTED: * Displayed selections match the filters parameters
        EXPECTED: * The following details are provided:
        EXPECTED: -Jockey
        EXPECTED: -Trainer
        EXPECTED: -Form
        EXPECTED: -Price
        EXPECTED: -Silks
        EXPECTED: -Time selection is running
        EXPECTED: -Runner Number
        EXPECTED: -Draw
        EXPECTED: * Filter 'Sort by TIME/ODDS' on the header (sorted 'by time' by default) sorts displayed selection either by time or odds
        """
        wait_for_result(lambda: self.site.horseracing_bet_filter.find_bets_button.is_enabled(), timeout=5)
        self.site.horseracing_bet_filter.find_bets_button.click()
        result = wait_for_result(lambda: self.site.racing_bet_filter_results_page.content_title_text == self.site.racing_bet_filter_results_page.TITLE
                                 if self.brand == 'bma' else self.site.racing_bet_filter_results_page.TITLE.title(), timeout=10)
        self.assertTrue(result, msg='Results page was not opened')

        time = self.site.racing_bet_filter_results_page.items[0].time.text
        for item in self.site.racing_bet_filter_results_page.items:
            horse_name = item.horse_name.text
            self._logger.info(msg=f'*** Verifying item with horse name "{horse_name}"')
            item.scroll_to_we()
            self.assertTrue(item.jockey_name.is_displayed(), msg='Failed to display jockey name')
            self.assertTrue(item.trainer_name.is_displayed(), msg='Failed to display trainer name')
            try:
                self.assertTrue(item.form.is_displayed())
            except AttributeError:
                self.assertTrue(self.get_formstring_value(horse_name=horse_name) == '',
                                msg=f'Failed to display the form for horse name "{horse_name}"')
            self.softAssert(self.assertTrue, item.has_silks, msg='Failed to display the silk')
            self.assertTrue(item.runner_number.is_displayed(), msg='Failed to display the number')
            self.assertTrue(item.horse_name.is_displayed(), msg='Failed to display the horse name')
            self.assertTrue(item.course.is_displayed(), msg='Failed to display the course')

            self.assertTrue(item.time.text >= time, msg=f'Items are not sorted by time.')
            time = item.time.text
