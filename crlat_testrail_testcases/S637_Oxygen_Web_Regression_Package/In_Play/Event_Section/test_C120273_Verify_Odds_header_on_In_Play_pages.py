import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C120273_Verify_Odds_header_on_In_Play_pages(Common):
    """
    TR_ID: C120273
    NAME: Verify Odds header on In-Play pages
    DESCRIPTION: This test case verify Odds header displaying on In-Play pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: Note:
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    """
    keep_browser_open = True

    def test_001_find_sport_or_type_section_where_event_with_primary_market_is_shown_first(self):
        """
        DESCRIPTION: Find Sport or type section where event with Primary Market is shown first
        EXPECTED: Odds header is present in <Sport> section and is shown according to the following rules:
        EXPECTED: *    Odds header is shown with 'Home'/'Draw'/'Away' options if events in the section have 3-way Primary Market being shown
        EXPECTED: *    Odds header is shown with '1'/'2' options if events in the section have 2-way Primary Market being shown
        """
        pass

    def test_002_find_sport_or_type_section_where_event_without_primary_market_or_outright_event_is_shown_first_in_the_section_followed_by_events_with_primary_market(self):
        """
        DESCRIPTION: Find Sport or type section where event without primary market OR Outright event is shown first in the section, followed by events with Primary Market
        EXPECTED: Odds header is present in <Sport> section and is shown according to the following rules:
        EXPECTED: *    Odds header is shown with 'Home'/'Draw'/'Away' options if events in the section have 3-way Primary Market being shown
        EXPECTED: *    Odds header is shown with '1'/'2' options if events in the section have 2-way Primary Market being shown
        """
        pass

    def test_003_find_outright_section_where_there_are_no_events_shown_with_primary_market(self):
        """
        DESCRIPTION: Find Outright section where there are no events shown with Primary Market
        EXPECTED: Odds header is shown but options are NOT displayed
        """
        pass

    def test_004_repeat_steps_1_3_for_upcoming_events(self):
        """
        DESCRIPTION: Repeat steps 1-3 for upcoming events
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_1_3_on_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play_module_for_mobiletablet_homepage__in_play__live_stream_section__in_play_and_live_stream_switchers_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 on:
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section > 'In-Play' and 'Live Stream' switchers **For Desktop**
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_4_on_homepage__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab_in_play_page__watch_live_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 on:
        DESCRIPTION: * Homepage > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * 'In-play' page > 'Watch live' tab
        EXPECTED: 
        """
        pass
