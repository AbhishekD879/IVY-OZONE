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
class Test_C59499271_YourCall_markets_grouping_on_All_Markets_tab(Common):
    """
    TR_ID: C59499271
    NAME: YourCall markets grouping on All Markets tab
    DESCRIPTION: This TC verifies the appearance of YourCall markets on All Markets tab
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: YourCall markets are available for an event;
    """
    keep_browser_open = True

    def test_001_log_in_to_application_and_go_to_football_event_edp(self):
        """
        DESCRIPTION: Log in to application and go to Football event EDP;
        EXPECTED: User is on EDP, Main tab;
        """
        pass

    def test_002_go_to_all_markets_tab_and_review_the_market_grouping(self):
        """
        DESCRIPTION: Go to All Markets tab and review the market grouping;
        EXPECTED: - YourCall markets are present on this tab along with other markets;
        EXPECTED: - markets are not grouped under one header;
        EXPECTED: - market order is set according to backoffice setting "Display Order";
        EXPECTED: - YourCall market layout should be equal to standard market layout comparing to other tabs;
        EXPECTED: - top two/four markets are expanded by default (on Mobile/Desktop);
        """
        pass

    def test_003_try_to_expandcollapse_markets(self):
        """
        DESCRIPTION: Try to expand/collapse markets;
        EXPECTED: Each market should be independently expandable / collapsable;
        """
        pass
