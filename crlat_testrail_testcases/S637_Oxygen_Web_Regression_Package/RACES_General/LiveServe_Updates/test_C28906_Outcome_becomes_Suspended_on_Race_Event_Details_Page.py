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
class Test_C28906_Outcome_becomes_Suspended_on_Race_Event_Details_Page(Common):
    """
    TR_ID: C28906
    NAME: Outcome becomes Suspended on <Race> Event Details Page
    DESCRIPTION: Test case verifies outcome suspension in real time on Race EDP
    PRECONDITIONS: To get SiteServer info about event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes' **= 'SP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: Make sure event is actice (**eventStatusCode** = 'A')
    PRECONDITIONS: **Updates are received in push notifications**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_open_race_event_details_page_where_event_has_lp_price_type_pricetypecodes__lp_(self):
        """
        DESCRIPTION: Open <Race> event details page where event has LP price type (
        DESCRIPTION: **'priceTypeCodes'** = 'LP' )
        EXPECTED: * Event details page is opened
        EXPECTED: * Available markets tabs are displayed
        """
        pass

    def test_004_in_ti_suspend_one_of_the_selections_with_enabled_liveserve_updates_outcomestatuscode__s___navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend one of the selections with enabled liveServe updates (
        DESCRIPTION: **'outcomeStatusCode'** = 'S' ) > Navigate to application and observe changes
        EXPECTED: *   Price/Odds button of changed outcome is immediately displayed as greyed out and become disabled
        EXPECTED: *   The rest outcomes and market tabs remain not changed
        """
        pass

    def test_005_in_ti_unsuspend_selection_outcomestatuscode__s___navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend selection (
        DESCRIPTION: **'outcomeStatusCode'** = 'S' ) > Navigate to application and observe changes
        EXPECTED: *   Price/Odds button is no more disabled, it becomes active immediately
        EXPECTED: *   The rest outcomes and market tabs remain not changed
        """
        pass

    def test_006_in_ti_suspend_one_of_the_selections_within_market_in_a_collapsed_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend one of the selections within market in a collapsed state > Navigate to application and observe changes
        EXPECTED: *   Price/Odds button of changed outcome is displayed as greyed out  when expanding the market
        EXPECTED: *   The rest outcomes and market tabs remain not changed
        """
        pass

    def test_007_in_ti_unsuspend_selection_within_market_in_a_collapsed_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend selection within market in a collapsed state > Navigate to application and observe changes
        EXPECTED: *   Price/Odds button is no more disabled, it is displayed as active when expanding the market
        EXPECTED: *   The rest outcomes and market tabs remain not changed
        """
        pass

    def test_008_in_ti_suspend_one_of_the_selections_within_market_in_an_expanded_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend one of the selections within market in an expanded state > Navigate to application and observe changes
        EXPECTED: *   Price/Odds button of changed outcome is immediately displayed as greyed out and become disabled
        EXPECTED: *   The rest outcomes and market tabs remain not changed
        """
        pass

    def test_009_in_ti_unsuspend_selection_within_market_in_an_expanded_state__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend selection within market in an expanded state > Navigate to application and observe changes
        EXPECTED: *   Price/Odds button is no more disabled, it becomes active immediately
        EXPECTED: *   The rest outcomes and market tabs remain not changed
        """
        pass

    def test_010_repeat_steps__3_9_for_event_where_price_type_is_splpsp(self):
        """
        DESCRIPTION: Repeat steps # 3-9 for event where price type is 'SP'/'LP,SP'
        EXPECTED: 
        """
        pass
