import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28533_Half_Time_Full_Time_market_section(Common):
    """
    TR_ID: C28533
    NAME: Half Time/Full Time market section
    DESCRIPTION: This test case verifies 'Half Time/Full Time market section' market section on Event Details Page
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half Time / Full Time"
    PRECONDITIONS: *   PROD: name="|Half-Time/Full-Time|"
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_half_timefull_time_market_section(self):
        """
        DESCRIPTION: Go to 'Half Time/Full Time' market section
        EXPECTED: *   Section is present on Event Details Page and titled 'Half Time/Full Time market section'
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Selection name corresponds to part of '**name**' attribute on the market level
        EXPECTED: **NOTE** "Result" or "Result Market" can be added in the end of some market names  - this expected and hardcoded
        EXPECTED: e.g. ***Half Time / Full Time Result Market***
        """
        pass

    def test_005_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If 'Half Time/Full Time' market section has **cashoutAvail="Y"** then label Cash out should be displayed next to market section name
        """
        pass

    def test_006_expandhalf_timefull_time_market_section(self):
        """
        DESCRIPTION: Expand 'Half Time/Full Time' market section
        EXPECTED: The list of available selections received from SS response are displayed within market section
        """
        pass

    def test_007_verify_half_timefull_time_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Half Time/Full Time' section in case of data absence
        EXPECTED: 'Half Time/Full Time' section is not shown if:
        EXPECTED: *   market is absent
        EXPECTED: *   there are no outcomes within the market
        """
        pass
