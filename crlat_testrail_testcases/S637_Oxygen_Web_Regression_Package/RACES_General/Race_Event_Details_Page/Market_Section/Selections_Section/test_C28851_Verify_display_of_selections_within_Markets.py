import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28851_Verify_display_of_selections_within_Markets(Common):
    """
    TR_ID: C28851
    NAME: Verify display of selections within Markets
    DESCRIPTION: This test case verifies display of selections within different Markets
    PRECONDITIONS: **JIRA Ticket** : BMA-6584 'Racecard Layout Update - Horse Information'
    PRECONDITIONS: BMA-18626'Replace Generic Silks with Race Card Number Design (Racing)'
    PRECONDITIONS: NOTE : all information about <Race> and Runner is displayed only if it is mapped
    PRECONDITIONS: NOTE 2: Timeform will be not used for Ladbrokes. Racing post data will be displayed instead. This is from comment in BMA-44480
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon on the Sports Menu Ribbon
        EXPECTED: <Race> Landing Page is opened
        """
        pass

    def test_003_tap_event_name_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name on the Event section
        EXPECTED: *   <Race> Event Details page is opened
        EXPECTED: *   'Win or E/W' market is selected by default
        """
        pass

    def test_004_go_to_race_event_selection_area_where_silks_are_mapped(self):
        """
        DESCRIPTION: Go to <Race> Event Selection area where SILKS are mapped
        EXPECTED: * Correct silks are displayed for mapped selections (silkName)
        EXPECTED: * Generic silks are displayed for missed selections
        """
        pass

    def test_005_clicks_within_the_race_event_selection_area_or_on_the_arrow_on_the_left_side(self):
        """
        DESCRIPTION: Clicks within the <Race> Event Selection area (or on the arrow on the left side)
        EXPECTED: *   Runner information is expanded showing information about the runner
        EXPECTED: *  For HR: Spotlight text is present
        EXPECTED: *  For GH: Timeform summary with rating starts are present
        """
        pass

    def test_006_click_on_the_other_race_event_selection_area(self):
        """
        DESCRIPTION: Click on the other <Race> Event Selection area
        EXPECTED: *   First runner information is collapsed and a new one is expanded
        """
        pass

    def test_007_only_for_horses_go_to_race_event_selection_area_where_no_silks_mapped(self):
        """
        DESCRIPTION: ONLY FOR HORSES: Go to <Race> Event Selection area where no SILKS mapped
        EXPECTED: * NO Generic Pictures, Horse Name, price/Odds and Previous Odds under Price/Odds button are displayed
        EXPECTED: * Only runner numbers are displayed
        """
        pass
