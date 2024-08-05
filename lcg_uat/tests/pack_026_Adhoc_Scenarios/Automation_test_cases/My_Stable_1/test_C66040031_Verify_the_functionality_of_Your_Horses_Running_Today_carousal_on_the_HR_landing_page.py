import pytest
from datetime import datetime, date
from crlat_cms_client.utils.date_time import get_date_time_as_string
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.my_stable
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C66040031_Verify_the_functionality_of_Your_Horses_Running_Today_carousal_on_the_HR_landing_page(BaseRacing):
    """
    TR_ID: C66040031
    NAME: Verify the functionality of 'Your Horses Running Today' carousal on the HR landing page.
    DESCRIPTION: This test case validates the display of horses bookmarked from today's races are displayed in the Horse racing landing page in the 'Your Horses Running Today' carousal.
    """
    keep_browser_open = True
    end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'

    def is_today_date(self, date_from_fe=None):
        date_obj = datetime.strptime(date_from_fe, '%d-%m-%Y %H:%M')
        today_date = date.today()
        return date_obj.date() == today_date

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS configurations
        TR_ID: C66040031
        NAME: Verify the functionality of 'Your Horses Running Today' carousal on the HR landing page
        """

        my_stable_status_in_cms = self.cms_config.get_my_stable_config().get('active')
        if not my_stable_status_in_cms:
            raise CmsClientException('My stable Page is not active in CMS')
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.assertTrue(events, f'UK and Irish Events are unavailable')
        self.__class__.event_id = next((event['event']['id'] for event in events if
                                        'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event'][
                                            'typeFlagCodes']))

    def test_001_login_to_the_application_and_navigate_to_the_horse_racing_landing_pageselect_or_bookmark_horses_from_multiple_events_which_are_for_the_current_day(self):
        """
        DESCRIPTION: Login to the application and navigate to the horse racing landing page.Select or bookmark horses from multiple events which are for the current day.
        EXPECTED: The user should be able to bookmark multiple horses and should be added successfully to the Stable.
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        if self.device_type == 'mobile' and self.site.wait_for_stream_and_bet_overlay(timeout=10):
            try:
                self.site.stream_and_bet_overlay.close_button.click()
            except:
                pass
        if self.device_type == 'mobile' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        if self.device_type == 'mobile' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.edit_stable.click()
        outcomes = self.site.racing_event_details.items_as_ordered_dict
        for horse_name, outcome in list(outcomes.items())[:4]:
            outcome.scroll_to_we()
            if outcome.is_bookmark_filled:
                continue
            outcome.fill_bookmark()

    def test_002_validate_the_details_of_the_horses_displayed_in_the_your_horses_running_today_carousal_in_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Validate the details of the horses displayed in the 'Your Horses Running Today' carousal in the horse racing landing page.
        EXPECTED: The number of horses bookmarked from today's events should be displayed in the 'Your Horses Running Today' carousal.
        EXPECTED: ![](index.php?/attachments/get/b6ffaac8-e11e-4d4d-bb01-637196262687)
        EXPECTED: ![](index.php?/attachments/get/e428dd72-7fb4-4dac-8b7e-5f0a65c0d32f)
        """
        self.navigate_to_page('my-stable')
        all_race_cards = self.site.my_stable.my_stable_race_cards
        for race_card in all_race_cards.values():
            race_card.scroll_to_we()
            race_card.expand()
        today_horses = [name.upper() for name, card in all_race_cards.items() if card.has_bet_button() and self.is_today_date(card.event_date)]
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")
        horses = wait_for_result(
            lambda: self.site.horse_racing.tab_content.accordions_list.your_horses_running_today.items_as_ordered_dict)
        your_horses_names = [name.upper() for name in horses]
        your_horses_names.sort()
        today_horses.sort()
        self.assertEqual(your_horses_names,today_horses, msg=f"actual horses {your_horses_names} are not equal to {today_horses}")

    def test_003_verify_that_if_a_user_un_bookmarks_any_of_the_horses_from_todays_event_it_should_not_display_in_the_your_horses_running_today_carousal(self):
        """
        DESCRIPTION: Verify that if a user un-bookmarks any of the horses from today's event it should not display in the 'Your Horses Running Today' carousal.
        EXPECTED: The un-bookmarked horse details should not be seen in the 'Your Horses Running Today' carousal.
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        if self.site.wait_for_stream_and_bet_overlay(timeout=10):
            self.site.stream_and_bet_overlay.close_button.click()
        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.site.racing_event_details.edit_stable.click()
        outcomes = self.site.racing_event_details.items_as_ordered_dict
        for horse_name, outcome in outcomes.items():
            if outcome.is_bookmark_filled:
                outcome.clear_bookmark()
                break
        self.test_002_validate_the_details_of_the_horses_displayed_in_the_your_horses_running_today_carousal_in_the_horse_racing_landing_page()

    def test_004_verify_that_a_horse_bookmarked_from_todays_event_gets_removed_from_the_your_horses_running_today_carousal_on_race_off_the_event(self):
        """
        DESCRIPTION: Verify that a horse bookmarked from today's event gets removed from the 'Your Horses Running Today' carousal on race off the event.
        EXPECTED: The horse details should be removed from the 'Your Horses Running Today' carousal when the event starts off (Race Off condition).
        """
        self.navigate_to_page('my-stable')
        self.site.my_stable.edit_stable.click()
        all_race_cards = self.site.my_stable.my_stable_race_cards
        for card_name, card in all_race_cards.items():
            card.clear_bookmark()
            wait_for_haul(2)
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state("HorseRacing")
        self.assertFalse(self.site.horse_racing.tab_content.accordions_list.has_your_horses_running_today(), msg=f"Your Horses Running Today is displaying after removing all the bookmarked horses")

    def test_005_verify_that_the_your_horses_running_today_carousal_is_not_displayed_in_the_front_end_when_there_are_no_bookmarked_horses_from_todays_events(self):
        """
        DESCRIPTION: Verify that the 'Your Horses Running Today' carousal is not displayed in the front end when there are no bookmarked horses from today's events.
        EXPECTED: The 'Your Horses Running Today' carousal should not be displayed when there are no bookmarked horses from today's races.
        EXPECTED: ![](index.php?/attachments/get/72573ddb-63d1-4860-97cc-940cc2d37bcd)
        EXPECTED: ![](index.php?/attachments/get/cc0224a2-9fca-4452-9d51-4bf080cccfbc)
        """
        #covered in above step

    def test_006_verify_that_the_your_horses_running_today_carousal_is_not_displayed_in_the_front_end_when_the_user_is_logged_out_on_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Verify that the 'Your Horses Running Today' carousal is not displayed in the front end when the user is logged out on the Horse racing landing page.
        EXPECTED: The 'Your Horses Running Today' carousal should not be displayed in the HR landing page when the user is logged out.
        """
        self.site.logout()
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")
        self.assertFalse(self.site.horse_racing.tab_content.accordions_list.has_your_horses_running_today(), msg=f"Your Horses Running Today is displaying after logout")