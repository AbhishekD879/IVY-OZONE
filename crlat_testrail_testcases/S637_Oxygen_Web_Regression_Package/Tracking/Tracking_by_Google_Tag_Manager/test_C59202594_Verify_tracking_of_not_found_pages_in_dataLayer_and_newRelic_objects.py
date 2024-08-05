import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59202594_Verify_tracking_of_not_found_pages_in_dataLayer_and_newRelic_objects(Common):
    """
    TR_ID: C59202594
    NAME: Verify tracking of not-found pages in dataLayer and newRelic objects.
    DESCRIPTION: This test case verifies tracking of not-found pages (any invalid pages, invalid event id and sport pages) in the Google Analytic's data Layer and NewRelic objects.
    PRECONDITIONS: 1. dataLayer and newRelic should be enabled for environment under test, else data can be tracked in dataLayerEvents and newRelicEvents objects.
    PRECONDITIONS: 2. Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application.
        EXPECTED: Home page is opened.
        """
        pass

    def test_002_add_to_existing_url_invalidpage_and_tap_enter(self):
        """
        DESCRIPTION: Add to existing URL '/InvalidPage' and tap 'Enter'.
        EXPECTED: User is redirected to the Home page.
        """
        pass

    def test_003_type_in_browser_console_datalayernewrelic_and_tap_enter_not_simultaneously_first_check_one_object_then_another_object(self):
        """
        DESCRIPTION: Type in browser console "dataLayer"/"newRelic" and tap 'Enter' (not simultaneously, first check one object, then another object).
        EXPECTED: The following event with corresponding parameters is present:
        EXPECTED: - in Data Layer:
        EXPECTED: {event:'not-found-page',
        EXPECTED: location: "general",
        EXPECTED: activeUrl: "/currentUrl",
        EXPECTED: previousUrl: "/someUrl" }
        EXPECTED: );
        EXPECTED: - in NewRelic:
        EXPECTED: newRelicService.addPageAction('NotFoundPageHit')
        EXPECTED: Note:
        EXPECTED: activeUrl: invalid URL typed by user
        EXPECTED: previousUrl: URL from which user was redirected to activeURL
        """
        pass

    def test_004_add_to_existing_url_eventinvalideventid_and_tap_enter(self):
        """
        DESCRIPTION: Add to existing URL '/event/invalidEventId' and tap 'Enter'.
        EXPECTED: User is redirected to the Home page.
        """
        pass

    def test_005_type_in_browser_console_datalayernewrelic_and_tap_enter_not_simultaneously_first_check_one_object_then_another_object(self):
        """
        DESCRIPTION: Type in browser console "dataLayer"/"newRelic" and tap 'Enter' (not simultaneously, first check one object, then another object).
        EXPECTED: The following event with corresponding parameters is present:
        EXPECTED: - in Data Layer:
        EXPECTED: {event:'not-found-page',
        EXPECTED: location: "edp",
        EXPECTED: activeUrl: "/currentUrl",
        EXPECTED: previousUrl: "/someUrl" }
        EXPECTED: );
        EXPECTED: - in NewRelic:
        EXPECTED: newRelicService.addPageAction('NotFoundPageHit')
        EXPECTED: Note:
        EXPECTED: activeUrl: invalid URL typed by user
        EXPECTED: previousUrl: URL from which user was redirected to activeURL
        """
        pass

    def test_006_add_to_existing_url_sportinvalidsportname_and_tap_enter(self):
        """
        DESCRIPTION: Add to existing URL '/sport/invalidSportName' and tap 'Enter'.
        EXPECTED: User is redirected to the Home page.
        """
        pass

    def test_007_type_in_browser_console_datalayernewrelic_and_tap_enternot_simultaneously_first_check_one_object_then_another_object(self):
        """
        DESCRIPTION: Type in browser console "dataLayer"/"newRelic" and tap 'Enter'
        DESCRIPTION: (not simultaneously, first check one object, then another object).
        EXPECTED: The following event with corresponding parameters is present:
        EXPECTED: - in Data Layer:
        EXPECTED: {event:'not-found-page',
        EXPECTED: location: "slp",
        EXPECTED: activeUrl: "/currentUrl",
        EXPECTED: previousUrl: "/someUrl" }
        EXPECTED: );
        EXPECTED: - in NewRelic:
        EXPECTED: newRelicService.addPageAction('NotFoundPageHit')
        EXPECTED: Note:
        EXPECTED: activeUrl: invalid URL typed by user
        EXPECTED: previousUrl: URL from which user was redirected to activeURL
        """
        pass
