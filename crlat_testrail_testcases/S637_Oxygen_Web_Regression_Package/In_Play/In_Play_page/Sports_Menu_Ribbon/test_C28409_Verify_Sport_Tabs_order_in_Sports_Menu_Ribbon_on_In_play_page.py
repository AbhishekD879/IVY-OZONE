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
class Test_C28409_Verify_Sport_Tabs_order_in_Sports_Menu_Ribbon_on_In_play_page(Common):
    """
    TR_ID: C28409
    NAME: Verify Sport Tabs order in Sports Menu Ribbon on 'In-play' page
    DESCRIPTION: This test case verifies order of Sport Tabs in Sports Menu Ribbon on 'In-play' page
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category, where X.XX - the latest OpenBet release
    PRECONDITIONS: Load Oxygen app
    """
    keep_browser_open = True

    def test_001_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: *   'In-Play' page is opened
        EXPECTED: *   First <Sport> tab is opened by default (e.g. Football)
        """
        pass

    def test_002_verify_sport_tabs_order(self):
        """
        DESCRIPTION: Verify sport tabs order
        EXPECTED: Tabs are displayed in the following order:
        EXPECTED: *   'Watch Live' tab first
        EXPECTED: *   'Live Now' sports categories are displayed first horizontally based on the Category 'displayOrder' in ascending order
        EXPECTED: *   'Upcoming' categories are displayed after this horizontally based on the Category 'displayOrder' in ascending order
        EXPECTED: *   If the displayOrder is the same in BOTH cases then they are displayed in A-Z order.
        """
        pass

    def test_003_verify_selected_sport_icon(self):
        """
        DESCRIPTION: Verify selected <Sport> icon
        EXPECTED: <Sport> icon is underscored
        """
        pass

    def test_004_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_verify_sport_tabs_order(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and verify Sport tabs order
        EXPECTED: Tabs are displayed in the following order:
        EXPECTED: * Sports categories are displayed based on the Category 'displayOrder' in ascending order
        EXPECTED: * If displayOrder is the same then they are displayed in A-Z order.
        """
        pass
