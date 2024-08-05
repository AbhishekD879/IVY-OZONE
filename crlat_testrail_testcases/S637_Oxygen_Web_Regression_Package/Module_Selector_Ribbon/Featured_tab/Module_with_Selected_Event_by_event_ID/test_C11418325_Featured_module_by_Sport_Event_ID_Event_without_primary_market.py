import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C11418325_Featured_module_by_Sport_Event_ID_Event_without_primary_market(Common):
    """
    TR_ID: C11418325
    NAME: Featured module by <Sport> Event ID: Event without primary market
    DESCRIPTION: This test verifies the case when Feature event module is created using Event that doesn't have a primary market available but has other active markets available(not primary markets)
    PRECONDITIONS: 1. Featured module by Event id without primary market should be created in CMS-> Featured Tab Module
    PRECONDITIONS: 2. User should be on homepage Featured tab.
    PRECONDITIONS: List of primary markets:
    PRECONDITIONS: - Win or Each Way
    PRECONDITIONS: - Match Betting,
    PRECONDITIONS: - Match Results,
    PRECONDITIONS: - Extra Time Result,
    PRECONDITIONS: - Extra-Time Result,
    PRECONDITIONS: - Penalty Shoot-Out Winner,
    PRECONDITIONS: - To Qualify
    """
    keep_browser_open = True

    def test_001_find_featured_module_by_event_id_from_preconditions_and_verify_displaying_of_the_module(self):
        """
        DESCRIPTION: Find Featured module by Event Id from preconditions and verify displaying of the module
        EXPECTED: * Featured module by Event Id is displayed with the accordion
        EXPECTED: * Event inside the module is displayed without Market/Selections
        """
        pass

    def test_002_tap_on_the_event_inside_the_module_and_verify_redirection_to_the_event_details_page(self):
        """
        DESCRIPTION: Tap on the Event inside the module and verify redirection to the Event Details page
        EXPECTED: * User is redirected to Event Details Page
        EXPECTED: * Other active markets of the Event are shown on Event Details Page
        """
        pass
