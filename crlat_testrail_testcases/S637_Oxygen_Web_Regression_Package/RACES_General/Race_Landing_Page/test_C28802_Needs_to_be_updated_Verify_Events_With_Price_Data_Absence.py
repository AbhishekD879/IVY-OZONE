import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28802_Needs_to_be_updated_Verify_Events_With_Price_Data_Absence(Common):
    """
    TR_ID: C28802
    NAME: [Needs to be updated] Verify Events With Price Data Absence
    DESCRIPTION: This test case verifies events without price data on <Race> landing/ details pages.
    PRECONDITIONS: 1. In order to retrieve all **Event** outcomes for the Classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: *
    PRECONDITIONS: XX - category id
    PRECONDITIONS: *
    PRECONDITIONS: ZZZZ is a comma separated list of Class ID's
    PRECONDITIONS: *   *YYYY1-MM1-DD1 is lower time bound*
    PRECONDITIONS: *   *YYYY2-MM2-DD2 is higher time bound*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. Find events with attributes **'priceTypeCodes'**='LP' and **'priceTypeCodes'**= 'LP,SP'
    PRECONDITIONS: 3. Price data is absent in outcome section (attributes '**priceNum'**, '**priceDen'** and **'priceDec' **are absent)
    """
    keep_browser_open = True

    def test_001_retrieve_the_list_of_events_for_verified_tab_use_time_intervalspecial_events_identifier(self):
        """
        DESCRIPTION: Retrieve the list of events for verified tab (use time interval/special event's identifier)
        EXPECTED: List of events are returned from siteserver
        """
        pass

    def test_002_find_events_with_attribure_pricetypecodeslp_but_withoutpricenumpricedenpricedec_attributes_in_outcome_section(self):
        """
        DESCRIPTION: Find events with attribure** 'priceTypeCodes'**='LP' but without **priceNum/priceDen/priceDec **attributes in outcome section
        EXPECTED: 
        """
        pass

    def test_003_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_004_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_005_go_to_verified_tabfor_horse_racing_featured_next_4_racesfor_greyhounds_today_tomorrow_future_next_4_races(self):
        """
        DESCRIPTION: Go to verified tab:
        DESCRIPTION: for **Horse Racing**: Featured, Next 4 Races
        DESCRIPTION: for **Greyhounds**: Today, Tomorrow, Future, Next 4 Races
        EXPECTED: Verified tab is opened
        """
        pass

    def test_006_check_list_of_events_on_races_homepage_when_by_meeting_sorting_type_is_selected(self):
        """
        DESCRIPTION: Check list of events on <Races> homepage when 'By Meeting' sorting type is selected
        EXPECTED: Event off times / list of race meetings are shown
        """
        pass

    def test_007_try_to_find_event_from_step_2(self):
        """
        DESCRIPTION: Try to find event from step #2
        EXPECTED: Events are shown on the <Race> landing page ('By Meeting' sorting type)
        """
        pass

    def test_008_check_list_of_events_on_race_landing_page_when_by_time_sorting_type_is_selected(self):
        """
        DESCRIPTION: Check list of events on <Race> landing page when 'By Time' sorting type is selected
        EXPECTED: A list of events with <Race> local times are shown
        """
        pass

    def test_009_try_to_find_event_from_step__2(self):
        """
        DESCRIPTION: Try to find event from step # 2
        EXPECTED: Event is shown on the <Race> landing page ('By Time' sorting type is selected)
        """
        pass

    def test_010_check_list_of_event_off_times_on_event_landing_page(self):
        """
        DESCRIPTION: Check list of event off times on event landing page
        EXPECTED: All events have price/odds buttons on it's event landing page
        """
        pass

    def test_011_try_to_find_events_from_step_2(self):
        """
        DESCRIPTION: Try to find events from step #2
        EXPECTED: Events are shown on the HR event landing page
        """
        pass

    def test_012_repeat_steps_1(self):
        """
        DESCRIPTION: Repeat steps #1
        EXPECTED: 
        """
        pass

    def test_013_on_site_server_find_an_event_with_attribute_pricetypecodeslpsp_but_prices_are_are_absent_for_outcomes(self):
        """
        DESCRIPTION: On Site Server find an event with attribute **'priceTypeCodes'**='LP,SP'  but prices are are absent for outcomes
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_3___6_and_step_8___find_events_with_incomplete_data(self):
        """
        DESCRIPTION: Repeat steps #3 - 6 and  step #8 -> find events with incomplete data
        EXPECTED: Events ARE shown
        """
        pass

    def test_015_repeat_steps_10___11(self):
        """
        DESCRIPTION: Repeat steps #10 - 11
        EXPECTED: Outcomes without prices are shown
        """
        pass
