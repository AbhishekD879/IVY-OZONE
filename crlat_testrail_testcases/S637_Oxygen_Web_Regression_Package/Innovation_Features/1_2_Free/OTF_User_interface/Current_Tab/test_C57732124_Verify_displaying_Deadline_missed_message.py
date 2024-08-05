import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C57732124_Verify_displaying_Deadline_missed_message(Common):
    """
    TR_ID: C57732124
    NAME: Verify displaying 'Deadline missed' message
    DESCRIPTION: This test case verifies displaying 'Deadline missed' message
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User didn't submit a 1-2-Free prediction for the current game
    PRECONDITIONS: 3. One of events from current game started
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Deadline Missed' message displayed on 'Current Tab'
        EXPECTED: - Message retrieved from CMS
        EXPECTED: - Designed according: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c4af6671386a637a91d1790
        """
        pass
