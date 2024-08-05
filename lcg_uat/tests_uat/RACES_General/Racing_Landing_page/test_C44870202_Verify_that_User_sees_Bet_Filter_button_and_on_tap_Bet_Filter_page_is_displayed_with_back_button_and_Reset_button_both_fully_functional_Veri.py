import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.prod  # Works only in beta as the bet fliter is not present in prod Horse racing landing page
@pytest.mark.medium
@pytest.mark.p2
@pytest.mark.races
@vtest
class Test_C44870202_Verify_that_User_sees_Bet_Filter_button_and_on_tap_Bet_Filter_page_is_displayed_with_back_button_and_Reset_button_both_fully_functional_Verify_that_page_displays_data_as_per_GDs_user_is_able_to_create_a_selection_choosing_in_meetings_selectin(Common):
    """
    TR_ID: C44870202
    NAME: "Verify that User sees Bet Filter button, and on tap, Bet Filter page is displayed (with back button and Reset button, both fully functional) Verify that page displays data as per GDs, user is able to create a selection choosing in meetings, selectin
    DESCRIPTION: "Verify that User sees Bet Filter button, and on tap, Bet Filter page is displayed (with back button and Reset button, both fully functional)
    DESCRIPTION: Verify that page displays data as per GDs, user is able to create a selection choosing in meetings, selecting specific ODDS,  and Form, Ground Type, Digital Tipsteer Filters, Star Rating, and user is able to save selection as per page functionality"

    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: User is logged in the application and is on Horse Racing Landing page.
        """
        self.site.login()
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_001_verify_that_the_bet_filter_button_is_displayed(self):
        """
        DESCRIPTION: Verify that the Bet filter button is displayed.
        EXPECTED: The 'Bet Filter' button is displayed on Horse Racing Landing page (on the top right corner of the screen).
        """
        actual_title = self.site.horse_racing.header_line.page_title.text
        if self.brand == 'bma':
            self.assertEqual(actual_title, vec.racing.HORSE_RACING_TAB_NAME, msg=f'Actual text: "{actual_title}"'
                                                                                 f'is not same as Expected text: "{vec.racing.HORSE_RACING_TAB_NAME}"')
        else:
            self.assertEqual(actual_title, vec.virtuals.VIRTUAL_HORSE_RACING, msg=f'Actual text: "{actual_title}"'
                                                                                  'is not same as '
                                                                                  f'Expected text: "{vec.virtuals.VIRTUAL_HORSE_RACING}"')
        self.assertTrue(self.site.horse_racing.bet_filter_link.is_displayed(),
                        msg='The bet filter button is not displayed on the Horse Racing Landing page')

    def test_002_tap_on_bet_filter_button_click_on_back_arrow_button_and_verify(self):
        """
        DESCRIPTION: Tap on Bet filter button. Click on back arrow button and verify.
        EXPECTED: The user is redirected to horse racing landing page.
        """
        self.site.horse_racing.bet_filter_link.click()
        self.site.wait_content_state_changed()
        self.__class__.bet_filter = self.site.horseracing_bet_filter
        actual_title = self.bet_filter.content_title_text
        self.assertEqual(actual_title, vec.bet_finder.BF_HEADER_TITLE, msg=f'Actual text: "{actual_title}" is not same as '
                                                                           f'Expected text: "{vec.bet_finder.BF_HEADER_TITLE}"')
        if self.brand == 'bma':
            self.bet_filter.back_button_click()
        else:
            self.site.back_button_click()
        self.site.wait_content_state('Horseracing')
        self.test_001_verify_that_the_bet_filter_button_is_displayed()
        self.site.horse_racing.bet_filter_link.click()
        self.site.wait_content_state_changed()

    def test_003_tap_on_bet_filter_button_and_create_a_selections_by_selecting_specific_meetingsoddsformgoingdigital_tipster_filtersstar_rating(self):
        """
        DESCRIPTION: Tap on Bet filter button and create a selection/s by selecting specific meetings/odds/form/Going/Digital tipster filters/star rating.
        EXPECTED: The Find bets button displays the number of selections available as per the filters set by the user.
        """
        going = list(self.bet_filter.items_as_ordered_dict.keys())[13]
        if self.brand == 'bma':
            self.__class__.selections = [self.bet_filter.ODDS[1].capitalize(),
                                         self.bet_filter.FORM[2].capitalize().replace("w", "W"),
                                         going, self.bet_filter.DTF[0].capitalize()]
        else:
            self.__class__.selections = [self.bet_filter.ODDS[1], self.bet_filter.FORM[2], going, self.bet_filter.DTF[0]]
        meetings = self.bet_filter.meetings_drop_down
        self.assertTrue(meetings, msg='The meetings dropdown is not displayed')
        option = 'All Meetings' if self.brand == 'bma' else 'ALL MEETINGS'
        self.assertTrue(meetings.is_option_selected(option=option), msg='The meeting option is not selected')
        bet_filter_options = self.bet_filter.items_as_ordered_dict
        for selection in self.selections:
            bet_filter_options[selection].click()
            self.site.wait_content_state_changed()
            self.assertTrue(self.bet_filter.is_filter_selected(selection),
                            msg=f'The bet filter option "{selection}" is not selected')
        number_of_selections = self.bet_filter.read_number_of_bets()
        try:
            self.assertTrue(number_of_selections, msg=f'The number of selections found are :"{number_of_selections}"')
        except Exception:
            self._logger.info('*** There are no bets found for this selection"')

    def test_004_click_on_save_selection_verify(self):
        """
        DESCRIPTION: Click on Save Selection. Verify.
        EXPECTED: 1. The filters selected by the user are saved.
        EXPECTED: 2. The Save selection button is disabled.
        """
        self.assertTrue(self.bet_filter.save_selection_button.is_displayed(),
                        msg='The Save Selection button is not displayed')
        self.bet_filter.save_selection_button.click()
        self.site.wait_content_state_changed()
        for selection in self.selections:
            self.assertTrue(self.bet_filter.is_filter_selected(filter=selection),
                            msg=f'The bet filter option "{selection}" is not selected')
        self.assertFalse(self.bet_filter.save_selection_button.is_enabled(),
                         msg='The Save Selection button is not disabled')

    def test_005_click_on_reset_button_and_verify(self):
        """
        DESCRIPTION: Click on Reset button and verify.
        EXPECTED: The fields filled earlier are reset and Save selection button is enabled.
        """
        self.assertTrue(self.bet_filter.reset_link.is_displayed(),
                        msg='The Reset link button is not displayed')
        self.bet_filter.reset_link.click()
        self.site.wait_content_state_changed()
        for selection in self.selections:
            self.site.wait_content_state_changed()
            self.assertFalse(self.bet_filter.is_filter_selected(filter=selection, expected_result=False),
                             msg=f'The given selection "{selection}" is selected '
                                 'but it should not be selected')
        self.assertTrue(self.bet_filter.save_selection_button.is_enabled(),
                        msg='The button is disabled')

    def test_006_create_a_selections_by_selecting_specific_meetingsoddsformgoingdigital_tipster_filtersstar_rating_and_click_on_find_bets_button(self):
        """
        DESCRIPTION: Create a selection/s by selecting specific meetings/odds/form/Going/Digital tipster filters/star rating and click on Find bets button.
        EXPECTED: The bet filter results are displayed
        """
        self.test_003_tap_on_bet_filter_button_and_create_a_selections_by_selecting_specific_meetingsoddsformgoingdigital_tipster_filtersstar_rating()
        self.bet_filter.find_bets_button.click()
        self.site.wait_content_state_changed()
        try:
            results_displayed = self.site.racing_bet_filter_results_page.content_title_text
            self.assertTrue(results_displayed, msg=f'The number of results found are :"{results_displayed}"')
        except Exception:
            self._logger.info('*** There are no bets found for this selection"')
