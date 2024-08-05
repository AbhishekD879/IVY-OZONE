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
class Test_C28977_Verify_data_for_Results_tab___To_be_archived(Common):
    """
    TR_ID: C28977
    NAME: Verify data for 'Results' tab  -  To be archived
    DESCRIPTION: This test case verifies data which is displayed in the 'Results' tab
    DESCRIPTION: NOTE, UAT assistance is needed for configuration of racing results.
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To verify Results for events use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **startTime** - to verify event start date
    PRECONDITIONS: **typeFlagCodes** - to identify group the event belongs to
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_on_the_homepage_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On the homepage tap 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: 1.  'Greyhounds' landing page is opened
        EXPECTED: 2.  'Today tab' tab is displayed
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: 'Results' tab is opened
        EXPECTED: **'By Latest Results' **sorting type is selected by default
        """
        pass

    def test_004_verify_data_which_is_displayed_in_results_tab(self):
        """
        DESCRIPTION: Verify data which is displayed in 'Results' tab
        EXPECTED: Results are displayed ONLY for today's events (see '**startTime'** attribute)
        """
        pass

    def test_005_verify_events_which_are_shown_in_the_results_tab(self):
        """
        DESCRIPTION: Verify events which are shown in the 'Results' tab
        EXPECTED: Only events which have results available are shown on the 'Results' tab (**'isResulted'=**'true' attibute is present)
        """
        pass

    def test_006_verify_price_type_for_events_on_results_tab(self):
        """
        DESCRIPTION: Verify price type for events on 'Results' tab
        EXPECTED: Events ONLY with the following price types are shown on the 'Results' tab:
        EXPECTED: *   **priceTypeCodes=**'SP'
        EXPECTED: *   **priceTypeCodes=**'LP,SP'
        """
        pass

    def test_007_verify_event_with_pricetypecodeslp(self):
        """
        DESCRIPTION: Verify event with** 'priceTypeCodes'**=LP
        EXPECTED: Events with 'LP' price type are NOT shown on the 'Results' tab
        """
        pass
