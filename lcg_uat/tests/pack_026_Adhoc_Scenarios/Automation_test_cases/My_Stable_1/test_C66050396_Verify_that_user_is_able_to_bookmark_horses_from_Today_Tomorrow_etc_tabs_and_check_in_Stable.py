import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
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
@pytest.mark.timeout(900)
@vtest
class Test_C66050396_Verify_that_user_is_able_to_bookmark_horses_from_Today_Tomorrow_etc_tabs_and_check_in_Stable(BaseRacing):
    """
    TR_ID: C66050396
    NAME: Verify that user is able to bookmark horses from Today/Tomorrow etc. tabs and check in Stable.
    DESCRIPTION: This test case validates the functionality of bookmarking horses from the Today's, Tomorrow's and Day after tabs and checking if they are successfully added to the Stable.
    """
    keep_browser_open = True
    bookmarked_horses = []
    enable_bs_performance_log = True

    def un_book_mark_the_horses(self, current_page_my_stable=False):
        def clear(edit_stable_enabled=False):
            if not self.site.my_stable.has_no_favorite_horses_icon():
                if not edit_stable_enabled:
                    self.site.my_stable.edit_stable.click()
                cards = self.site.my_stable.my_stable_race_cards
                for card in cards.values():
                    card.clear_bookmark()
                    wait_for_haul(0.2)

        if not current_page_my_stable:
            self.navigate_to_page('my-stable')
        clear()
        if not self.site.my_stable.has_no_favorite_horses_icon():
            clear(edit_stable_enabled=True)

    def book_mark_the_horses_and_verify_signposting(self, ss_event=None, number_of_horses=3):
        if ss_event:
            drill_down_tag_names = ss_event['event']["drilldownTagNames"]
            stream_and_bet_status = self.device_type == 'mobile' and "EVFLAG_IHR" in drill_down_tag_names and "EVFLAG_RVA" not in drill_down_tag_names and "EVFLAG_PVM" not in drill_down_tag_names and "EVFLAG_PVA" not in drill_down_tag_names
        else:
            stream_and_bet_status = True
        if stream_and_bet_status and self.site.wait_for_stream_and_bet_overlay(timeout=10):
            overlay = self.site.stream_and_bet_overlay
            if overlay and overlay.is_displayed():
                overlay.close_button.click()
        if self.device_type == 'mobile' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        if self.device_type == 'mobile' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.edit_stable.click()
        outcomes = self.site.racing_event_details.items_as_ordered_dict

        for horse_name, outcome in outcomes.items():
            outcome.scroll_to_we()
            bookmark_status = outcome.has_my_stable_bookmark()
            if horse_name in [vec.racing.UNNAMED_FAVORITE, vec.racing.UNNAMED_FAVORITE_2ND]:
                self.assertFalse(bookmark_status, f'"{horse_name}" has my stable bookmark')
            else:
                self.assertTrue(bookmark_status, f'my stable bookmark is not displayed for "{horse_name}"')
        for horse_name, outcome in list(outcomes.items())[:number_of_horses]:
            if horse_name in ['Unnamed Favourite', 'Unnamed 2nd Favourite']:
                continue
            outcome.fill_bookmark(notes='BM-Notes')
            self.assertTrue(outcome.has_my_stable_sign_posting(), f'My Stable Sign Posting is not displayed')
            self.assertTrue(outcome.has_my_stable_notes_sign_posting(),
                            f'My Stable Notes Sign Posting is not displayed')
            if horse_name.upper() not in self.bookmarked_horses:
                self.bookmarked_horses.append(horse_name.upper())

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS configurations
        PRECONDITIONS: My Stable Menu item
        PRECONDITIONS: My Stable Configurations
        PRECONDITIONS: Checkbox against �Active Mystable� - Should be checked in
        PRECONDITIONS: Checkbox against �Mystable Horses Running Today Carousel� - Should be checked in
        PRECONDITIONS: Checkbox against �Active Antepost� - Should be checked in
        PRECONDITIONS: Checkbox against �Active My Bets� (Phase 2)
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
        PRECONDITIONS: Empty Stable Message Label - Tap on �Edit Stable� on the Race Card to add a horse
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

        self.__class__.end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.__class__.today_event = next(
            (event for event in events if 'UK' in event['event']['typeFlagCodes']), None)

        self.__class__.start_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        self.__class__.end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.__class__.tomorrow_event = next(
            (event for event in events if 'UK' in event['event']['typeFlagCodes']), None)

    def test_001_login_to_the_application_and_navigate_to_the_horse_racing_landing_pagefrom_the_todays_tab_select_an_event_from_the_uk_and_irish_meetingsclick_on_the_edit_stable_optionverify_that_user_is_able_to_bookmark_the_horses_from_the_todays_event_and_add_notesindexphpattachmentsget7dcb7fc8_4a52_472d_896a_4e592de8b134_indexphpattachmentsgetce87e716_1caf_4793_ae01_f78da221832a(
            self):
        """
        DESCRIPTION: Login to the application and navigate to the Horse racing landing page.From the Today's tab select an event from the UK and Irish meetings.Click on the 'Edit Stable' option.Verify that user is able to bookmark the horses from the today's event and add notes.
        DESCRIPTION: ![](index.php?/attachments/get/7dcb7fc8-4a52-472d-896a-4e592de8b134) ![](index.php?/attachments/get/ce87e716-1caf-4793-ae01-f78da221832a)
        EXPECTED: User should be able to bookmark and add notes against various horses from today's event.
        EXPECTED: User should be able to view the bookmark and notes signposting.
        EXPECTED: The bookmarked horses should be added to the Stable.
        """
        self.site.login()
        self.un_book_mark_the_horses()
        self.navigate_to_edp(event_id=self.today_event['event']['id'], sport_name='horse-racing')
        self.book_mark_the_horses_and_verify_signposting(ss_event=self.today_event, number_of_horses=2)

    def test_002_navigate_to_the_tomorrows_tab_in_the_horse_racing_landing_pageselect_a_horse_racing_event_from_tomorrow_under_the_uk_amp_irish_racesin_the_event_details_page_try_to_bookmark_and_add_notes_by_selecting_the_edit_stable_optionindexphpattachmentsget8f51571f_45f5_493a_b1d9_b3586b8171a1_indexphpattachmentsget5ab4dd80_bbc2_4b11_a34a_74be0d4bdc58(
            self):
        """
        DESCRIPTION: Navigate to the Tomorrow's tab in the Horse racing landing page.Select a horse racing event from tomorrow under the UK &amp; Irish races.In the event details page try to bookmark and add notes by selecting the 'Edit Stable' option.
        DESCRIPTION: ![](index.php?/attachments/get/8f51571f-45f5-493a-b1d9-b3586b8171a1) ![](index.php?/attachments/get/5ab4dd80-bbc2-4b11-a34a-74be0d4bdc58)
        EXPECTED: User should be able to bookmark and add notes against various horses from tomorrow's event.
        EXPECTED: User should be able to view the bookmark and notes signposting.
        EXPECTED: The bookmarked horses should be added to the Stable.
        """
        self.navigate_to_edp(event_id=self.tomorrow_event['event']['id'], sport_name='horse-racing')
        self.book_mark_the_horses_and_verify_signposting(ss_event=self.today_event,number_of_horses=2)

    def test_003_select_the_overlay_from_the_event_details_pageselect_an_event_from_the_uk_amp_irish_meetings_which_is_scheduled_2_days_after_the_current_date_sundaymonday_etc_in_the_events_details_page_select_the_edit_stable_option_and_try_to_bookmark_and_add_the_notes_against_the_horse_and_click_on_the_done_button_to_save_the_notes(self, test_004=False, **kwargs):
        """
        DESCRIPTION: Select the overlay from the event details page.Select an event from the UK &amp; Irish meetings which is scheduled 2 days after the current date. (Sunday,Monday etc.). In the events details page select the 'Edit Stable' option and try to bookmark and add the notes against the horse and click on the 'Done' button to save the notes.
        DESCRIPTION: ![](index.php?/attachments/get/46cf6bc2-055b-4fd2-8248-cb7696eb3fe4) ![](index.php?/attachments/get/578686c6-ba0d-4e7b-b590-b6e2a8f7ad29)
        EXPECTED: User should be able to bookmark and add notes against various horses from events which are scheduled two days after the current date.
        EXPECTED: User should be able to view the bookmark and notes signposting.
        EXPECTED: The bookmarked horses should be added to the Stable.
        """
        self.site.racing_event_details.meeting_selector.click()
        if kwargs.get('today') or kwargs.get('tomorrow'):
            date_tab_name, date_tab = next(([tab_name, tab] for tab_name, tab in
                                            self.site.racing_event_details.meetings_list.date_tab.items_as_ordered_dict.items()
                                            if (kwargs.get('today') and tab_name.upper() == vec.sb.SPORT_DAY_TABS.today.upper()) or (kwargs.get('tomorrow') and tab_name.upper() == vec.sb.SPORT_DAY_TABS.tomorrow.upper())),
                                           [None, None])
        else:
            date_tab_name, date_tab = next(([tab_name, tab] for tab_name, tab in
                                            self.site.racing_event_details.meetings_list.date_tab.items_as_ordered_dict.items()
                                            if tab_name.upper() not in [vec.sb.SPORT_DAY_TABS.tomorrow.upper(),
                                                                        vec.sb.SPORT_DAY_TABS.today.upper()]), [None, None])
        date_tab.click()
        meetings_list = self.site.racing_event_details.meetings_list.get_items(name=self.uk_and_ire_type_name)
        uk_and_irish = meetings_list.get(self.uk_and_ire_type_name) if self.uk_and_ire_type_name in meetings_list else meetings_list.get('UK / IRELAND RACES')
        if not uk_and_irish:
            self._logger.info(f'There is no UK and Irish Events in {date_tab_name}')
            close_button = self.site.racing_event_details.meeting_selector if self.device_type == 'desktop' else  self.site.racing_event_details.meetings_list.close_button
            close_button.click()
            return
        else:
            if not uk_and_irish.has_items:
                uk_and_irish.expand()
            wait_for_result(lambda: uk_and_irish.has_items is True)
            meeting_name, meeting = uk_and_irish.first_item
            event_time, event = meeting.first_item
            event.click()
        self.book_mark_the_horses_and_verify_signposting(number_of_horses=4)

    def test_004_verify_that_user_is_able_to_bookmark_and_add_notes_from_todays_and_tomorrows_events_by_selecting_it_from_the_meeting_overlay_in_the_events_detail_page(
            self):
        """
        DESCRIPTION: Verify that user is able to bookmark and add notes from today's and tomorrow's events by selecting it from the meeting overlay in the events detail page.
        EXPECTED: User should be able to bookmark and add notes against various horses from events from today's and tomorrow's events when they select the event from the meeting overlay.
        EXPECTED: User should be able to view the bookmark and notes signposting.
        EXPECTED: The bookmarked horses should be added to the Stable.
        """
        self.test_003_select_the_overlay_from_the_event_details_pageselect_an_event_from_the_uk_amp_irish_meetings_which_is_scheduled_2_days_after_the_current_date_sundaymonday_etc_in_the_events_details_page_select_the_edit_stable_option_and_try_to_bookmark_and_add_the_notes_against_the_horse_and_click_on_the_done_button_to_save_the_notes(test_004=True, today=True)
        self.test_003_select_the_overlay_from_the_event_details_pageselect_an_event_from_the_uk_amp_irish_meetings_which_is_scheduled_2_days_after_the_current_date_sundaymonday_etc_in_the_events_details_page_select_the_edit_stable_option_and_try_to_bookmark_and_add_the_notes_against_the_horse_and_click_on_the_done_button_to_save_the_notes(test_004=True, tomorrow=True)

    def test_005_navigate_to_the_stable_page_by_clicking_any_of_the_entry_points_available_either_in_the_hr_landing_page_or_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Stable page by clicking any of the entry points available either in the HR landing page or the event details page.
        EXPECTED: User should be able to view all the bookmarked horses from Today's, Tomorrow's and XXXXX day events which was bookmarked in the above steps.
        EXPECTED: User should be able to un-bookmark and re-bookmark the previously selected horses from the My Stable page or the respective event details page.
        """
        self.navigate_to_page('my-stable')
        horses = self.site.my_stable.my_stable_race_cards.keys()
        horses_in_my_stable_page = sorted(list(set([horse.upper() for horse in horses])))
        book_marked_horses = sorted(list(set(self.bookmarked_horses)))

        self.assertListEqual(horses_in_my_stable_page, book_marked_horses,
                             f'Actual Horses in My Stable Page : {horses_in_my_stable_page} is not same as '
                             f'Expected Bookmarked Horses : {book_marked_horses}')
        self.un_book_mark_the_horses(current_page_my_stable=True)

        self.__class__.bookmarked_horses = []
        self.navigate_to_edp(event_id=self.today_event['event']['id'], sport_name='horse-racing')
        self.book_mark_the_horses_and_verify_signposting(number_of_horses=2)
        self.navigate_to_page('my-stable')
        horses = self.site.my_stable.my_stable_race_cards.keys()
        horses_in_my_stable_page = sorted([horse.upper() for horse in horses])
        book_marked_horses = sorted(self.bookmarked_horses)

        self.assertListEqual(horses_in_my_stable_page, book_marked_horses,
                             f'Actual Horses in My Stable Page : {horses_in_my_stable_page} is not same as '
                             f'Expected Bookmarked Horses : {book_marked_horses}')
        self.un_book_mark_the_horses(current_page_my_stable=True)

