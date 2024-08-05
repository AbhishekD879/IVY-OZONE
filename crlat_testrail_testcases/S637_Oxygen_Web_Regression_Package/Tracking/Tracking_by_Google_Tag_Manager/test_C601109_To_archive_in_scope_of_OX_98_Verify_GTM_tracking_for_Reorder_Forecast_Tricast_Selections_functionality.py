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
class Test_C601109_To_archive_in_scope_of_OX_98_Verify_GTM_tracking_for_Reorder_Forecast_Tricast_Selections_functionality(Common):
    """
    TR_ID: C601109
    NAME: [To archive in scope of OX 98] Verify GTM tracking for Reorder Forecast/Tricast Selections functionality
    DESCRIPTION: This test case verifies GTM tracking for Reorder Forecast/Tricast Selections functionality in the Betslip
    PRECONDITIONS: Oxygen application is loaded
    PRECONDITIONS: Two and more Horse Racing selections from the same event and the same market are added to the Betslip
    PRECONDITIONS: Betslip is opened and Forecast/Tricast section is available
    """
    keep_browser_open = True

    def test_001_go_to_forecasttricast_section(self):
        """
        DESCRIPTION: Go to Forecast/Tricast section.
        EXPECTED: 
        """
        pass

    def test_002_change_position_for_few_selections_in_forecaststricasts_sectiondo_not_tap_done_text_linkverify_data_in_datalayer(self):
        """
        DESCRIPTION: Change position for few selections in Forecasts/Tricasts section.
        DESCRIPTION: Do Not tap 'Done' text link.
        DESCRIPTION: Verify data in DataLayer.
        EXPECTED: There is no tracking data for selections positions changing
        """
        pass

    def test_003_tap_done_text_linkverify_data_in_datalayer(self):
        """
        DESCRIPTION: Tap 'Done' text link.
        DESCRIPTION: Verify data in DataLayer.
        EXPECTED: Following data is displayed:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'Re-order selections',
        EXPECTED: 'eventLabel' : 'Re-order selections',
        """
        pass
