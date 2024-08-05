import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C25039114_Verify_Interacting_with_Horse_Racing_Event_Cards(Common):
    """
    TR_ID: C25039114
    NAME: Verify Interacting with Horse Racing Event Cards
    DESCRIPTION: This Test Case Verifies Interacting with Horse Racing Event Cards.
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default on Home page
    PRECONDITIONS: * A Horse Racing module is present on Featured Tab
    PRECONDITIONS: * The Horse Racing module includes one ore more Horse Racing Events
    """
    keep_browser_open = True

    def test_001_navigate_to_the_horse_racing_module_on_featured_tab(self):
        """
        DESCRIPTION: Navigate to the Horse Racing module on Featured tab
        EXPECTED: User is viewing the Horse Racing Event card(s)
        """
        pass

    def test_002_the_horse_racing_module_includes_the_one_horse_racing_event(self):
        """
        DESCRIPTION: The Horse Racing module includes the one Horse Racing Event:
        EXPECTED: * User see Horse Racing Card which size fits within the allocated space
        EXPECTED: * User can't swipe displayed Horse Racing Card to the right or the left
        """
        pass

    def test_003_the_horse_racing_module_includes_more_than_one_horse_racing_event(self):
        """
        DESCRIPTION: The Horse Racing module includes more than one Horse Racing Event:
        EXPECTED: * User see Horse Racing Card in the carousel
        EXPECTED: * The first Horse Racing Card is displayed wholly, the next one is displayed partially
        EXPECTED: * User be able to swipe Horse Racing Cards to the right and left to locate an event
        EXPECTED: * No infinite swipe: event cards are swiped from the first to the last and back - from the last to the first.
        """
        pass
