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
class Test_C17032860_Vanilla_Global_footer(Common):
    """
    TR_ID: C17032860
    NAME: [Vanilla] Global footer
    DESCRIPTION: This test case verified Global Footer (GVC functionality)
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_check_global_footer(self):
        """
        DESCRIPTION: Check global footer.
        EXPECTED: Global footer is displayed at the bottom of each page.
        EXPECTED: Footer contains (configured by GVC marketing team, may differ):
        EXPECTED: - Responsible Gambling link
        EXPECTED: - links divided into sections
        EXPECTED: - Help & information
        EXPECTED: - Quick links
        EXPECTED: - Coral online and shop support
        EXPECTED: - Name, address and legal information of Coral
        EXPECTED: - Logos with links to partners (EGBA, essa, gambling commission etc)
        EXPECTED: All links are clickable and can be opened
        """
        pass
