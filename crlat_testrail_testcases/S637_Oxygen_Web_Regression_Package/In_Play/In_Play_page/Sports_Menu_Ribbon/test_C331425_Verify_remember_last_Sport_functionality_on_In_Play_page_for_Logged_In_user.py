import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C331425_Verify_remember_last_Sport_functionality_on_In_Play_page_for_Logged_In_user(Common):
    """
    TR_ID: C331425
    NAME: Verify remember last Sport functionality on In-Play page for Logged In user
    DESCRIPTION: This test case verifies remember last Sport functionality on In-Play page for Logged In user
    PRECONDITIONS: TI (events) config:
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category, where X.XX - the latest OpenBet release
    PRECONDITIONS: Load Oxygen application
    PRECONDITIONS: Log in
    """
    keep_browser_open = True

    def test_001_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to In-Play page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default
        """
        pass

    def test_002_choose_any_sports_icon(self):
        """
        DESCRIPTION: Choose any Sports icon
        EXPECTED: * Selected Sports tab is underlined by red line **Coral** /without underline **Ladbrokes**
        EXPECTED: * The appropriate content is displayed for selected Sports
        """
        pass

    def test_003_navigate_across_application(self):
        """
        DESCRIPTION: Navigate across application
        EXPECTED: 
        """
        pass

    def test_004_back_to_in_play_page(self):
        """
        DESCRIPTION: Back to In-Play page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * Tab from step 2 is selected and underlined by red line **Coral**/ without underline **Ladbrokes**
        """
        pass

    def test_005_repeat_steps_1_4_when_there_are_no_in_play_events_for_saved_sport(self):
        """
        DESCRIPTION: Repeat steps 1-4 when there are no In-Play events for saved sport
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * <Sport> tab which was chosen before (without Live events) is opened  and underlined by red line **Coral**/ without underline **Ladbrokes**
        """
        pass
