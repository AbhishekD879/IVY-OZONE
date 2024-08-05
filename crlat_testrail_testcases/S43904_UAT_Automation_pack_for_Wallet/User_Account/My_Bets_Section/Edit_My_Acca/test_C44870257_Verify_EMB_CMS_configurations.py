import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870257_Verify_EMB_CMS_configurations(Common):
    """
    TR_ID: C44870257
    NAME: Verify EMB CMS configurations
    DESCRIPTION: 
    PRECONDITIONS: User logged in
    PRECONDITIONS: User have accumulator bets
    """
    keep_browser_open = True

    def test_001_enabled_emb_checkbox_in_cms(self):
        """
        DESCRIPTION: Enabled EMB checkbox in cms
        EXPECTED: EMB is displayed in front end
        EXPECTED: Note: when place a accumulator bet EMB should be displayed on MY Bets area.
        """
        pass

    def test_002_disabled_emb_checkbox_in_cms(self):
        """
        DESCRIPTION: Disabled EMB checkbox in cms
        EXPECTED: EMB should not displayed in front end.
        EXPECTED: Note: when place a accumulator bet EMB should not displayed on MY Bets area.
        """
        pass
