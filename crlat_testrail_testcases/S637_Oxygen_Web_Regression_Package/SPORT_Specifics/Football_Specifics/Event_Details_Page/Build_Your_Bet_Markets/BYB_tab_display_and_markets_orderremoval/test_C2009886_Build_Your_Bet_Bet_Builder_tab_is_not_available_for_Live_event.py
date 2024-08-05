import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C2009886_Build_Your_Bet_Bet_Builder_tab_is_not_available_for_Live_event(Common):
    """
    TR_ID: C2009886
    NAME: 'Build Your Bet'/'Bet Builder' tab is not available for Live event
    DESCRIPTION: Test case describes restriction of in play bet placement by 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab removal when event is Live
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: **FE removes 'BYB/Bet Builder' tab based on the event status sent from the feed provider (status: 2):**
    PRECONDITIONS: To check status for Banach event see query https://buildyourbet-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/v1/events/event_id
    PRECONDITIONS: ![](index.php?/attachments/get/48623426)
    PRECONDITIONS: Use Charles tool to edit response i.e. change status from 1 to 2 in https://buildyourbet-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/v1/events/event_id
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to prematch event details page where 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab tab is available
    """
    keep_browser_open = True

    def test_001_open_build_your_bet_coral__bet_builder_ladbrokes_tab_before_event_went_live_status_parameter_from_the_feed_provider_equals_1when_on_edp_page_until_event_goes_live_status_parameter_from_the_feed_provider_equals_2_and_perform_page_refresh(self):
        """
        DESCRIPTION: Open 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab before event went Live (status parameter from the feed provider equals 1).
        DESCRIPTION: When on EDP page until event goes live (status parameter from the feed provider equals 2) and perform page refresh
        EXPECTED: 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is removed from the UI when status code 2 is received in the response
        """
        pass

    def test_002_from_matches_tab_on_football_open_the_event_with_banach_which_is_live(self):
        """
        DESCRIPTION: From Matches tab on Football open the event with Banach which is live
        EXPECTED: When event is opened 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is not shown
        """
        pass
