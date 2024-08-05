import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.my_stable
@pytest.mark.timeout(900)
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C66065975_Verify_that_user_is_able_to_user_can_bookmark_un_bookmark_and_add_notes_against_the_horses_on_which_the_user_has_placed_bets_from_My_Bets_section__Open_tab_Cashout_tab_and_from_My_Bets_tab_available_in_the_event_details_page(BaseDataLayerTest,BaseUserAccountTest,
    BaseBetSlipTest):
    """
    TR_ID: C66065975
    NAME: Verify that user is able to user can bookmark, un-bookmark and add notes against the horses on which the user has placed bets from My Bets section - Open tab, Cashout tab and from My Bets tab available in the event details page.
    DESCRIPTION: This test case validates the functionality implemented in the phase 2 where in user can bookmark, un-bookmark and add notes against the horses on which the user has placed bets from My Bets section - Open tab, Cashout tab and from My Bets tab available in the event details page.
    """
    keep_browser_open = True
    uk_event_id, non_uk_event_id, bet_placed_selection_names, notes, horse_racing_edp_my_bets_tab = None, None, {}, 'Testing Notes', 'MY BETS'

    def close_overlays(self, event_type='UK'):
        if self.device_type == 'mobile' and self.site.wait_for_stream_and_bet_overlay(timeout=5):
            overlay = self.site.stream_and_bet_overlay
            try:
                if overlay and overlay.is_displayed():
                    overlay.close_button.click()
            except:
                pass

        if event_type == 'UK' and self.device_type == 'mobile' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

        if event_type == 'UK' and self.device_type == 'mobile' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

    def un_book_mark_the_horses(self):
        self.navigate_to_page('my-stable')
        if not self.site.my_stable.has_no_favorite_horses_icon():
            self.site.my_stable.edit_stable.click()
            cards = self.site.my_stable.my_stable_race_cards
            for card in cards.values():
                card.clear_bookmark()
                wait_for_haul(0.1)

    def verify_ga_tracking(self, position_event=None, location_event=None, event_detail=None):
        expected_resp = {
            "event": "Event.Tracking",
            "component.CategoryEvent": "horse racing",
            "component.LabelEvent": "my stable",
            "component.ActionEvent": "click",
            "component.PositionEvent": position_event,
            "component.LocationEvent": location_event,
            "component.EventDetails": event_detail,
            "component.URLClicked": "not applicable",
            "component.ContentPosition": "not applicable",
        }

        attempts = 5
        while attempts:
            attempts -= 1
            try:
                actual_response = self.get_data_layer_specific_object(object_key="event",
                                                                      object_value="Event.Tracking")
                self.assertEqual(expected_resp, actual_response)
            except Exception as e:
                if not attempts:
                    raise e
                else:
                    wait_for_haul(3)
                    continue

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS configurations
        PRECONDITIONS: My Stable Menu item
        PRECONDITIONS: My Stable Configurations
        PRECONDITIONS: Checkbox against �Active Mystable� - Should be checked in
        PRECONDITIONS: Checkbox against �Mystable Horses Running Today Carousel� - Should be checked in
        PRECONDITIONS: Checkbox against �Active Antepost� - Should be checked in
        PRECONDITIONS: Checkbox against �Active Open Bets� - Should be checked in (Phase 2)
        PRECONDITIONS: Checkbox against 'Active Settled Bets' - Should not be checked in (Phase 2)
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

        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.__class__.uk_event_id = next((event['event']['id'] for event in events if
                                           'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event'][
                                               'typeFlagCodes']))
        if not self.uk_event_id:
            raise SiteServeException('UK and Irish Events are unavailable')

        self.__class__.non_uk_event_id = next((event['event']['id'] for event in events if
                                               'UK' not in event['event']['typeFlagCodes'] and 'SP' not in
                                               event['event'][
                                                   'typeFlagCodes']))
        if not self.non_uk_event_id:
            raise SiteServeException('Non UK and Irish Events are unavailable')

    def test_001_login_to_the_application_with_valid_credentials_and_navigate_to_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Login to the application with valid credentials and navigate to the Horse racing landing page.
        EXPECTED: User should be able to successfully login and navigate to the Horse racing landing page.
        """
        self.__class__.username = tests.settings.my_stable_user
        self.site.login(username=self.username)

    def test_002_select_an_event_from_the_uk_amp_irish_meetings_select_multiple_selections_and_place_bet(self, event_id=None, event_type='UK'):
        """
        DESCRIPTION: Select an event from the UK &amp; Irish meetings. Select multiple selections and place bet.
        EXPECTED: The bets should be placed successfully.
        """
        self.un_book_mark_the_horses()
        self.navigate_to_edp(event_id=self.uk_event_id if not event_id else event_id, sport_name='horse-racing')
        self.close_overlays(event_type=event_type)

        outcomes = self.site.racing_event_details.items_as_ordered_dict
        bet_places_horses = []
        for outcome_name, outcome in list(outcomes.items())[:2]:
            outcome.scroll_to_we()
            outcome.odds_button.click()
            if self.device_type == 'mobile' and len(bet_places_horses) == 0:
                self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True, timeout=15),
                                msg='Quick Bet is not opened')
                self.site.quick_bet_panel.close()
                wait_for_haul(2)
            bet_places_horses.append(outcome_name.upper())

        self.bet_placed_selection_names[event_type] = bet_places_horses

        self.site.open_betslip()
        section = self.get_betslip_sections().Singles
        section.all_stakes_section.amount_form.enter_amount(value='0.1')
        self.site.betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_003_navigate_to__the_my_bets_section___open_tab_and_try_to_bookmarkun_bookmark_the_horses_from_the_section_and_add_notes(
            self):
        """
        DESCRIPTION: Navigate to  the My Bets section - Open tab and try to bookmark/un-bookmark the horses from the section and add notes.
        EXPECTED: 1. The tooltip should be displayed for the first time for the user against the bookmark icon where user has not bookmarked any horse from the My Bets - Open tab.
        EXPECTED: 2. The user should be able to view the bookmark option against the horses from the UK &amp; Irish races only.
        EXPECTED: 3. User should be able to bookmark/un-bookmark the horses and add notes to it from the My Bets - Open tab.
        EXPECTED: 4. The user should be able to view the bookmark and notes signposting in the section.
        EXPECTED: 5. User should be able to view the notes in the My Stable page.
        """
        # Navigating to My Bets - open tab : verifying ga tracking for Open Bets - click on bookmark and save
        self.site.open_my_bets_open_bets()
        uk_event_bet = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        bet_placed_by_script = \
            [bet_leg for bet in uk_event_bet.values() for bet_leg in bet.items_as_ordered_dict.values()][0]
        tooltip_container_status = wait_for_result(lambda: bet_placed_by_script.my_stable_bookmark.is_tooltip_container_appear() is True,name="waiting for my stable tooltip in open bets ")
        self.assertTrue(tooltip_container_status, 'Tooltip Container is not displayed')

        bookmark = bet_placed_by_script.my_stable_bookmark
        bookmark.click()
        wait_for_result(lambda: bookmark.is_bookmarked is True, name="Checking whether the horse is bookmarked")
        self.assertTrue(bookmark.is_bookmarked, 'Unable to Bookmark')
        # ga tracking for click on bookmark
        location_event, position_event, event_detail = "open bets - sports", "bookmark", f"{bet_placed_by_script.outcome_name} - added"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)

        bet_placed_by_script.my_stable_notes.input_notes.value = self.notes
        bet_placed_by_script.my_stable_notes.save.click()
        # ga tracking for click on save
        position_event, event_detail = "notes", f"{bet_placed_by_script.outcome_name} - save"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)

        self.assertTrue(bet_placed_by_script.has_my_stable_sign_posting(), 'My Stable Signposting is Not Displayed')
        self.assertTrue(bet_placed_by_script.has_my_stable_notes_sign_posting(),
                        'My Stable Notes signposting is not Displayed')
        bookmarked_horse_name = bet_placed_by_script.outcome_name

        # navigating to my-stable page : verifying bookmarked horse is appeared in my stable page and added notes in My Bets - open tab
        self.navigate_to_page('my-stable')
        horse_name, horse = self.site.my_stable.first_item
        self.assertTrue(horse_name and horse_name.upper() == bookmarked_horse_name.upper(),
                        f'Bookmarked Horse is not displayed in My Stable Page or Actual Horse Name is : {horse_name} is not same as Expected Horse name {bookmarked_horse_name}')

        horse.expand()
        horse.view_notes_button.click()
        notes_status = wait_for_result(lambda: horse.existing_notes == self.notes,name="waiting for the added notes and the exixting notes to be matched")
        self.assertTrue(notes_status, f'Actual Notes {horse.existing_notes} is not same as Expected Notes is {self.notes}')

        # navigating to edp : verifying bookmarked horse is appeared in edp - my bets
        self.navigate_to_edp(self.uk_event_id, sport_name='horse-racing')
        self.site.racing_event_details.event_user_tabs_list.open_tab(tab_name=self.horse_racing_edp_my_bets_tab)
        bets = self.site.racing_event_details.my_bets.accordions_list.items_as_ordered_dict
        bet_leg_in_edp = \
            next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if bet_leg.outcome_name.upper() == bookmarked_horse_name.upper()), None)
        self.assertTrue(bet_leg_in_edp.has_my_stable_sign_posting(), 'My Stable Signposting is Not Displayed')
        self.assertTrue(bet_leg_in_edp.has_my_stable_notes_sign_posting(),
                        'My Stable Notes signposting is not Displayed')

        # navigating back to My Bets - open tab
        self.site.open_my_bets_open_bets()
        uk_event_bet = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        bet_placed_by_script = \
            next((bet_leg for bet in uk_event_bet.values() for bet_leg in bet.items_as_ordered_dict.values() if bet_leg.outcome_name.upper() == bookmarked_horse_name.upper()), None)
        bet_placed_by_script.my_stable_bookmark.click()
        wait_for_result(lambda: bet_placed_by_script.my_stable_bookmark.is_bookmarked is False,name="checking for whether is horse is to be unbook marked")
        self.assertFalse(bet_placed_by_script.my_stable_bookmark.is_bookmarked, 'Unable to Un-Bookmark')

    def test_004_navigate_to__the_my_bets_section___cashout_tab_and_try_to_bookmarkun_bookmark_the_horses_from_the_section_and_add_notes(
            self):
        """
        DESCRIPTION: Navigate to  the My Bets section - Cashout tab and try to bookmark/un-bookmark the horses from the section and add notes.
        EXPECTED: 1. The tooltip should be displayed for the first time for the user against the bookmark icon where user has not bookmarked any horse from the My Bets - Cashout tab.
        EXPECTED: 2. The user should be able to view the bookmark option against the horses from the UK &amp; Irish races only.
        EXPECTED: 3. User should be able to bookmark/un-bookmark the horses and add notes to it from the My Bets - Cashout tab.
        EXPECTED: 4. The user should be able to view the bookmark and notes signposting in the section.
        EXPECTED: 5. User should be able to view the notes in the My Stable page.
        """
        # Navigating to My Bets - cash out tab : verifying ga tracking for Cash out - click on bookmark and save
        self.site.open_my_bets_cashout()
        uk_event_bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        bet_placed_by_script = \
            [bet_leg for bet in uk_event_bets.values() for bet_leg in bet.items_as_ordered_dict.values()][0]

        bookmark = bet_placed_by_script.my_stable_bookmark

        bookmark.click()
        wait_for_result(lambda: bookmark.is_bookmarked is True, name="Checking whether the horse is bookmarked")
        self.assertTrue(bookmark.is_bookmarked, 'Unable to Bookmark')
        # ga tracking for click bookmarking
        location_event, position_event, event_detail = "cashout bets - sports", "bookmark", f"{bet_placed_by_script.outcome_name} - added"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)

        bet_placed_by_script.my_stable_notes.input_notes.value = self.notes
        bet_placed_by_script.my_stable_notes.save.click()

        position_event, event_detail = "notes", f"{bet_placed_by_script.outcome_name} - save"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)

        self.assertTrue(bet_placed_by_script.has_my_stable_sign_posting(), 'My Stable Signposting is Not Displayed')
        self.assertTrue(bet_placed_by_script.has_my_stable_notes_sign_posting(),
                        'My Stable Notes signposting is not Displayed')

        bookmarked_horse_name = bet_placed_by_script.outcome_name

        # navigating to my-stable page : verifying bookmarked horse is appeared in my stable page and added notes in My Bets - cash out tab
        self.navigate_to_page('my-stable')
        horse_name, horse = self.site.my_stable.first_item
        self.assertTrue(horse_name and horse_name.upper() == bookmarked_horse_name.upper(),
                        f'Bookmarked Horse is not displayed in My Stable Page or Actual Horse Name is : {horse_name} is not same as Expected Horse name {bookmarked_horse_name}')

        horse.expand()
        horse.view_notes_button.click()
        notes_status = wait_for_result(lambda: horse.existing_notes == self.notes, name="waiting for the added notes and the exixting notes to be matched")
        self.assertTrue(notes_status,
                        f'Actual Notes {horse.existing_notes} is not same as Expected Notes is {self.notes}')

        # navigating to edp : verifying bookmarked horse is appeared in edp - my bets
        self.navigate_to_edp(self.uk_event_id, sport_name='horse-racing')
        self.close_overlays()
        self.site.racing_event_details.event_user_tabs_list.open_tab(tab_name=self.horse_racing_edp_my_bets_tab)
        bets = self.site.racing_event_details.my_bets.accordions_list.items_as_ordered_dict
        bet_leg_in_edp = \
            next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if
                  bet_leg.outcome_name.upper() == bookmarked_horse_name.upper()), None)
        self.assertTrue(bet_leg_in_edp.has_my_stable_sign_posting(), 'My Stable Signposting is Not Displayed')
        self.assertTrue(bet_leg_in_edp.has_my_stable_notes_sign_posting(),
                        'My Stable Notes signposting is not Displayed')

        # navigating back to My Bets - cash out
        self.site.open_my_bets_cashout()
        uk_event_bet = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        bet_placed_by_script = \
            next((bet_leg for bet in uk_event_bet.values() for bet_leg in bet.items_as_ordered_dict.values() if
                  bet_leg.outcome_name.upper() == bookmarked_horse_name.upper()), None)
        bet_placed_by_script.my_stable_bookmark.click()
        wait_for_result(lambda: bet_placed_by_script.my_stable_bookmark.is_bookmarked is False, name="checking for whether is horse is to be un-bookmarked")
        self.assertFalse(bet_placed_by_script.my_stable_bookmark.is_bookmarked, 'Unable to Un-Bookmark')


    def test_005_navigate_to_the_my_bets_section___settled_tab_and_verify_that_user_is_not_able_to_view_bookmark_and_add_notes_options(
            self):
        """
        DESCRIPTION: Navigate to the My Bets section - Settled tab and verify that user is not able to view bookmark and add notes options.
        EXPECTED: The user should not be able to view the bookmark and add notes option in the My Bets - Settled bets section.
        """
        # we can't wait up to event resulted

    def test_006_select_any_uk_and_irish_racing_event_and_navigate_to_the_respective_event_details_page_select_multiple_selections_and_place_bet_navigate_to_the_my_bets_tab_in_the_edp(
            self):
        """
        DESCRIPTION: Select any UK and Irish racing event and navigate to the respective event details page. Select multiple selections and place bet. Navigate to the My Bets tab in the EDP.
        EXPECTED: 1. The tooltip should be displayed for the first time for the user against the bookmark icon where user has not bookmarked any horse from the event details page - My Bets tab.
        EXPECTED: 2. The user should be able to view the bookmark option against the horses from the UK &amp; Irish races only.
        EXPECTED: 3. User should be able to bookmark/un-bookmark the horses and add notes to it from the event details page - My Bets tab.
        EXPECTED: 4. The user should be able to view the bookmark and notes signposting in the section.
        EXPECTED: 5. User should be able to view the notes in the My Stable page.
        """
        # logging with new user to validate tooltip in EDP - My Bets
        self.navigate_to_page('/')
        self.site.logout()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.refresh_page()
        self.site.login(username=self.username)
        self.navigate_to_edp(event_id=self.uk_event_id, sport_name='horse-racing')
        self.close_overlays()
        self.site.racing_event_details.event_user_tabs_list.open_tab(tab_name=self.horse_racing_edp_my_bets_tab)
        bets = self.site.racing_event_details.my_bets.accordions_list.items_as_ordered_dict
        bet_placed_by_script = \
            [bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values()][0]

        tooltip_container_status = bet_placed_by_script.my_stable_bookmark.is_tooltip_container_appear()
        self.assertTrue(tooltip_container_status, 'Tooltip Container is not displayed')  # validating the tooltip

        bookmark = bet_placed_by_script.my_stable_bookmark
        bookmark.click()
        wait_for_result(lambda: bookmark.is_bookmarked is True, name='validating horse to be bookmarked')
        self.assertTrue(bookmark.is_bookmarked, 'Unable to Bookmark')
        # verifying ga tracking for edp >> my-bets >> click - bookmark
        location_event, position_event, event_detail = "EDP - My bets", "bookmark", f"{bet_placed_by_script.outcome_name} - added"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)

        bet_placed_by_script.my_stable_notes.input_notes.value = self.notes
        bet_placed_by_script.my_stable_notes.save.click()
        # verifying ga tracking for edp >> my-bets >> bookmark >> click on save
        position_event, event_detail = "notes", f"{bet_placed_by_script.outcome_name} - save"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)

        self.assertTrue(bet_placed_by_script.has_my_stable_sign_posting(), 'My Stable Signposting is Not Displayed')
        self.assertTrue(bet_placed_by_script.has_my_stable_notes_sign_posting(),
                        'My Stable Notes signposting is not Displayed')
        bookmarked_horse_name = bet_placed_by_script.outcome_name

        # navigating to My Bets - Open Bets : verifying bookmarked horse appeared in My Bets - Open
        self.site.open_my_bets_open_bets()
        uk_event_bet = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        bet_leg_in_my_bets = \
            next((bet_leg for bet in uk_event_bet.values() for bet_leg in bet.items_as_ordered_dict.values() if
                  bet_leg.outcome_name.upper() == bookmarked_horse_name.upper()), None)
        self.assertTrue(bet_leg_in_my_bets.has_my_stable_sign_posting(), 'My Stable Signposting is Not Displayed')
        self.assertTrue(bet_leg_in_my_bets.has_my_stable_notes_sign_posting(),
                        'My Stable Notes signposting is not Displayed')

        # verifying in my-stable page : bookmarked horse appeared in my stable page
        self.navigate_to_page('my-stable')
        horse_name, horse = self.site.my_stable.first_item
        self.assertTrue(horse_name and horse_name.upper() == bookmarked_horse_name.upper(),
                        f'Bookmarked Horse is not displayed in My Stable Page or Actual Horse Name is : {horse_name} is not same as Expected Horse name {bookmarked_horse_name}')

        horse.expand()
        horse.view_notes_button.click()
        notes_status = wait_for_result(lambda: horse.existing_notes == self.notes, name="waiting for the added notes and the exixting notes to be matched")
        self.assertTrue(notes_status,
                        f'Actual Notes {horse.existing_notes} is not same as Expected Notes is {self.notes}')

        # going back to edp - my bets
        self.navigate_to_edp(self.uk_event_id, sport_name='horse-racing')
        self.close_overlays()
        self.site.racing_event_details.event_user_tabs_list.open_tab(tab_name=self.horse_racing_edp_my_bets_tab)
        bets = self.site.racing_event_details.my_bets.accordions_list.items_as_ordered_dict
        bet_leg_in_edp = \
            next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if
                  bet_leg.outcome_name.upper() == bookmarked_horse_name.upper()), None)
        bookmark = bet_leg_in_edp.my_stable_bookmark
        bookmark.click()
        wait_for_result(lambda: bookmark.is_bookmarked is False, name="checking for whether is horse is to be unbookmarked")
        self.assertFalse(bookmark.is_bookmarked, f'Unable to Un-Bookmark the horse name {bookmarked_horse_name.upper()} in EDP')

        wait_for_haul(3)
        bookmark.click()
        wait_for_result(lambda: bookmark.is_bookmarked is True, name="Checking whether the horse is bookmarked ")
        self.assertTrue(bookmark.is_bookmarked, f'Unable to Bookmark horse name {bookmarked_horse_name.upper()} in EDP')
        bet_leg_in_edp.my_stable_notes.cancel.click()
        # verifying ga tracking for edp >> my-bets >> bookmark >> click on cancel
        position_event, event_detail = "no notes", f"{bet_leg_in_edp.outcome_name} - close"
        self.verify_ga_tracking(location_event=location_event, event_detail=event_detail, position_event=position_event)
        bookmark.click()
        wait_for_result(lambda: bookmark.is_bookmarked is False, name="checking for whether is horse is to be unbookmarked")
        self.assertFalse(bookmark.is_bookmarked, f'Unable to Un-Bookmark the horse name {bookmarked_horse_name.upper()} in EDP')

    def test_007_verify_that_user_should_be_able_to_bookmarkun_bookmark_and_view_the_signposting_in_edp___my_bets_tab_my_bets_section___open_cashout_tabs(
            self):
        """
        DESCRIPTION: Verify that user should be able to bookmark/un-bookmark and view the signposting in EDP - My Bets tab, My Bets section - Open, Cashout tabs.
        EXPECTED: User should be able to bookmark/un-bookmark add notes from any of these sections and it should be updated accordingly in EDP- My Bets tab, My Bets section - Open, Cashout tabs.
        """
        # covered in above step

    def test_008_verify_that_user_is_able_to_bookmarkun_bookmark_horses_from_the_my_bets_section___open_cashout_tabs_and_edp___my_bets_tab_when_they_place_bets_for_multiple_selections_from_uk_amp_irish_events_and_few_selections_from_the_non_uk_amp_irish_events(
            self):
        """
        DESCRIPTION: Verify that user is able to bookmark/un-bookmark horses from the My Bets Section - Open, Cashout tabs and EDP - My Bets tab when they place bets for multiple selections from UK &amp; Irish events and few selections from the Non UK &amp; Irish events.
        EXPECTED: User should be able to view, bookmark, add notes and un-bookmark horses which are from UK &amp; Irish meetings only from the My Bets section - Open, Cashout tabs and EDP - My Bets tab.
        EXPECTED: User should not be able to view, bookmark, add notes and un-bookmark horses which are not from UK &amp; Irish meetings from the My Bets section - Open, Cashout tabs and EDP - My Bets tab.
        """
        self.test_002_select_an_event_from_the_uk_amp_irish_meetings_select_multiple_selections_and_place_bet(event_id=self.non_uk_event_id, event_type='Non-UK') # placing bet on non-uk event
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict

        non_uk_bet = next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if bet_leg.outcome_name.upper() in self.bet_placed_selection_names['Non-UK']), None)
        uk_bet = next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if bet_leg.outcome_name.upper() in self.bet_placed_selection_names['UK']), None)

        self.assertFalse(non_uk_bet.has_my_stable_bookmark(), f'Bookmark Displayed For Non-UK bet. Non UK event id : "{self.non_uk_event_id}" and Selection Name "{non_uk_bet.outcome_name}"')
        self.assertTrue(uk_bet.has_my_stable_bookmark(), f'Bookmark Not Displayed For UK bet. UK event id : "{self.uk_event_id}" and Selection Name "{uk_bet.outcome_name}"')

        uk_bet.my_stable_bookmark.click()
        wait_for_result(lambda: uk_bet.my_stable_bookmark.is_bookmarked is True, name="checking for whether is horse is to be bookmarked")
        self.assertTrue(uk_bet.my_stable_bookmark, f'Unable to Bookmark {uk_bet.outcome_name}')

        uk_bet.my_stable_bookmark.click()
        wait_for_result(lambda: uk_bet.my_stable_bookmark.is_bookmarked is False, name="checking for whether is horse is to be unbook marked")
        self.assertFalse(uk_bet.my_stable_bookmark.is_bookmarked, f'Unable to Un-Bookmark {uk_bet.outcome_name}')

        self.navigate_to_edp(self.non_uk_event_id, sport_name='horse-racing')
        self.site.racing_event_details.event_user_tabs_list.open_tab(tab_name=self.horse_racing_edp_my_bets_tab)
        bets = self.site.racing_event_details.my_bets.accordions_list.items_as_ordered_dict
        bet_leg_in_edp = \
            next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values()), None)
        self.assertFalse(bet_leg_in_edp.has_my_stable_bookmark(), f'Bookmark Displayed For Non-UK bet. Non UK event id : "{self.non_uk_event_id}" and Selection Name "{non_uk_bet.outcome_name}"')

    def test_009_verify_that_user_should_be_able_to_bookmark_un_bookmark_horses_from_the_my_bets_section___open_cashout_tabs_and_edp___my_bets_tab_when_they_place_bets_on_horses_from_the_uk_amp_irish_meetings_along_with_other_sports(
            self):
        """
        DESCRIPTION: Verify that user should be able to bookmark/ un-bookmark horses from the My Bets Section - Open, Cashout tabs and EDP - My Bets tab when they place bets on horses from the UK &amp; Irish meetings along with other sports.
        EXPECTED: User should be able to view, bookmark, add notes and un-bookmark horses which are from UK &amp; Irish meetings only from the My Bets section - Open, Cashout tabs and EDP - My Bets tab.
        EXPECTED: User should not be able to view the bookmark option against the selections from other sports in the My Bets section - Open, Cashout tabs and EDP - My Bets tab.
        """
        self.navigate_to_edp(event_id=self.uk_event_id, sport_name='horse-racing')
        self.close_overlays()

        outcomes = self.site.racing_event_details.items_as_ordered_dict
        bet_places_horse = None
        for outcome_name, outcome in outcomes.items():
            outcome.scroll_to_we()
            if outcome_name.upper() not in self.bet_placed_selection_names['UK']:
                outcome.odds_button.click()
                bet_places_horse = outcome_name.upper()
                break

        if self.device_type == 'mobile':
            self.site.quick_bet_panel.add_to_betslip_button.click()
            wait_for_result(lambda: int(self.site.header.bet_slip_counter.counter_value) == 1, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException), name=f'Waiting for Bet Counter Increased')

        self.navigate_to_page('sport/football')
        events = self.site.football.tab_content.accordions_list.first_item[1].items_as_ordered_dict
        selection_name, event = None, None
        for event_name, event in events.items():
            name, odd = next(([name, button] for name, button in list(event.template.get_available_prices().items()) if
                               button.name.upper() not in ['N/A', 'SUSP']), [None, None])
            if odd:
                selection_name = name
                event = event
                odd.click()
                break

        self.site.open_betslip()
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

        if self.brand == 'bma':
            event.click()
            self.site.wait_content_state_changed()
            self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)
            bets = self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict

            horse_bet_leg_in_my_bets = \
                next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if
                      bet_leg.outcome_name.upper() == bet_places_horse.upper()), None)

            football_bet_leg_in_my_bets = \
                next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if
                      bet_leg.outcome_name.upper() == selection_name.upper()), None)

            self.assertFalse(football_bet_leg_in_my_bets.has_my_stable_bookmark(),
                             f'Bookmark Displayed For Football event. Issue with Football >> My Bets >> SelectionName : {selection_name}')

            self.assertTrue(horse_bet_leg_in_my_bets.has_my_stable_bookmark(),
                             f'Bookmark Not Displayed For Horse : {bet_places_horse}. Issue with Football >> My Bets >> SelectionName : {bet_places_horse}')

            horse_bet_leg_in_my_bets.my_stable_bookmark.click()
            wait_for_result(lambda: horse_bet_leg_in_my_bets.my_stable_bookmark.is_bookmarked is True)
            self.assertTrue(horse_bet_leg_in_my_bets.my_stable_bookmark, f'Unable to Bookmark {horse_bet_leg_in_my_bets.outcome_name}')

            horse_bet_leg_in_my_bets.my_stable_bookmark.click()
            wait_for_result(lambda: horse_bet_leg_in_my_bets.my_stable_bookmark.is_bookmarked is False)
            self.assertFalse(horse_bet_leg_in_my_bets.my_stable_bookmark.is_bookmarked, f'Unable to Un-Bookmark {horse_bet_leg_in_my_bets.outcome_name}')

        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        football_bet = next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if
                           bet_leg.outcome_name.upper() == selection_name.upper()), None)

        horse_racing_bet = next((bet_leg for bet in bets.values() for bet_leg in bet.items_as_ordered_dict.values() if
                           bet_leg.outcome_name.upper() == bet_places_horse.upper()), None)

        self.assertFalse(football_bet.has_my_stable_bookmark(), f'Bookmark Displayed for selection name : {selection_name}')
        self.assertTrue(horse_racing_bet.has_my_stable_bookmark(), f'Bookmark Not Displayed for selection name : {selection_name}')

    def test_010_verify_ga_tracking_for_various_actions_performed_from_edp___my_bets_tab_and_my_bets_section___opencashout_tabs(
            self):
        """
        DESCRIPTION: Verify GA tracking for various actions performed from EDP - My Bets tab and My Bets section - Open/Cashout tabs.
        EXPECTED: Verify that the below actions are captured through GA tracking.
        EXPECTED: Scenario 1: Bookmark from Open Bets and Cashout tabs
        EXPECTED: ![](index.php?/attachments/get/3292bb26-2510-41c6-9c23-20b8c512171a)
        EXPECTED: Scenario 2: Saved empty notes from Open Bets and Cashout tabs.
        EXPECTED: ![](index.php?/attachments/get/f4c1f284-6c15-4216-afb6-b21fb16900d9)
        EXPECTED: ![](index.php?/attachments/get/84d89fbb-9f07-450e-a0c8-017fb5011abe)
        EXPECTED: Scenario 3: Horse racing EDP - Bookmarking and saving notes.
        EXPECTED: ![](index.php?/attachments/get/9b68c69d-388f-42d7-b3cc-9354060330bb)
        EXPECTED: Scenario 4: Horse racing EDP - Bookmarking and cancel on notes pop up.
        EXPECTED: ![](index.php?/attachments/get/392595f4-d97a-4e20-a75c-3a506ee8474c)
        """
        # covered in above step
