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
class Test_C2745934_Verify_Google_Tracking_of_International_Tote_Race(Common):
    """
    TR_ID: C2745934
    NAME: Verify Google Tracking of International Tote Race
    DESCRIPTION: This test case verifies Google Analytics tracking of International Tote Race
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: International Tote Races are available.
    PRECONDITIONS: International Tote Races Carousel is present below UK Races
    PRECONDITIONS: ***User is on Horse racing landing page.***
    """
    keep_browser_open = True

    def test_001_tap_on_any_of_the_race_in_the_carousel(self):
        """
        DESCRIPTION: Tap on any of the Race in the carousel
        EXPECTED: Race card of respective Meeting is opened
        """
        pass

    def test_002_open_developments_tool__console_and_perform_datalayer_command(self):
        """
        DESCRIPTION: Open developments tool > console and perform **dataLayer** command
        EXPECTED: The following has been recorded in **dataLayer**:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'tote carousel',
        EXPECTED: 'eventLabel' : '<< Event name / time >>'
        EXPECTED: })
        """
        pass
