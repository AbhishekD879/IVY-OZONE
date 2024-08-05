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
class Test_C28486_Verify_ordering_of_selections_within_Markets(Common):
    """
    TR_ID: C28486
    NAME: Verify ordering of selections within Markets
    DESCRIPTION: This test case verifies ordering of selections in different Markets
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Please check the Selections Order per Display Sort Name in the table using the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Generic+Sport+Template+-+Selections+Display+Rules
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_ltsportgticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '&lt;Sport&gt;'  icon on the Sports Menu Ribbon
        EXPECTED: 'Sport' Landing Page is opened
        """
        pass

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: &lt;Sport&gt; Event Details page is opened
        """
        pass

    def test_004_go_to_verified_market_section(self):
        """
        DESCRIPTION: Go to verified Market section
        EXPECTED: It is possible to collapse/expand Market sections by tapping the section's header
        """
        pass

    def test_005_check_presence_and_value_ofdispsortnameattribute_of_verified_market_using_first_link_from_preconditions(self):
        """
        DESCRIPTION: Check presence and value of **dispSortName **attribute of verified Market using first link from Preconditions
        EXPECTED: *   If **dispSortName **tag is available -&gt; go to step №6
        EXPECTED: *   If **dispSortName **tag is NOT available -&gt; go to step №9
        """
        pass

    def test_006_check_presence_and_value_ofoutcomemeaningminorcode_attributes_of_selections_within_verified_market(self):
        """
        DESCRIPTION: Check presence and value of **outcomeMeaningMinorCode **attributes of selections within verified Market
        EXPECTED: *   If **outcomeMeaningMinorCode **tags are available -&gt; go to step №7
        EXPECTED: *   If **outcomeMeaningMinorCode **tags are not available -&gt; go to step №8
        """
        pass

    def test_007_find_corresponding_to_verified_marketdispsortnamein_the_table_using_the_second_link_from_preconditions(self):
        """
        DESCRIPTION: Find corresponding to verified Market **dispSortName **in the table using the second link from Preconditions
        EXPECTED: Selections order found in the table corresponds to selections order displayed on front-end for verified Market based on **outcomeMeaningMinorCode **tag
        EXPECTED: (e.g.H-left side, A-right side, D,N,L-middle)
        """
        pass

    def test_008_checkdisplayorder_attributeof_selections_within_verified_market(self):
        """
        DESCRIPTION: Check **displayOrder **attribute of selections within verified Market
        EXPECTED: Selections are ordered by **displayOrder **tag value of selections in ascending order
        """
        pass

    def test_009_check_prices_of_selections_within_verified_market(self):
        """
        DESCRIPTION: Check prices of selections within verified Market
        EXPECTED: *   Selections are ordered **by price** in ascending order
        EXPECTED: *   If Price is the same for two or more selections - selections are ordered **alphabetically**
        """
        pass

    def test_010_repeat_steps_4_5_for_several_different_markets(self):
        """
        DESCRIPTION: Repeat steps №4-5 for several different Markets
        EXPECTED: 
        """
        pass
