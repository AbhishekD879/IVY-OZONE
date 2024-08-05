import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28844_Verify_Disable_Non_Runners_Scratched_Horses_from_Bet_placement(Common):
    """
    TR_ID: C28844
    NAME: Verify Disable Non-Runners (Scratched) Horses from Bet placement
    DESCRIPTION: Verify Disable Non-Runners (Scratched) Horses
    PRECONDITIONS: Steps to set a Non-Runner Horse:
    PRECONDITIONS: In order to set a non runner, you just need to settle the selection as Void in the 'Set results' page in the http://backoffice-tst2.coral.co.uk/ti, and add the "N/R" text after the selection name (before you settle the selection).
    PRECONDITIONS: JIRA Tikets:
    PRECONDITIONS: BMA-10860 - Disable Non-Runners (Scratched) Horses From Bet Placement
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_horse_racing_section(self):
        """
        DESCRIPTION: Go to Horse Racing section
        EXPECTED: 'Races' Landing Page is opened
        """
        pass

    def test_003_open_event_details_page_with_non_runner_horses_available(self):
        """
        DESCRIPTION: Open event details page with Non-Runner Horses available
        EXPECTED: 'Race' Event Details page is opened
        """
        pass

    def test_004_verify_non_runner_horses_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify Non-Runner Horses displaying on the page
        EXPECTED: *   Any horse that is a Non-Runner is greyed out
        EXPECTED: *   Non-Runner horses are displayed in the last positions in the list but before the 'UNNAMED FAVOURITE'/UNNAMED 2nd FAVOURITE' sections
        """
        pass

    def test_005_tapclick_on_on_priceodds_for_non_runner(self):
        """
        DESCRIPTION: Tap/Click on on 'Price/Odds' for Non-Runner
        EXPECTED: *   'Price/Odds' is not clickable and marked as suspended
        EXPECTED: *    User cannot select or add Non-Runner horse selection to betslip
        """
        pass

    def test_006_verify_non_runners_horsers_ordering_when_there_are_few_of_them_available_for_the_single_event(self):
        """
        DESCRIPTION: Verify Non-Runners Horsers ordering when there are few of them available for the single event
        EXPECTED: *   All Non-Runner horses are displayed in the last positions in the list but before the 'UNNAMED FAVOURITE'/UNNAMED 2nd FAVOURITE' sections
        EXPECTED: *   Non-Runner Horses are ordered by running number in the list
        """
        pass

    def test_007_verify_race_information_section_availability_for_the_non_runner(self):
        """
        DESCRIPTION: Verify 'Race information' section availability for the Non-Runner
        EXPECTED: No 'Race information' section for Non-Runner selection
        """
        pass
