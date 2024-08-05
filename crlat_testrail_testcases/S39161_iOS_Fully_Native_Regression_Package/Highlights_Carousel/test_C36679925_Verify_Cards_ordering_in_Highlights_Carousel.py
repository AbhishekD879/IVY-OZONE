import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C36679925_Verify_Cards_ordering_in_Highlights_Carousel(Common):
    """
    TR_ID: C36679925
    NAME: Verify Cards ordering in Highlights Carousel
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
