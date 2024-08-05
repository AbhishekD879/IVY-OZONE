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
class Test_C9770230_Featured_ordering_of_modules_and_submodules(Common):
    """
    TR_ID: C9770230
    NAME: Featured: ordering of modules and submodules
    DESCRIPTION: This test case verifies ordering of modules and submodules in Featured tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems (Coral OB) or https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+OpenBet+System (Ladbrokes OB)
    PRECONDITIONS: - You should have active Featured modules and submodules (e.g Quick Links module with couple active quick links, Highlights Carousel module with couple active Highlights Carousels etc.) in CMS > Sport Pages > Homepage
    PRECONDITIONS: - You should be on a Home page > Featured tab in application
    """
    keep_browser_open = True

    def test_001_verify_order_of_modules_and_submodules(self):
        """
        DESCRIPTION: Verify order of modules and submodules
        EXPECTED: - Modules are ordered according to order in CMS
        EXPECTED: - Submodules are grouped within their modules and ordered according to order in CMS
        """
        pass

    def test_002___in_cms__sport_pages__homepage_reorder_modules_and_submodules__in_application_verify_order_of_modules_and_submodules(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage reorder modules and submodules
        DESCRIPTION: - In application verify order of modules and submodules
        EXPECTED: - Modules are ordered according to order in CMS
        EXPECTED: - Submodules are grouped within their modules and ordered according to order in CMS
        """
        pass
