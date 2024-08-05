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
class Test_C9647832_TO_EDITVerify_Live_Now_and_Upcoming_sections_layout_on_In_Play_page(Common):
    """
    TR_ID: C9647832
    NAME: [TO EDIT]Verify 'Live Now' and 'Upcoming' sections layout on 'In-Play' page
    DESCRIPTION: This test case verifies 'Live Now' and 'Upcoming' sections layout on 'In-Play' page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    """
    keep_browser_open = True

    def test_001_verify_live_now_section_layout_on_in_play_page(self):
        """
        DESCRIPTION: Verify 'Live Now' section layout on 'In-Play' page
        EXPECTED: 'Live Now' section consists of the next items:
        EXPECTED: * 'LIVE NOW' (XX) - a title with the number of available live events
        EXPECTED: * 'Type' accordions
        EXPECTED: * Fixture Header
        EXPECTED: * Event Card
        EXPECTED: * 'UPCOMING' (XX) - a title with the number of available upcoming events
        """
        pass

    def test_002_verify_type_accordions_within_the_live_now_section(self):
        """
        DESCRIPTION: Verify 'Type' accordions within the 'Live Now' section
        EXPECTED: * 'Type' accordions contains 'Type' name, 'Cash Out' label and 'See All' link with chevron
        EXPECTED: * The number of expanded accordions is set in CMS
        """
        pass

    def test_003_verify_cash_out_label_displaying(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label displaying
        EXPECTED: 'CASH OUT' label is shown next to Type name if at least one of the event has cashoutAvail="Y)
        """
        pass

    def test_004_verify_type_accordions_order(self):
        """
        DESCRIPTION: Verify 'Type' accordions order
        EXPECTED: Type accordions are ordered by:
        EXPECTED: 1.  Class 'displayOrder' in ascending where minus ordinals are displayed first;
        EXPECTED: 2.  Type 'displayOrder' in ascending
        """
        pass

    def test_005_verify_fixture_header_displaying(self):
        """
        DESCRIPTION: Verify Fixture Header displaying
        EXPECTED: 'Home'/'Draw'/'Away' or 1'/'2' options are displayed and aligned by the right side
        """
        pass
