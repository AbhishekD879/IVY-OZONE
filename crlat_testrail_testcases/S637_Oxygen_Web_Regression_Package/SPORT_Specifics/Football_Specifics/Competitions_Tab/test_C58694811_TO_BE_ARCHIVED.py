import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C58694811_TO_BE_ARCHIVED(Common):
    """
    TR_ID: C58694811
    NAME: TO BE ARCHIVED!
    DESCRIPTION: Test case is no longer actual due to changes in scope of https://jira.egalacoral.com/browse/BMA-54287
    PRECONDITIONS: 
    """
    keep_browser_open = True
