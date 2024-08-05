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
class Test_C60064480_Tracking_of_Selecting_Deselecting_Time_League_filter(Common):
    """
    TR_ID: C60064480
    NAME: Tracking of Selecting/Deselecting Time/League filter
    DESCRIPTION: This Test Case verified tracking in the Google Analytic's data Layer when Time/League filters are selected/deselected
    PRECONDITIONS: Filters configuration:
    PRECONDITIONS: * 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page (Today Tab)
    PRECONDITIONS: 3. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “league filters", eventAction: ${CMS Button Name} e.g. Top Leagues eventLabel: ${‘select'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_003_click_selected_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Click selected League Filter (e.g. 'Top Leagues')
        EXPECTED: * Filter is not highlighted
        EXPECTED: * Page loads all events
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “league filters", eventAction: ${CMS Button Name} e.g. Top Leagues eventLabel: ${'deselect'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_005_select_some_time_filter_eg_3h(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. ‘3h’)
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events that are due to start within the next 3 hours for that given Sport
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “time filters", eventAction: ${CMS Button Name} e.g. 3h eventLabel: ${‘select'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_007_click_selected_time_filter_eg_3h(self):
        """
        DESCRIPTION: Click selected Time Filter (e.g. ‘3h’)
        EXPECTED: * Filter is not highlighted
        EXPECTED: * Page loads all events
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “time filters", eventAction: ${CMS Button Name} e.g. 3h eventLabel: ${'deselect'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_009_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “league filters", eventAction: ${CMS Button Name} e.g. Top Leagues eventLabel: ${‘select'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_011_click_another_league_filter_eg_test_league(self):
        """
        DESCRIPTION: Click another League Filter (e.g. ’Test League')
        EXPECTED: * Previous filter is not highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        """
        pass

    def test_012_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “league filters", eventAction: ${CMS Button Name} e.g. Test League eventLabel: ${‘select'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_013_select_some_time_filter_eg_3h(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. ‘3h’)
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are due to start within the next 3 hours AND that are in line to selected League Filter
        """
        pass

    def test_014_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “time filters", eventAction: ${CMS Button Name} e.g. 3h eventLabel: ${‘select'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_015_click_another_time_filter_eg_1h(self):
        """
        DESCRIPTION: Click another Time Filter (e.g. ‘1h’)
        EXPECTED: * Previous filter is not highlighted
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are due to start within the next 1 hours AND that are in line to selected League Filter
        """
        pass

    def test_016_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “time filters", eventAction: ${CMS Button Name} e.g. 1h eventLabel: ${'select'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_017_click_selected_time_filter_eg_1h(self):
        """
        DESCRIPTION: Click selected Time Filter (e.g. ‘1h’)
        EXPECTED: * Time Filter is not highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter
        """
        pass

    def test_018_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “time filters", eventAction: ${CMS Button Name} e.g. 3h eventLabel: ${'deselect'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass

    def test_019_click_selected_league_filter_eg_test_league(self):
        """
        DESCRIPTION: Click selected League Filter (e.g. ‘Test League')
        EXPECTED: * Filter is not highlighted
        EXPECTED: * Page loads all events
        """
        pass

    def test_020_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: datalayer.push({ event: "trackEvent", eventCategory: “league filters", eventAction: ${CMS Button Name} e.g. Top Leagues eventLabel: ${'deselect'}, categoryID: $"
        EXPECTED: {Sport}
        EXPECTED: " e.g. 16 })
        """
        pass
