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
class Test_C60079231_Verify_displaying_of_specific_Cricket_Team_nameeg_England_3rd_T20(Common):
    """
    TR_ID: C60079231
    NAME: Verify displaying of specific Cricket Team name(e.g. |England 3rd T20|)
    DESCRIPTION: This test case verified displaying of specific Cricket Team name(e.g. England 3rd T20).
    DESCRIPTION: Created after PROD incident https://jira.egalacoral.com/browse/BMA-48652
    PRECONDITIONS: In TI create/find Cricket event with the following name templates:
    PRECONDITIONS: - **|TeamName1 X T20| |vs| |TeamName2 Y T20|**
    PRECONDITIONS: - **|TeamName1| |vs| |TeamName2 X T20|**
    PRECONDITIONS: where X,Y are sequence numbers(e.g. 2nd, 3rd, 4th)
    PRECONDITIONS: Event name examples:
    PRECONDITIONS: - **|India 3rd T20| |vs| |England 3rd T20|**
    PRECONDITIONS: - **|New Zealand| |vs| |England 3rd T20|**
    PRECONDITIONS: To retrieve information about event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_applicationverify_that_the_event_names_are_correctly_shown_on_pages_where_the_events_are_present(self):
        """
        DESCRIPTION: Load Oxygen application.
        DESCRIPTION: Verify that the Event names are correctly shown on pages where the Events are present.
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletin_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_cricket_pagesfor_desktopin_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_cricket_pages(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Cricket** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Cricket** pages
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_003_for_mobiletablethome_page__featured_tab_verify_that_event_names_on_in_play_modulehighlight_carouselfeatured_module_created_by_type_idevent_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'Featured' tab** :
        DESCRIPTION: Verify that Event names on :
        DESCRIPTION: In-play module
        DESCRIPTION: Highlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_004_for_mobiletablethome_page__in_play_tabhome_page__live_stream_tabfor_desktophome_page__in_play_and_live_stream_modulecheck_in_play_tab_and_live_stream_tabs(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'In Play'** tab
        DESCRIPTION: Home page > **'Live stream'** tab
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Home page > **'In play and live stream'** module
        DESCRIPTION: Check 'In-play' tab and 'Live Stream' tabs
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_005_on_cricket_landing_page__in_play_tab(self):
        """
        DESCRIPTION: On **Cricket Landing page > 'In Play'** tab
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_006_on_edp_of_the_appropriate_events(self):
        """
        DESCRIPTION: On **EDP** of the appropriate events
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_007_for_desktopon_sports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: On Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_008_for_mobileadd_any_selection_from_created_cricket_events_to_quick_bet_and_verify_displaying_of_event_names_in_quick_bet(self):
        """
        DESCRIPTION: **For Mobile:**
        DESCRIPTION: Add any selection from created Cricket Events to Quick Bet and verify displaying of Event names in **Quick Bet**.
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_009_add_any_selection_from_created_cricket_events_to_betslip_and_verify_displaying_of_event_names_in_betslip_only_ladbrokes(self):
        """
        DESCRIPTION: Add any selection from created Cricket Events to Betslip and verify displaying of Event names in **Betslip**. (Only Ladbrokes)
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass

    def test_010_place_bets_for_created_cricket_events_and_verify_displaying_of_event_names_in_my_bets(self):
        """
        DESCRIPTION: Place bets for created Cricket Events and verify displaying of Event names in **My Bets**.
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        pass
