from datetime import datetime, date, timedelta
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.my_stable
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C66040522_Verify_the_functionality_on_the_My_Stable_page(Common):
    """
    TR_ID: C66040522
    NAME: Verify the functionality on the My Stable page.
    DESCRIPTION: This test case validates the details and options present on the My Stable page:
    DESCRIPTION: 1. Display of bookmarked horses and details.
    DESCRIPTION: 2. View Notes option.
    DESCRIPTION: 3. Hide Notes option.
    DESCRIPTION: 4. Add Notes option.
    DESCRIPTION: 5. Edit Notes option.
    DESCRIPTION: 6. Sort By option.
    """
    keep_browser_open = True
    end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'

    def is_today_date(self, date_from_fe=None):
        date_obj = datetime.strptime(date_from_fe, '%d-%m-%Y %H:%M') - timedelta(hours=4, minutes=30)
        today_date = date.today()
        return date_obj.date() == today_date

    def check_running_today_and_my_horses(self, all_race_cards):
        for card_name, card in all_race_cards.items():
            card.scroll_to_we()
            card.expand()
        expected_running_today = {'name': 'RUNNING TODAY',
                                  'count': sum([1 for card in all_race_cards.values() if card.has_bet_button() and self.is_today_date(card.event_date)])}
        expected_my_horses = {'name': 'MY HORSES', 'count': len(all_race_cards)}
        self.assertEqual(expected_my_horses, self.site.my_stable.my_horses,
                         f'Actual "My Horses": "{self.site.my_stable.my_horses}" is not same as '
                         f'Expected "My Horses": "{expected_my_horses}"')

        self.assertEqual(expected_running_today, self.site.my_stable.running_today,
                         f'Actual "RUNNING TODAY": "{self.site.my_stable.running_today}" is not same as '
                         f'Expected "RUNNING TODAY": "{expected_running_today}"')

    def book_mark_horses_by_event_id(self, event_id, non_runner=False):
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')

        if self.site.wait_for_stream_and_bet_overlay(timeout=10):
            overlay = self.site.stream_and_bet_overlay
            if overlay and overlay.is_displayed():
                overlay.close_button.click()

        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

        self.site.racing_event_details.edit_stable.click()

        outcomes = self.site.racing_event_details.items_as_ordered_dict

        if non_runner:
            non_runner_horse_name, outcome = next(((horse_name, outcome) for horse_name, outcome in outcomes.items() if outcome.is_non_runner))
            outcome.fill_bookmark()
            self.bookmarked_horses.append(non_runner_horse_name.upper())
            return

        for horse_name, outcome in outcomes.items():
            bookmark_status = outcome.has_my_stable_bookmark()
            if horse_name in [vec.racing.UNNAMED_FAVORITE, vec.racing.UNNAMED_FAVORITE_2ND]:
                self.assertFalse(bookmark_status, f'"{horse_name}" has my stable bookmark')
            else:
                self.assertTrue(bookmark_status, f'"my stable bookmark is not displayed for{horse_name}" ')

        for horse_name, outcome in list(outcomes.items())[:3]:
            if horse_name in ['Unnamed Favourite', 'Unnamed 2nd Favourite'] or outcome.is_bookmark_filled:
                continue
            outcome.fill_bookmark()
            self.bookmarked_horses.append(horse_name.upper())

    def bookmarking_non_runner_and_checking_the_behaviour_of_stable_page(self):
        self.__class__.start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        self.__class__.end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        event_id = None
        for event in events:
            if 'UK' in event['event']['typeFlagCodes']:
                event = self.ss_req.ss_event_to_outcome_for_event(event_id=event['event']['id'])[0]
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == '|Win or Each Way|' and market['market'].get(
                            'children'):
                        for outcome in market['market']['children']:
                            if 'N/R' in outcome.get('outcome').get('name') and outcome.get('outcome').get(
                                    'isResulted') and outcome.get('outcome').get('isFinished') and outcome.get(
                                    'outcome').get(
                                    'outcomeStatusCode') == 'S':
                                event_id = event['event']['id']
                                break

        if not event_id:
            return False
        my_horses_before_non_runner_bookmark = self.site.my_stable.my_horses.get('count')
        today_running_before_non_runner_bookmark = self.site.my_stable.running_today.get('count')
        self.book_mark_horses_by_event_id(event_id=event_id, non_runner=True)
        self.navigate_to_page('my-stable')
        my_horses_after_non_runner_bookmark = self.site.my_stable.my_horses.get('count')
        today_running_after_non_runner_bookmark = self.site.my_stable.running_today.get('count')
        self.assertEqual(my_horses_after_non_runner_bookmark, my_horses_before_non_runner_bookmark + 1,
                         f'Actual My Horses Count : "{my_horses_after_non_runner_bookmark}" is not same as '
                         f'Expected My Horses Count : "{my_horses_before_non_runner_bookmark + 1}"')
        self.assertEqual(today_running_after_non_runner_bookmark, today_running_before_non_runner_bookmark,
                         f'Actual Today Running Count : "{today_running_after_non_runner_bookmark}" is not same as '
                         f'Expected Today Running Count : "{today_running_before_non_runner_bookmark}"')
        return True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS configurations
        PRECONDITIONS: My Stable Menu item
        PRECONDITIONS: My Stable Configurations
        PRECONDITIONS: Checkbox against ‘Active Mystable’ - Should be checked in
        PRECONDITIONS: Checkbox against ‘Mystable Horses Running Today Carousel’ - Should be checked in
        PRECONDITIONS: Checkbox against ‘Active Antepost’ - Should be checked in
        PRECONDITIONS: Checkbox against ‘Active My Bets’ (Phase 2)
        PRECONDITIONS: My Stable Entry Point
        PRECONDITIONS: Entry Point SVG Icon - (Mystable-Entry-Point-White)
        PRECONDITIONS: Entry Point Label  - Ladbrokes (Stable Mates)/ Coral (My Stable)
        PRECONDITIONS: Edit Or Save My Stable
        PRECONDITIONS: Edit Stable Svg Icon - (Mystable-Entry-Point-Dark)
        PRECONDITIONS: Edit Stable Label - (Edit Stable)
        PRECONDITIONS: Save Stable Svg Icon - ( Mystable-Entry-Point-White)
        PRECONDITIONS: Save Stable Label -(Done)
        PRECONDITIONS: Edit Note Svg Icon - (Mystable-Edit-Note)
        PRECONDITIONS: Bookmark Svg Icon -(bookmarkfill)
        PRECONDITIONS: InProgress Bookmark Svg icon -(Mystable-Inprogress-Bookmark)
        PRECONDITIONS: Unbookmark Svg Icon -(bookmark)
        PRECONDITIONS: Empty My Stable
        PRECONDITIONS: Empty Stable Sag Icon - Mystable-Stable-Signposting
        PRECONDITIONS: Empty Stable Header Label - Empty Stable
        PRECONDITIONS: Empty Stable Message Label - Tap on ‘Edit Stable’ on the Race Card to add a horse
        PRECONDITIONS: Empty Stable CTA Label - View my horses
        PRECONDITIONS: My Stable Signposting
        PRECONDITIONS: Signposting Svg Icon - Mystable-Stable-Signposting
        PRECONDITIONS: Notes Signposting Svg Icon-Mystable-Note-Signposting
        PRECONDITIONS: Your Horses Running Today Carousel
        PRECONDITIONS: Carousel Icon - Mystable-Entry-Point-Dark
        PRECONDITIONS: Carousel Name - Your horses running today!
        PRECONDITIONS: Error Message Popups
        PRECONDITIONS: Maximum Horses Exceed Message - Maximum number of  selections reached. To add more, remove horses from your stable.
        """
        my_stable_status_in_cms = self.cms_config.get_my_stable_config().get('active')
        if not my_stable_status_in_cms:
            raise CmsClientException('My stable Page is not active in CMS')

        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id, all_available_events=True)
        self.assertTrue(events, f'UK and Irish Events are unavailable')
        self.__class__.event_id1 = next((event['event']['id'] for event in events if 'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event']['typeFlagCodes']))
        self.__class__.event_id2 = next((event['event']['id'] for event in events if 'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event']['typeFlagCodes'] if event['event']['id'] != self.event_id1))

        self.__class__.start_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        self.__class__.end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id, all_available_events=True)
        self.__class__.event_id3 = next((event['event']['id'] for event in events if 'UK' in event['event']['typeFlagCodes']), None)

    def test_001_login_to_the_application_and_navigate_to_the_my_stable_page_by_clicking_the_entry_points_on_the_horse_racing_landing_page_or_the_event_details_pageindexphpattachmentsget45bd1efe_a499_4fb2_ac62_e971f4bb8523indexphpattachmentsgetdee70b96_ee5c_44f2_9615_226974110062(
            self):
        """
        DESCRIPTION: Login to the application and navigate to the My Stable page by clicking the entry points on the horse racing landing page or the event details page.
        EXPECTED: User should be able to navigate to the My Stable page successfully.
        """
        self.site.login()

        self.navigate_to_page('my-stable')
        self.__class__.bookmarked_horses = [name.upper() for name in self.site.my_stable.my_stable_race_cards.keys()] if not self.site.my_stable.has_view_todays_races() else []

        self.book_mark_horses_by_event_id(event_id=self.event_id1)
        self.book_mark_horses_by_event_id(event_id=self.event_id2)
        self.book_mark_horses_by_event_id(event_id=self.event_id3)

    def test_002_verify_the_details_displayed_on_the_my_stable_page(self):
        """
        DESCRIPTION: Verify the details displayed on the My Stable page.
        EXPECTED: The following details should be displayed in the My Stable page.
        EXPECTED: 1. The details of all the bookmarked horses should be displayed on the page. Various details like the name of the meeting, time of the event, odds etc should be displayed.
        EXPECTED: 2. The total number of horses bookmarked and the number of horses running on the current day events should be displayed on the top.
        EXPECTED: 3. The Edit Stable option should be available for the user to un-bookmark any of the selected horses from the My Stable page.
        """
        self.site.racing_event_details.my_stable_link.click()
        self.site.wait_content_state('my-stable')

        # expectation 1
        all_race_cards = self.site.my_stable.my_stable_race_cards
        self.assertEqual(sorted(self.bookmarked_horses), sorted([name.upper() for name in all_race_cards.keys()]),
                         f'Bookmarked Horses are not equal. '
                         f'Horses in My stable Page : "{sorted(list(all_race_cards.keys()))}"'
                         f'Not same as Bookmarked horses : "{sorted(self.bookmarked_horses)}"')

        # expectation 2 and test_003
        self.check_running_today_and_my_horses(all_race_cards=all_race_cards)

        # expectation 3
        status_of_edit_stable = wait_for_result(lambda: self.site.my_stable.edit_stable is not None,
                                                bypass_exceptions=(NoSuchElementException,
                                                                   StaleElementReferenceException, VoltronException))
        self.assertTrue(status_of_edit_stable, f'"Edit Stable" is not displayed')

        # 003
        card_name, card = next(iter(all_race_cards.items()))
        self.site.my_stable.edit_stable.click()
        card.clear_bookmark()

        try:
            race_cards = self.site.my_stable.my_stable_race_cards
            self.assertNotIn(card_name, list(race_cards.keys()), f'Horse : {card_name} is not un-bookmarked')
            self.check_running_today_and_my_horses(all_race_cards=race_cards)
        except:
            wait_for_haul(2)
            race_cards = self.site.my_stable.my_stable_race_cards
            self.assertNotIn(card_name, list(race_cards.keys()), f'Horse : {card_name} is not un-bookmarked')
            self.check_running_today_and_my_horses(all_race_cards=race_cards)

        # tes_004
        sp_found = False
        for card_name, card in race_cards.items():
            card.expand()
            if card.has_bet_button():
                if not sp_found:
                    sp_found = not card.has_bet_button() or card.bet_button.name == 'SP'
                    continue
                self.assertTrue(not card.has_bet_button() or card.bet_button.name == 'SP', f'Actual ODD Value : "{card.bet_button.name} is not same as '
                                                              f'"Expected ODD Value : "SP" for {card_name}')

    def test_003_verify_that_the_number_of_total_horses_horses_bookmarked_and_horses_running_today_are_displayed_on_top_of_the_page(
            self):
        """
        DESCRIPTION: Verify that the number of total horses horses bookmarked and horses running today are displayed on top of the page.
        EXPECTED: The total number of bookmarked horses should be displayed against 'MY HORSES' and the count of horses running today should be displayed against 'RUNNING TODAY'.
        EXPECTED: The details of the total horses &amp; horses running today should get updated accordingly when any horse is un-bookmarked and when the current day events are completed so the count against 'Running Today' gets updated.
        """
        # covering in above step

    def test_004_verify_the_display_order_of_the_bookmarked_horses_in_my_stable_page(self):
        """
        DESCRIPTION: Verify the display order of the bookmarked horses in My Stable page.
        EXPECTED: First the horses which are participating in the race that is going to start first from the current time should be displayed on top. Next the horse which is participating  in the next races should follow based on the time of the event.
        EXPECTED: The Horses with live prices show up on top of the list based upon the event time with open accordions.
        EXPECTED: Next the horses which do not have live prices or from resulted races display with closed accordions.
        """
        # covered in above steps

    def test_005_verify_the_functionality_of_view_notes_option(self):
        """
        DESCRIPTION: Verify the functionality of 'View Notes' option.
        EXPECTED: By clicking on this option user should be able to view the notes which were entered by the user on the EDP against that specific horse.
        """
        # covering in test_007

    def test_006_verify_the_functionality_of_hide_notes_option(self):
        """
        DESCRIPTION: Verify the functionality of 'Hide Notes' option.
        EXPECTED: The notes should collapse and user should not be able to view the notes added.
        """
        # covering in test_007

    def test_007_verify_that_user_is_able_to_add_notes_for_horses_against_which_notes_were_not_added_from_the_event_details_page(
            self):
        """
        DESCRIPTION: Verify that user is able to add notes for horses against which notes were not added from the event details page.
        EXPECTED: The user should be able to add notes against the horses from the My Stable page as well and save it.
        EXPECTED: The notes added against the horse on the My Stable page should be displayed on the events details page.
        """
        all_race_cards = self.site.my_stable.my_stable_race_cards
        card_name, card = next(iter(all_race_cards.items()))

        # verifying "ADD NOTES"
        add_notes_status = card.add_notes_button.name.upper() == vec.sb.ADD_NOTES
        self.assertTrue(add_notes_status, f'"{vec.sb.ADD_NOTES}" is not displayed on {card_name}')

        card.add_notes_button.click()
        card.notes.input_notes.value = 'MY NOTES'
        card.notes.save.click()

        # verifying "HIDE NOTES"
        hide_notes_status = card.hide_notes_button.name.upper() == vec.sb.HIDE_NOTES
        self.assertTrue(hide_notes_status, f'"{vec.sb.HIDE_NOTES}" is not displayed on {card_name}')

        self.assertTrue(card.edit_notes_button, f'EDIT NOTES Icon is not displayed')
        self.assertEqual(card.existing_notes, 'MY NOTES', f'NOTES are not equal')

        # verifying editing notes
        edited_text = "EDITED TEXT"
        card.edit_notes_button.click()
        card.notes.input_notes.value = edited_text
        card.notes.save.click()
        wait_for_haul(1)
        self.assertEqual(card.existing_notes, edited_text, f'TEXT IS NOT UPDATED AFTER NOTES ADDED')

        # verifying "VIEW NOTES"
        card.hide_notes_button.click()
        your_notes_status = wait_for_result(lambda: card.hide_notes_button.name.upper() == vec.sb.VIEW_NOTES)
        self.assertTrue(your_notes_status, f'"{vec.sb.VIEW_NOTES}" is not displayed on {card_name}')

    def test_008_verify_that_the_user_is_able_to_edit_the_existing_notes_against_the_horses_by_clicking_the_edit_icon_present_in_the_right_side_of_the_section(
            self):
        """
        DESCRIPTION: Verify that the user is able to edit the existing notes against the horses by clicking the edit icon present in the right side of the section.
        EXPECTED: The user should be able to edit the existing notes against the horses and update it.
        EXPECTED: The updated notes should be successfully saved and displayed on the My Stable page and the EDP.
        """
        # covered in 007

    def test_009_verify_the_sort_by_functionality_available_on_the_my_stable_pageindexphpattachmentsget98f9644f_82b7_406e_8c6b_8ddd0f161fc5(
            self):
        """
        DESCRIPTION: Verify the sort by functionality available on the My Stable page.
        EXPECTED: The user will have an option to sort the data on the My Stable page.
        EXPECTED: By default the A-Z option is selected and data is sorted accordingly. This sort option is applicable only for horses which do not have live prices.
        EXPECTED: Recently added sort option sorts the horses by the recently added horse on the top.
        """
        # verifying sort by functionality
        sort_by = self.site.my_stable.sort_by
        self.assertEqual(sort_by.selected_option, vec.sb.AZ,
                         f'A-Z option is not selected by default. Actual Selected option : "{sort_by.selected_option}"')
        sort_by.click()
        dropdown = sort_by.drop_down
        self.assertTrue(dropdown, f'dropdown is not displayed on my-stable page')

        wait_for_result(lambda: self.site.my_stable.sort_by.drop_down.items_as_ordered_dict.get(vec.sb.RECENTLY_ADDED))
        self.site.my_stable.sort_by.drop_down.items_as_ordered_dict.get(vec.sb.RECENTLY_ADDED).click()
        wait_for_result(lambda: self.site.my_stable.sort_by.selected_option.upper() == vec.sb.RECENTLY_ADDED.upper())
        self.assertEqual(sort_by.selected_option.upper(), vec.sb.RECENTLY_ADDED.upper(), f'"{vec.sb.RECENTLY_ADDED}" option is not selected')

        # checkpoint --> Sort - SP selections / non runners / resulted horses and Priced horses - should be sorted in increasing order of race time
        recently_added_horses_order = []
        race_cards = self.site.my_stable.my_stable_race_cards
        for name, card in race_cards.items():
            card.expand()
            if not card.has_bet_button() or card.bet_button.name == 'SP':
                recently_added_horses_order.append(name)

        # checking live price cards order
        live_price_cards = [card for card in race_cards.values() if card.has_bet_button() and card.bet_button.name != 'SP']
        is_live_price_odd_cards_sorted_by_event_start_time = lambda l: all(l[i].event_date <= l[i + 1].event_date for i in range(len(live_price_cards) - 1))
        self.assertTrue(is_live_price_odd_cards_sorted_by_event_start_time, f'Horses(which have LP odds) are not Sorted based on event start time')

        sort_by.click()
        wait_for_result(lambda: self.site.my_stable.sort_by.drop_down.items_as_ordered_dict.get(vec.sb.AZ))
        self.site.my_stable.sort_by.drop_down.items_as_ordered_dict.get(vec.sb.AZ).click()
        wait_for_result(lambda: self.site.my_stable.sort_by.selected_option.upper() == vec.sb.AZ.upper())
        self.assertEqual(sort_by.selected_option.upper(), vec.sb.AZ.upper(),
                         f'"{vec.sb.AZ}" option is not selected')

        actual_order_after_selected_az_option = []
        for name, card in self.site.my_stable.my_stable_race_cards.items():
            card.expand()
            if not card.has_bet_button() or card.bet_button.name == 'SP':
                actual_order_after_selected_az_option.append(name)
        self.assertListEqual(actual_order_after_selected_az_option, sorted(recently_added_horses_order),
                             f'Cards are not sorted after clicking selecting A-Z. Actual Order is "{actual_order_after_selected_az_option}"'
                             f'  Expected order is "{sorted(recently_added_horses_order)}"')

        sort_by.click()
        wait_for_result(lambda: self.site.my_stable.sort_by.drop_down.items_as_ordered_dict.get(vec.sb.RECENTLY_ADDED))
        self.site.my_stable.sort_by.drop_down.items_as_ordered_dict.get(vec.sb.RECENTLY_ADDED).click()
        wait_for_result(lambda: self.site.my_stable.sort_by.selected_option.upper() == vec.sb.RECENTLY_ADDED.upper())
        self.assertEqual(sort_by.selected_option.upper(), vec.sb.RECENTLY_ADDED.upper(),
                         f'"{vec.sb.RECENTLY_ADDED}" option is not selected')

        actual_order_reselected_recently_added_option = []
        for name, card in self.site.my_stable.my_stable_race_cards.items():
            card.expand()
            if not card.has_bet_button() or card.bet_button.name == 'SP':
                actual_order_reselected_recently_added_option.append(name)
        self.assertEqual(actual_order_reselected_recently_added_option, recently_added_horses_order, f'Actual Order : "{actual_order_reselected_recently_added_option}" not same '
                                                                                                     f'Expected Order : "{recently_added_horses_order}"')
        success = self.bookmarking_non_runner_and_checking_the_behaviour_of_stable_page()
        if not success:
            self._logger.info('not successfully checked. Reason :unable to get event which have non-runner')
        else:
            self._logger.info('Successfully Completed the bookmarking_non_runner_and_checking_the_behaviour_of_stable_page')
            self.site.my_stable.edit_stable.click()

    def test_010_verify_that_the_user_is_able_to_expand_and_collapse_the_accordions_against_various_horses_available_on_the_my_stable_screen(
            self):
        """
        DESCRIPTION: Verify that the user is able to expand and collapse the accordions against various horses available on the My Stable screen.
        EXPECTED: The user should be able to expand and see the details of the horses by clicking on the accordions present against them.
        EXPECTED: The user should be able to collapse the expanded section of the horse by clicking on the accordion.
        """
        for name, card in self.site.my_stable.my_stable_race_cards.items():
            if not card.is_expanded():
                card.expand()
                self.assertTrue(card.is_expanded(), f'unable to expand the race card : "{name}"')
                card.collapse()
                self.assertFalse(card.is_expanded(), f'unable to collapse the race card : "{name}"')
            else:
                card.collapse()
                self.assertFalse(card.is_expanded(), f'unable to collapse the race card : "{name}"')
                card.expand()
                self.assertTrue(card.is_expanded(), f'unable to expand the race card : "{name}"')
            card.clear_bookmark()

