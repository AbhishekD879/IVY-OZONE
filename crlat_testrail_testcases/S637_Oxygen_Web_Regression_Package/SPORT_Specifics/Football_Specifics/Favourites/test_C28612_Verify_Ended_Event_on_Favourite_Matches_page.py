import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28612_Verify_Ended_Event_on_Favourite_Matches_page(Common):
    """
    TR_ID: C28612
    NAME: Verify Ended Event on Favourite Matches page
    DESCRIPTION: This Test Case verified Event view on Favourite Matches page for ended events.
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-9619 Remove link to more markets and suspended selections once game has finished on favorites page
    PRECONDITIONS: In order to check 'finish' attribute use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XXXXXXX - Event** **ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: Favourites should be turned off for Ladbrokes
    PRECONDITIONS: 1. User is on Football landing page
    """
    keep_browser_open = True

    def test_001_add_football_event_to_favorites_by_clicking_star_icon_on_event_card(self):
        """
        DESCRIPTION: Add Football Event to Favorites by clicking Star icon on event card
        EXPECTED: The star is highlighted in yellow
        """
        pass

    def test_002_tap_on_favourite_matches_page_icon_mobile_only(self):
        """
        DESCRIPTION: Tap on Favourite Matches page icon (mobile only)
        EXPECTED: Mobile:
        EXPECTED: - Favourites Matches page is opened
        EXPECTED: - Football Event is displayed on the Favourites page
        EXPECTED: Desktop: Event is added to Favourites widget
        """
        pass

    def test_003_wait_for_event_to_end_or_result_it_manually_in_ti(self):
        """
        DESCRIPTION: Wait for event to end or result it manually in TI
        EXPECTED: Finished event correponds to the attributes:
        EXPECTED: **isFinished="true"**
        EXPECTED: **isResulted=yes**
        """
        pass

    def test_004_verified_view_of_finished_event(self):
        """
        DESCRIPTION: Verified view of Finished Event
        EXPECTED: Mobile:
        EXPECTED: - Finished event is removed from Favourites and no longer displayed on Favourites page
        EXPECTED: Desktop:
        EXPECTED: - Finished event is removed from Favourites and no longer displayed in Favourites widget
        """
        pass
