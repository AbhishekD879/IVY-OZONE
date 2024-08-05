import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


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
class Test_C66039858_Verify_the_entry_points_for_My_Stable_in_Horse_racing_landing_page_and_event_details_page(
    BaseRacing):
    """
    TR_ID: C66039858
    NAME: Verify the entry points for My Stable in Horse racing landing page and event details page.
    DESCRIPTION: This test case evaluates the entry points for accessing the Stable screen in the Horse racing landing page and the HR events details pages.
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
    keep_browser_open = True

    def test_001_navigate_to_the_horse_racing_landing_page_without_logging_in_the_application(self):
        """
        DESCRIPTION: Navigate to the Horse racing landing page without logging in the application.
        EXPECTED: 1. User should be able to navigate to the Horse racing landing page successfully.
        EXPECTED: 2. User should not be able to view the Stable entry point in the HR landing page.
        EXPECTED: (Ladbrokes: Stable Mates ; Coral: My Stable)
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
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")
        result = self.site.horse_racing.has_my_stable_icon(expected_result=False)
        self.assertFalse(result, msg="my stable entry point is shown in horse racing landing page in logged out state ")

    def test_002_login_with_valid_credentials_and_observe_that_the_entry_point_is_visible_on_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Login with valid credentials and observe that the entry point is visible on the Horse racing landing page.
        EXPECTED: The entry point should be displayed on the Horse racing landing page through which user can access the Stable page.
        EXPECTED: 1. Ladbrokes: Stable Mates.
        EXPECTED: 2. Coral: My Stable.
        EXPECTED: ![](index.php?/attachments/get/6ba38561-a289-421a-ba1c-c3d68d37bd11) ![](index.php?/attachments/get/4c951e91-7aee-4949-9ff5-943d9e5a58f7)
        """
        self.navigate_to_page("/")
        self.site.login()
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")
        result = self.site.horse_racing.has_my_stable_icon(expected_result=True)
        self.assertTrue(result,
                        msg="my stable entry point is not shown in horse racing landing page in loggedin state ")

        self.site.horse_racing.my_stable_link.click()
        self.site.wait_content_state('my-stable')

        bypass_exceptions = (NoSuchElementException, StaleElementReferenceException, VoltronException)
        wait_for_result(lambda: self.site.back_button.click() is None, bypass_exceptions=bypass_exceptions)
        self.site.wait_content_state('HorseRacing')

    def test_003_navigate_to_the_various_horse_racing_event_details_page_non_uk_amp_irish_races_as_well_and_observe_the_entry_points(self):
        """
        DESCRIPTION: Navigate to the various horse racing event details page non UK &amp; Irish races as well and observe the Entry points.
        EXPECTED: The entry point should be displayed on the Horse racing event details pages through which user can access the Stable page.
        EXPECTED: 1. Ladbrokes: Stable Mates.
        EXPECTED: 2. Coral: My Stable.
        EXPECTED: ![](index.php?/attachments/get/230e341f-91ec-425b-8c05-f302044a4360) ![](index.php?/attachments/get/047e7e0a-9e5b-4eb4-97b7-7c5386078016)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        result = self.site.racing_event_details.has_my_stable_icon(expected_result=True)
        self.assertTrue(result,
                        msg="my stable entry point is not shown in horse racing event detail page in loggedin state ")

        self.site.racing_event_details.my_stable_link.click()
        self.site.wait_content_state('my-stable')

        bypass_exceptions = (NoSuchElementException, StaleElementReferenceException, VoltronException)
        wait_for_result(lambda: self.site.back_button.click() is None, bypass_exceptions=bypass_exceptions)
        self.site.wait_content_state('RACINGEVENTDETAILS')
