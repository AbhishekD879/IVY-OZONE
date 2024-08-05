import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.my_stable
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.timeout(1200)
@vtest
class Test_C66050375_Verify_the_display_of_error_message_when_user_tries_to_bookmark_the_101th_horse_and_the_hyperlink_to_navigate_to_the_stable_page(Common):
    """
    TR_ID: C66050375
    NAME: Verify the display of error message when user tries to bookmark the 101th horse and  the hyperlink to navigate to the  stable page.
    DESCRIPTION: This test case validates the display of the error message pop up when user tries to bookmark the 101 th horse and the functionality of the hyperlink which is available in the message.
    DESCRIPTION: Note: User will be able to bookmark only 100 horses maximum.
    """
    keep_browser_open = True
    bookmarked_horses_count = 0

    def un_book_mark_the_horses(self):
        self.navigate_to_page('my-stable')
        if not self.site.my_stable.has_no_favorite_horses_icon():
            self.site.my_stable.edit_stable.click()
            cards = self.site.my_stable.my_stable_race_cards
            for card in cards.values():
                card.clear_bookmark()
                wait_for_haul(0.1)

    def book_mark_horses_by_event_id(self, event_id):
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        if self.device_type == 'mobile':
            if self.event_ids[event_id] and self.site.wait_for_stream_and_bet_overlay(timeout=5):
                overlay = self.site.stream_and_bet_overlay
                if overlay and overlay.is_displayed():
                    overlay.close_button.click()
            if self.site.wait_for_my_stable_onboarding_overlay():
                self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        if self.device_type == 'mobile':
            if self.site.wait_for_my_stable_onboarding_overlay():
                self.site.my_stable_onboarding_overlay.close_button.click()
        self.site.racing_event_details.edit_stable.click()
        outcomes = self.site.racing_event_details.items_as_ordered_dict

        for horse_name, outcome in outcomes.items():
            if horse_name in [vec.racing.UNNAMED_FAVORITE, vec.racing.UNNAMED_FAVORITE_2ND]:
                continue
            if self.bookmarked_horses_count == 100:
                # test_003
                outcome.my_stable_bookmark.click()
                self.assertTrue(outcome.my_stable_bookmark.is_tooltip_container_appear(), f'Tooltip container is not popup')
                error_msg = outcome.my_stable_bookmark.error_msg
                self.assertEqual(''.join(error_msg.split()), ''.join(self.error_msg.split()), f'Actual Message : "{error_msg}" is not same as '
                                                            f'Expected Message : "{self.error_msg}"')

                # test_004
                outcome.my_stable_bookmark.go_to_my_stable_page_link.click()
                self.site.wait_content_state('my-stable')
                try:
                    self.un_book_mark_the_horses()
                except:
                    if not self.site.my_stable.has_no_favorite_horses_icon():
                        self.un_book_mark_the_horses()
                return "Validations Completed"
            else:
                if outcome.is_bookmark_filled:
                    continue
                outcome.fill_bookmark()
                self.__class__.bookmarked_horses_count = self.bookmarked_horses_count + 1
        return "Validations Not Completed Yet."

    def get_event_ids_for_100_horses(self):
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.assertTrue(events, f'UK and Irish Events are unavailable')
        outcomes_count, event_ids = 0, {}
        for event in events:
            if outcomes_count > 130:
                break
            if 'UK' in event['event']['typeFlagCodes']:
                event = self.ss_req.ss_event_to_outcome_for_event(event_id=event['event']['id'])[0]
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == '|Win or Each Way|' and market['market'].get(
                            'children'):
                        outcomes_count_for_event = sum([1 for outcome in market['market'].get('children') if outcome.get('outcome').get('name') not in ['|Unnamed Favourite|', '|Unnamed 2nd Favourite|']])
                        drill_down_tag_names = event['event']["drilldownTagNames"]
                        event_ids[event['event']['id']] = "EVFLAG_IHR" in drill_down_tag_names and "EVFLAG_RVA" not in drill_down_tag_names and "EVFLAG_PVM" not in drill_down_tag_names and "EVFLAG_PVA" not in drill_down_tag_names
                        outcomes_count += outcomes_count_for_event
        return outcomes_count, event_ids

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
        my_stable_config = self.cms_config.get_my_stable_config()
        if not my_stable_config.get('active'):
            raise CmsClientException('My stable Page is not active in CMS')
        self.__class__.error_msg = my_stable_config.get('horseCountExceededMsg').strip('\n').strip()
        outcomes_count, self.__class__.event_ids = self.get_event_ids_for_100_horses()
        self.assertTrue('100 horses are not available to bookmark')

    def test_001_login_to_the_application_with_valid_user_credentials_who_has_bookmarked_around_100_horses_alreadynavigate_to_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Login to the application with valid user credentials who has bookmarked around 100 horses already.Navigate to the Horse racing landing page.
        EXPECTED: User should be on the Horse racing landing page logged in successfully.
        """
        self.site.login()
        self.un_book_mark_the_horses()
        for event_id in self.event_ids:
            status_msg = self.book_mark_horses_by_event_id(event_id=event_id)
            if status_msg == "Validations Completed":
                self._logger.info('Successfully Validated the "Error Message" and "Go to My Stable" Link')
                break

    def test_002_select_an_event_from_the_uk_amp_irish_racesclick_on_the_edit_stable_option_available_in_the_each_way_market_tab(self):
        """
        DESCRIPTION: Select an event from the UK &amp; Irish races.Click on the 'Edit Stable' option available in the Each way market tab.
        EXPECTED: The user should be in the event details page. The bookmark options should be displayed against the horses.
        """
        # covered in above step

    def test_003_select_the_bookmark_option_against_any_of_the_horses_available_in_the_race_card_user_has_already_bookmarked_100_horses(self):
        """
        DESCRIPTION: Select the bookmark option against any of the horses available in the race card. User has already bookmarked 100 horses.
        EXPECTED: User should not be able to bookmark the 101th horse since the maximum limit has already been reached.
        EXPECTED: Message should be displayed stating that 'Maximum number of  selections reached. To add more, remove horses from your stable.'
        EXPECTED: Note: This message is configurable in the CMS.
        EXPECTED: ![](index.php?/attachments/get/9cc80633-8e4a-41e5-888f-b38d065af25c) ![](index.php?/attachments/get/67a07643-1e8d-4a52-acc0-60272ffb11dd)  ![](index.php?/attachments/get/b9546b66-4955-48c8-beeb-6716e8901394)
        """
        # covered in above step

    def test_004_click_on_the_hyperlink_available_in_the_error_message_pop_upladbrokes_go_to_stable_matescoral_go_to_my_stableindexphpattachmentsgeta41e19d5_ce93_45af_ba9e_46243a8fe6bc_indexphpattachmentsget79396bb0_0a96_4a14_826c_fcbe785ee1a1(self):
        """
        DESCRIPTION: Click on the hyperlink available in the error message pop up.
        DESCRIPTION: Ladbrokes: Go to Stable Mates
        DESCRIPTION: Coral: Go to My Stable
        DESCRIPTION: ![](index.php?/attachments/get/a41e19d5-ce93-45af-ba9e-46243a8fe6bc) ![](index.php?/attachments/get/79396bb0-0a96-4a14-826c-fcbe785ee1a1)
        EXPECTED: User should be able to navigate to the Stable page when he clicks the hyperlink.
        """
        # covered in above step
