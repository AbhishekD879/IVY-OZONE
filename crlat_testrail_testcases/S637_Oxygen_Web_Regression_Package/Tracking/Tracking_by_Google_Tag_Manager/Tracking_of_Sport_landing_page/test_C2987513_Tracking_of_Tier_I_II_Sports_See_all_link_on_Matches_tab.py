import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2987513_Tracking_of_Tier_I_II_Sports_See_all_link_on_Matches_tab(Common):
    """
    TR_ID: C2987513
    NAME: Tracking of Tier I/II Sports 'See all link' on Matches tab
    DESCRIPTION: This test case verifies the GA tracking of clicking "See All" link on sport Matches tab (sport is Tier I or II type)
    PRECONDITIONS: 1. Sports Page > Sports Categories > <any sport> is enabled in CMS
    PRECONDITIONS: 2. User is on <sport> landing page: 'Matches' tab
    PRECONDITIONS: 3. Below 'In Play' module "See All" link is available for upcoming events for each type
    PRECONDITIONS: All sports that are tier I and II are listed here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    """
    keep_browser_open = True

    def test_001_click_on_see_all_link_in_upcoming_modules(self):
        """
        DESCRIPTION: Click on "See All" link (in upcoming modules)
        EXPECTED: User is redirected to Competition page of that league with all events available
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following tracking is displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'upcoming module',
        EXPECTED: 'eventAction' : '<< LOCATION >>',
        EXPECTED: 'eventLabel' : 'see all',
        EXPECTED: 'competitionName' : '<< COMPETITION NAME >>'
        EXPECTED: }
        """
        pass
