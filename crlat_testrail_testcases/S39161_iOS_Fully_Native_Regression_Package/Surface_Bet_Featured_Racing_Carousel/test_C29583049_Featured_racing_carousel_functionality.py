import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C29583049_Featured_racing_carousel_functionality(Common):
    """
    TR_ID: C29583049
    NAME: Featured racing carousel functionality
    DESCRIPTION: This test case verifies Featured racing carousel functionality
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. Featured race module is available (created in CMS - for now N/A)
    PRECONDITIONS: 3. User is viewing the Featured tab
    """
    keep_browser_open = True

    def test_001_verify_eventcard_in_the_carousel(self):
        """
        DESCRIPTION: Verify event/card in the carousel
        EXPECTED: event/card in the carousel is displayed as per design
        EXPECTED: Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/3937606)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/3937607)
        EXPECTED: different card width for 4.0 inch display:
        EXPECTED: ![](index.php?/attachments/get/20352259)
        """
        pass

    def test_002_swipe_the_card_carousel_to_the_left(self):
        """
        DESCRIPTION: swipe the card carousel to the left
        EXPECTED: the carousel is swiped
        EXPECTED: 2nd card is displayed in the middle (part of 1st and 3rd card are displayed on the edge of the screen)
        """
        pass

    def test_003_swipe_the_card_carousel_back_to_the_right(self):
        """
        DESCRIPTION: swipe the card carousel back to the right
        EXPECTED: event/card in the carousel is displayed as 1step
        """
        pass
