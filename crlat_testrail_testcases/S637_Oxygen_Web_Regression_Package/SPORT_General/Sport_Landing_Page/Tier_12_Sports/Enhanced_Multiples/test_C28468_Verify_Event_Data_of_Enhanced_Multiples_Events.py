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
class Test_C28468_Verify_Event_Data_of_Enhanced_Multiples_Events(Common):
    """
    TR_ID: C28468
    NAME: Verify Event Data of Enhanced Multiples Events
    DESCRIPTION: This test case verifies Event Data of Enhanced Multiples Events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **NOTE: Make sure you have  Enhanced Multiples events on Some sports (Sport events with typeName="Enhanced Multiples").**
    PRECONDITIONS: In order to check particular event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: Make sure you have <Sport> Enhanced Multiples events (events with **drilldownTagNames="EVFLAG_ES**")
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_any_ltsportsgt_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to any &lt;Sports&gt; page where Enhanced Multiples events are present
        EXPECTED: **Desktop**:
        EXPECTED: *  &lt;Sport&gt; Landing Page is opened
        EXPECTED: * 'Matches'-&gt;'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  &lt;Sport&gt; Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_go_to_outcome_section_of_em_event(self):
        """
        DESCRIPTION: Go to outcome section of EM event
        EXPECTED: Enhanced Multiples outcome is shown
        """
        pass

    def test_004_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection name
        EXPECTED: Selection name corresponds to **name** attribute on Outcome level
        """
        pass

    def test_005_verify_outcome_start_time_for_mobiletablet(self):
        """
        DESCRIPTION: Verify Outcome Start Time for **Mobile/Tablet**
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown below Outcome name
        EXPECTED: *   For outcomes that occur Today date format is 24 hours: **HH:MM, Today** (e.g. "14:00 or 05:00, Today")
        EXPECTED: *   For outcomes that occur in the future (including tomorrow) date format is 24 hours: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        pass

    def test_006_verify_outcome_start_time_for_desktop(self):
        """
        DESCRIPTION: Verify Outcome Start Time for **Desktop**
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown after Outcome name in the same row
        EXPECTED: *   For outcomes that occur Today date format is 24 hours: **HH:MM, Today** (e.g. 14:00 or 05:00)
        EXPECTED: *   For outcomes that occur in the future (including tomorrow) date format is 24 hours: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        pass

    def test_007_clicktap_onanywhere_on_outcome_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Click/Tap on anywhere on Outcome section (except for price buttons)
        EXPECTED: Outcome section is not clickable
        """
        pass

    def test_008_verify_data_of_priceodds_button_for_verified_outcome_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button for verified outcome in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen ** if **eventStatusCode="A"**
        EXPECTED: *   Disabled 'Price/Odds' button is displayed and corresponds to the **priceNum/priceDen ** if **eventStatusCode="S"**
        """
        pass

    def test_009_verify_data_of_priceodds_for_verified_outcome_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified outcome in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec ** if **eventStatusCode="A"**
        EXPECTED: *   Disabled 'Price/Odds' button is displayed and corresponds to the **priceNum/priceDen ** if **eventStatusCode="S"**
        """
        pass

    def test_010_navigate_to_tomorrowfuture_tab_on_desktoptablet_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to Tomorrow/Future tab on Desktop/Tablet where Enhanced Multiples events are present
        EXPECTED: * Enhanced Multiples section for **Mobile/Tablet**
        EXPECTED: * The EM carousel is still displaying with all available outcomes for **Desktop**
        EXPECTED: * The EM carousel is not reloaded during navigation between days (Today/Tomorrow/Future) for **Desktop**
        """
        pass

    def test_011_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps 3-8
        EXPECTED: 
        """
        pass

    def test_012_clicktap_on_enhanced_multiples_tab_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Click/Tap on 'Enhanced Multiples' tab from Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        pass

    def test_013_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps №3-9
        EXPECTED: 
        """
        pass

    def test_014_for_desktoprepeat_steps_3_9_on_ltsportsgt_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-9 on &lt;Sports&gt; Event Details Page but only for Pre-match events
        EXPECTED: 
        """
        pass
