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
class Test_C28540_Need_to_be_updatedScorecast_market_section_presence(Common):
    """
    TR_ID: C28540
    NAME: [Need to be updated]Scorecast market section presence
    DESCRIPTION: *FOR UPDATE NOTE*
    DESCRIPTION: - Test case lacks instructions on how to PROPERLY prepare or identify data needed for this test - therefore it is impossible to determine wheter test failed or data was incorrect.
    DESCRIPTION: - Step 11 expected result is VAGUE and is impossible to determine what the outcome is supposed to be. How many of all is some? Test need to check for specific outcome for specific input, and if there is some freedom in how data can be prepared the boundaries need to be specified (eg. 2 out of X possible markets, where possible markets are specified)
    DESCRIPTION: This test case verifies Scorecast market section presence.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Scorecast is applicable ONLY for Pre-March Football events
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Goalscorer"
    PRECONDITIONS: *   PROD: name="First Goal Scorer"
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootballicon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_003_open_event_detail_page_of_pre_match_football_event(self):
        """
        DESCRIPTION: Open Event Detail Page of Pre-Match Football event
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: * FOR CORAL: 'Main Markets' collection is selected by default
        EXPECTED: * FOR LADBROKES: 'All Markets' collection is selected by default (BMA-45315)
        """
        pass

    def test_004_verify_scorecast_market_section_presence(self):
        """
        DESCRIPTION: Verify Scorecast market section presence
        EXPECTED: Scorecast market section is shown after 'Correct Score' market only if the following markets exist:
        EXPECTED: *   name="First Goal Scorecast" and/or name="Last Goal Scorecast"
        EXPECTED: *   name="Firs Goalscorer" and/or "Last Goalscorer"
        EXPECTED: *   name="Correct Score"
        """
        pass

    def test_005_navigate_to_all_markets_collectioncoral(self):
        """
        DESCRIPTION: Navigate to 'All Markets' collection (CORAL)
        EXPECTED: *   'All Markets' collection is selected
        EXPECTED: *   All available markets for verified event are shown
        """
        pass

    def test_006_verify_scorecast_market_section_presence(self):
        """
        DESCRIPTION: Verify Scorecast market section presence
        EXPECTED: Scorecast market section is shown after 'Correct Score' market only if it is available in 'Main Markets' collection
        """
        pass

    def test_007_verify_cash_out_label_next_to_scorecast_market(self):
        """
        DESCRIPTION: Verify Cash out label next to Scorecast Market
        EXPECTED: If one of markets (First Goal Scorecast/Last Goal Scorecast) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_008_verify_scorecast_market_section_presence_in_other_collections(self):
        """
        DESCRIPTION: Verify Scorecast market section presence in other collections
        EXPECTED: Scorecast market section and related markets (name="|First Goal Scorecast|" and/or name="|Last Goal Scorecast|") are not shown in any other collections
        """
        pass

    def test_009_open_event_detail_page_of_in_play_football_event(self):
        """
        DESCRIPTION: Open Event Detail Page of In-Play Football event
        EXPECTED: * Football Event Details page is opened
        EXPECTED: * FOR CORAL: 'Main Markets' collection is selected by default
        EXPECTED: * FOR LADBROKES: 'All Markets' collection is selected by default (BMA-45315)
        """
        pass

    def test_010_verify_scorecast_market_section_presence(self):
        """
        DESCRIPTION: Verify Scorecast market section presence
        EXPECTED: Scorecast market section is NOT available for In-Play events
        """
        pass

    def test_011_verify_scorecast_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Scorecast' section in case of data absence
        EXPECTED: 'Scorecast' section is not shown if:
        EXPECTED: *   some/all markets that section consists of are absent
        EXPECTED: *   some/all markets that section consists of do not have outcomes
        """
        pass
