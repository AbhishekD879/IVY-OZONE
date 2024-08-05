import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.my_stable
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C66039860_Verify_the_details_on_the_empty_Stable_page(BaseRacing):
    """
    TR_ID: C66039860
    NAME: Verify the details on the empty Stable page.
    DESCRIPTION: This test case validates the details displayed on the My Stable screen when the user has not bookmarked any horse and when he navigates to the My Stable page the Empty Stable screen should be viewed.
    PRECONDITIONS: CMS configurations
    PRECONDITIONS: My Stable Menu item
    PRECONDITIONS: My Stable Configurations
    PRECONDITIONS: Checkbox against "Active Mystable" - Should be checked in
    PRECONDITIONS: Checkbox against "Mystable Horses Running Today Carousel" - Should be checked in
    PRECONDITIONS: Checkbox against "Active Antepost" - Should be checked in
    PRECONDITIONS: Checkbox against "Active My Bets" (Phase 2)
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
    PRECONDITIONS: Empty Stable Message Label - Tap on "Edit Stable" on the Race Card to add a horse
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
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        Description : getting "my stabl"e data from cms
        """
        my_stable_data = self.cms_config.get_my_stable_config()
        my_stable_status_in_cms = my_stable_data.get('active')
        if not my_stable_status_in_cms:
            raise CmsClientException('My stable Page is not active in CMS')
        self.__class__.expected_stable_empty_text = my_stable_data.get('emptyStableLabel1').upper()
        self.__class__.expected_empty_stable_message_label = my_stable_data.get('emptyStableLabel2').upper()
        self.__class__.expected_view_todays_races_cta_button_text = my_stable_data.get('noHorsesCtaButton').upper()

    def test_001_login_to_the_application_and_navigate_to_the_horse_racing_landing_page_or_event_details_page(self):
        """
        DESCRIPTION: Login to the application and navigate to the Horse racing landing page or event details page.
        EXPECTED: User should be successfully logged in the HR landing page or event details page.
        """
        self.navigate_to_page("/")
        self.site.login()
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")
        result = self.site.horse_racing.has_my_stable_icon()
        self.assertTrue(result, msg=f'"my stable" entry point is not shown in horse racing landing page in logged in state')
        self.site.horse_racing.my_stable_icon.click()
        self.site.wait_content_state("My Stable")
        # checking whether there is existing bookmarks in "mys stable" page
        # if there is any bookmarks making "my stable" page empty
        if not self.site.my_stable.has_view_todays_races():
            self.assertTrue(self.site.my_stable.edit_stable.is_displayed(),
                            msg=f'Edit my stable link is not display in my stable page')
            self.site.my_stable.edit_stable.click()
            race_cards = self.site.my_stable.items_as_ordered_dict
            for race_name, race in list(race_cards.items()):
                race.clear_bookmark()

    def test_002_click_on_the_entry_point_on_the_horse_racing_landing_page_or_the_event_details_page(self):
        """
        DESCRIPTION: Click on the entry point on the Horse racing landing page or the event details page.
        EXPECTED: User should be redirected to the My Stable page which is empty.
        EXPECTED: 1. The icon which is configured in the CMS should be displayed on the page.
        EXPECTED: 2. The empty stable header should be displayed as configured in the CMS 'Stable Empty'.
        EXPECTED: 3. The empty stable message label should be displayed as configured in the CMS 'Tap on 'Edit Stable' on the Race Card to add a horse'.
        EXPECTED: 4. The text on the CTA button should be as configured in the CMS 'VIEW TODAY'S RACES'.
        EXPECTED: ![](index.php?/attachments/get/8e3f0c7b-f5b0-42b9-b7d2-6706bace684e) ![](index.php?/attachments/get/267038d4-0474-4030-b77c-066713f9f7b7)
        """
        # verifying whether "Empty Stable" Svg Icon is displayed in "my stable" page ot not
        self.assertTrue(self.site.my_stable.has_no_favorite_horses_icon, msg=f'"no favorite horses icon" was not displaying in my stable empty page')
        # verifying whether "Empty Stable Header Label" is displayed in "my stable" page ot not
        self.assertTrue(self.site.my_stable.has_no_favorite_horses_label,
                        msg=f'"no favorite horses icon" was not displaying in my stable empty page')
        actual_stable_empty_text = self.site.my_stable.no_favorite_horses_label_text.upper()
        self.assertEqual(actual_stable_empty_text, self.expected_stable_empty_text,
                         msg=f'actual {actual_stable_empty_text} is not equal to expected {self.expected_stable_empty_text}')
        # verifying whether "Empty Stable Message Label" is displayed in "my stable" page ot not
        self.assertTrue(self.site.my_stable.has_no_favorite_horses_info,
                        msg=f'"no favorite horses info" was not displaying in my stable empty page')
        actual_empty_stable_message_label = self.site.my_stable.no_favorite_horses_info_text.upper()
        self.assertEqual(actual_empty_stable_message_label, self.expected_empty_stable_message_label,
                         msg=f'actual {actual_empty_stable_message_label} is not equal to expected {self.expected_empty_stable_message_label}')
        # verifying whether "Empty Stable CTA Label" is displayed in "my stable" page ot not
        actual_view_todays_races_cta_button_text = self.site.my_stable.has_view_todays_races_text.upper()
        self.assertEqual(actual_view_todays_races_cta_button_text, self.expected_view_todays_races_cta_button_text,
                         msg=f'actual {actual_view_todays_races_cta_button_text} is not equal to expected {self.expected_view_todays_races_cta_button_text}')
        # clicking on "view todays races" cta button
        view_todays_races_cta_button = self.site.my_stable.view_todays_races
        view_todays_races_cta_button.click()

    def test_003_click_on_the_view_todays_races_button(self):
        """
        DESCRIPTION: Click on the 'VIEW TODAY'S RACES' button.
        EXPECTED: User should be redirected to the Horse racing landing page.
        """
        self.site.wait_content_state("HorseRacing")
