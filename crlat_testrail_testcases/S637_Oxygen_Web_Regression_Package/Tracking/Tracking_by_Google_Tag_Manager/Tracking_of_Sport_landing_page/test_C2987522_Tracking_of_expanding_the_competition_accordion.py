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
class Test_C2987522_Tracking_of_expanding_the_competition_accordion(Common):
    """
    TR_ID: C2987522
    NAME: Tracking of expanding the competition accordion
    DESCRIPTION: This test case verifies the GA tracking of expanding the competition accordion on Matches tab (sport is Tier I or II type)
    PRECONDITIONS: 1. Sports Page > Sports Categories > <any sport> is enabled in CMS
    PRECONDITIONS: 2. User is on <sport> landing page: 'Matches' tab
    PRECONDITIONS: 3. Upcoming events are available on sports landing page
    PRECONDITIONS: All sports that are tier I and II are listed here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    """
    keep_browser_open = True

    def test_001_on_matches_tab_expand_any_type_competition_accordion_that_are_collapsed_by_default_at_the_bottom_of_the_page(self):
        """
        DESCRIPTION: On Matches tab expand any type (competition) accordion that are collapsed by default (at the bottom of the page)
        EXPECTED: Accordion becomes expanded
        """
        pass

    def test_002_type_in_browser_console_datalayerand_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer"and tap 'Enter'
        EXPECTED: The following tracking is fired:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent', 'eventCategory' : 'upcoming module', 'eventAction' : '<< LOCATION >>', 'eventLabel' : 'expand' }
        """
        pass
