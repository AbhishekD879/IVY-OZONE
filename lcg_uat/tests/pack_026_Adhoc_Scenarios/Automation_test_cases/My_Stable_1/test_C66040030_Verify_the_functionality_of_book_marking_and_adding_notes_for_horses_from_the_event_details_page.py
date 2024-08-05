import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
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
@vtest
class Test_C66040030_Verify_the_functionality_of_book_marking_and_adding_notes_for_horses_from_the_event_details_page(Common):
    """
    TR_ID: C66040030
    NAME: Verify the functionality of book marking and adding notes for horses from the event details page.
    DESCRIPTION: The test case validates the functionality of book marking  horses and adding notes on the event details page.
    """
    keep_browser_open = True

    def generate_fake_paragraph(self):
        from faker import Faker
        fake = Faker()
        fake_paragraph = fake.paragraph(nb_sentences=1)
        while len(fake_paragraph) < 190:
            fake_paragraph += " " + fake.paragraph(nb_sentences=1)
        return fake_paragraph

    def check_your_notes_at_top_of_spotlight_and_last_run(self):
        """
        added check point while Phase-I review: Suggested By (Takellapti Anusha)
        Check point - Notes display above the spotlight and Last Run
        """
        location_of_your_notes = self.outcome.expanded_summary.my_stable_your_notes.location.get('y')
        if self.outcome.expanded_summary.has_spotlight_info:
            location_of_spotlight = self.outcome.expanded_summary.spotlight_info.location.get('y')
            self.assertLess(location_of_your_notes, location_of_spotlight,
                            msg=f'"YOUR NOTES" is not at top of the "SPOT LIGHT"')
        location_of_last_run = self.outcome.expanded_summary.last_run_info_label.location.get('y')
        self.assertLess(location_of_your_notes, location_of_last_run,
                        msg=f'"YOUR NOTES" is not at top of the "LAST RUN"')

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

        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.assertTrue(events, f'UK and Irish Events are unavailable')
        self.__class__.event_id = next((event['event']['id'] for event in events if
                                        'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event'][
                                            'typeFlagCodes']))

    def test_001_navigate_to_the_horse_racing_landing_page_and_select_any_event_under_the_uk_amp_irish_racesuser_should_be_logged_in(self):
        """
        DESCRIPTION: Navigate to the Horse racing landing page and select any event under the UK &amp; Irish races.
        DESCRIPTION: (User should be logged in)
        EXPECTED: User should be able to view the 'Edit Stable' option in the right where the each way terms are displayed.
        EXPECTED: ![](index.php?/attachments/get/e7d13573-2676-4406-8df9-4fee2170728f)
        """
        self.site.login()

        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

        if self.site.wait_for_stream_and_bet_overlay(timeout=10):
            overlay = self.site.stream_and_bet_overlay
            try:
                if overlay and overlay.is_displayed():
                    overlay.close_button.click()
            except StaleElementReferenceException:
                pass

        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

    def test_002_click_on_the_edit_stable_option_in_the_event_details_page(self):
        """
        DESCRIPTION: Click on the 'Edit Stable' option in the event details page.
        EXPECTED: The 'Edit Stable' button should be changed to 'Done' button.
        EXPECTED: The bookmark icons should be displayed against the individual horses available in the race card.
        EXPECTED: ![](index.php?/attachments/get/6f06130e-cf73-4593-8d7c-1a642e53b627)
        """
        self.site.racing_event_details.edit_stable.click()

    def test_003_select_the_bookmark_icon_against_any_of_the_horses_from_the_race_card(self):
        """
        DESCRIPTION: Select the bookmark icon against any of the horses from the race card.
        EXPECTED: 1. The bookmark icon should change it's colour to grey(When user clicks on the icon) and becomes dark (When user gets the response for the request) indicating that the particular horse is bookmarked successfully.
        EXPECTED: 2. The Notes pop up shows up against the bookmarked horse for which the user can add notes.
        EXPECTED: ![](index.php?/attachments/get/2227d23e-cd73-42d7-86c7-2860ccbb5a1e)
        """
        outcomes = self.site.racing_event_details.items_as_ordered_dict
        self.__class__.horse_name, self.__class__.outcome = next(iter(outcomes.items()))
        self.__class__.note = self.generate_fake_paragraph()
        self.outcome.fill_bookmark(notes=self.note)

    def test_004_add_notes_against_the_bookmarked_horse_in_the_notes_pop_up(self):
        """
        DESCRIPTION: Add notes against the bookmarked horse in the notes pop up.
        EXPECTED: User should be able to add notes upto 180 characters maximum limit.
        EXPECTED: Click on the 'Save' button.The entered notes should be saved.
        """
        # covered in above step

    def test_005_the_icons_for_bookmarking_and_notes_should_be_displayed_against_the_horse(self):
        """
        DESCRIPTION: The icons for bookmarking and notes should be displayed against the horse.
        EXPECTED: On successful bookmarking and entering the notes the respective icons should be displayed against the horse indicating that the horse is bookmarked and notes have been added.
        EXPECTED: ![](index.php?/attachments/get/a15ccdce-358d-4e50-9e5d-32f4769c3ced)
        """
        self.assertTrue(self.outcome.is_bookmark_filled, f'"{self.horse_name}" is not bookmarked')
        self.assertTrue(self.outcome.has_my_stable_notes_sign_posting(), f'Notes Signposting is not displayed')

    def test_006_verify_that_the_user_is_able_to_un_bookmark_the_horse_which_was_bookmarked_previously(self):
        """
        DESCRIPTION: Verify that the user is able to un-bookmark the horse which was bookmarked previously.
        EXPECTED: User should be able to un-bookmark and bookmark again the previously bookmarked horses by using the 'Edit Stable' option and de-selecting the horse which has already been bookmarked.
        EXPECTED: User should be able to bookmark again the previously bookmarked horse which was un-bookmarked.
        EXPECTED: (User can bookmark and un-bookmark a horse multiple times).
        """
        # covering in below step

    def test_007_verify_the_display_of_the_notes_entered_against_the_horses_by_clicking_on_the_show_more_option_in_the_edp(self):
        """
        DESCRIPTION: Verify the display of the notes entered against the horses by clicking on the 'Show More' option in the EDP.
        EXPECTED: User should be able to view the saved notes in the 'Your Notes' section when user clicks the 'Show More' option.
        EXPECTED: The notes will be displayed in the section above the 'Spotlight' section in the event details page.
        EXPECTED: ![](index.php?/attachments/get/fe74ac02-07e6-44f0-a56a-87e11c03033a)
        """
        self.outcome.show_summary_toggle.click()

        # checking the location of your notes
        self.check_your_notes_at_top_of_spotlight_and_last_run()

        your_notes_text = self.outcome.expanded_summary.my_stable_your_notes.notes_text.strip()
        self.assertEqual(your_notes_text, self.note[:180].strip(), f'Actual Text : "{your_notes_text}"\n is not same as \n'
                                                              f'Expected Text : "{self.note[:180]}"')

        self.outcome.clear_bookmark()
        wait_for_haul(2)
        self.assertFalse(self.outcome.is_bookmark_filled, f'Still "{self.horse_name}" bookmarked')

        self.outcome.fill_bookmark()
        self.assertTrue(self.outcome.is_bookmark_filled, f'Unable to bookmark "{self.horse_name}" again')

        self.outcome.clear_bookmark()
        wait_for_haul(2)
        self.assertFalse(self.outcome.is_bookmark_filled, f'Still "{self.horse_name}" bookmarked')

    def test_008_verify_the_trainer_name_and_form_id_in_my_stabe_page_as_same_in_edp(self):
        """
        added check point while Phase-I review: Suggested By (Takellapti Anusha)
        Check point - Trainee and Form number to be validated ( data for horse in stable and HR EDP should be same )

        DESCRIPTION: Bookmark one horse and from edp and check the details of horse in My-Stable Page
        EXPECTATION: On successful bookmarking navigate to my-stable page and verify the  trainer name and form id.
        """
        self.outcome.fill_bookmark()
        trainer_name_in_edp = self.outcome.trainer_name
        form_info_in_edp = self.outcome.form

        self.site.racing_event_details.my_stable_link.click()
        self.site.wait_content_state('my-stable')
        race_cards = self.site.my_stable.my_stable_race_cards
        horse = next((horse for horse_name, horse in race_cards.items() if horse_name == self.horse_name), None)
        self.assertIsNotNone(horse, f'Bookmarked Horse "{self.horse_name}" is not displayed in my stable page')

        horse.expand()
        trainer_name_in_my_stable = horse.trainer_name
        form_info_in_my_stable = horse.form

        self.assertEqual(trainer_name_in_edp, trainer_name_in_my_stable,
                         f'Actual Trainer Name : "{trainer_name_in_my_stable}" is not Matched with '
                         f'Expected Trainer Name : "{trainer_name_in_edp}" for Horse "{self.horse_name}"')

        self.assertEqual(form_info_in_edp, form_info_in_my_stable,
                         f'Actual Form : "{form_info_in_edp}" is not Matched with '
                         f'Expected Form : "{form_info_in_my_stable}" for Horse "{self.horse_name}"')
