import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C29172_TO_EDITLeagues_Type_Names_with_Cash_Out_option_available(Common):
    """
    TR_ID: C29172
    NAME: TO EDIT:Leagues/Type Names with Cash Out option available
    DESCRIPTION: This test case verifies Leagues/Type Names with Cash Out option available on Event Landing Pages.
    DESCRIPTION: **Jira tickets**:
    DESCRIPTION: * BMA-2942, BMA-3925
    DESCRIPTION: * [BMA-17707 (Remove Cash Out icons from the accordions on the Outrights tab)][1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-17707
    PRECONDITIONS: 1. In order to check **Type **data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XX - Sport/Category ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. In order to get the list of **Sports **use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: **Currently ****CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_sport_landing_page(self):
        """
        DESCRIPTION: Open <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_verify_typesleagues_with_cash_out_label(self):
        """
        DESCRIPTION: Verify Types/Leagues with 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is shown next to event Type name if at least one of its events has cashoutAvail="Y" and on all higher levels cashoutAvail="Y"
        """
        pass

    def test_004_verify_cash_out_label_on_event_section_under_league_section(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label on Event section under League section
        EXPECTED: 'CASH OUT' label is not shown on Event section
        """
        pass

    def test_005_navigate_to_outrights_tab(self):
        """
        DESCRIPTION: Navigate to Outrights tab
        EXPECTED: 
        """
        pass

    def test_006_verify_typesleagues_with_cash_out_label(self):
        """
        DESCRIPTION: Verify Types/Leagues with 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is **NOT** shown
        """
        pass

    def test_007_open_race_langing_page(self):
        """
        DESCRIPTION: Open <Race> Langing page
        EXPECTED: *   <Race> Landing Page is opened
        EXPECTED: *   'Today' tab is selected by default
        EXPECTED: *   'By Meeting' is selected by default
        """
        pass

    def test_008_verify_race_types_with_cash_out_label(self):
        """
        DESCRIPTION: Verify Race Types with 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is shown next to event Type name if at least one of it's events has cashoutAvail="Y
        """
        pass

    def test_009_tap_by_time_sorting_type_and_verify_cash_out_label(self):
        """
        DESCRIPTION: Tap 'By Time' sorting type and verify 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is not shown on Event section
        """
        pass

    def test_010_verify_types_without_cash_out_label_on_sportsraces(self):
        """
        DESCRIPTION: Verify Types without 'CASH OUT' label on <Sports>/<Races>
        EXPECTED: These Types have
        EXPECTED: *   **cashoutAvail="N" **on type/market level OR
        EXPECTED: *   **cashoutAvail **attribute is absent on type/market level
        """
        pass
