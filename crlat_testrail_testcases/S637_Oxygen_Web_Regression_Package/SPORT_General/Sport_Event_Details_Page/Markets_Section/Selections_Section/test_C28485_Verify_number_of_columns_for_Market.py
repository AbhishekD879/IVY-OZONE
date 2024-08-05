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
class Test_C28485_Verify_number_of_columns_for_Market(Common):
    """
    TR_ID: C28485
    NAME: Verify number of columns for Market
    DESCRIPTION: Verify number of columns for particular Market displaying.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Please check the Number of Columns per Display Sort Name in the table using the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Generic+Sport+Template+-+Selections+Display+Rules
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_clicktap_on_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Click/Tap on Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_go_to_verified_market_section(self):
        """
        DESCRIPTION: Go to verified Market section
        EXPECTED: It is possible to collapse/expand Market sections by clicking/tapping the accordions
        """
        pass

    def test_005_check_presence_and_value_ofdispsortname_attribute_of_verified_market_using_the_first_link_from_preconditions(self):
        """
        DESCRIPTION: Check presence and value of **dispSortName** attribute of verified Market using the first link from Preconditions
        EXPECTED: *   If **dispSortName **tag is available -> go to step №6
        EXPECTED: *   If **dispSortName **tag is NOT available -> go to step №7
        """
        pass

    def test_006_find_correspondingdispsortnamein_the_table_using_the_second_link_from_preconditions(self):
        """
        DESCRIPTION: Find corresponding **dispSortName **in the table using the second link from Preconditions
        EXPECTED: Number of columns found in the table corresponds to number of columns displayed on front-end for verified Market
        """
        pass

    def test_007_verify_number_of_selections_in_such_market(self):
        """
        DESCRIPTION: Verify number of selections in such Market
        EXPECTED: *   1-6 selections within Market -> they are displayed in **ONE **column
        EXPECTED: *   6-24 selections -> Market selections are displayed in **TWO **columns
        EXPECTED: *   More than 24 selections -> Market selections are displayed in **THREE **columns
        """
        pass

    def test_008_repeat_steps_4_5_for_several_different_markets(self):
        """
        DESCRIPTION: Repeat steps №4-5 for several different Markets
        EXPECTED: 
        """
        pass
