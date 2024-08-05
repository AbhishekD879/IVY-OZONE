import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C60013389_Verify_that_BETBOOST_request_Removed_in_Kibana_after_build_bet_RemoteBetslip(Common):
    """
    TR_ID: C60013389
    NAME: Verify that BETBOOST request Removed in Kibana after build bet [RemoteBetslip]
    DESCRIPTION: This Test Сase verifies that RemoteBS DOES not make additional request to BPP /Proxy/accountFreebets?freebetTokenType=BETBOOST Kibana after each successful /Proxy/v1/buildBet request
    PRECONDITIONS: 1. Should be created a user with available odds boost.
    PRECONDITIONS: 2. How to add odds boost token https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+add+Odds+boost+token
    PRECONDITIONS: 3. Link to resources for monitoring request https://confluence.egalacoral.com/display/SPI/Symphony+Infrastructure+creds :
    PRECONDITIONS: - Link to Kibana for logs monitoring Coral (DEV) https://search-ladbrokescoral-logs-dev-qwxuyxesgs3eucjfy33g534srq.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:now-4h,mode:quick,to:now))&_a=(columns:!(log),index:%27remote-betslip-dev0-*%27,interval:auto,query:(language:lucene,query:%27%27),sort:!(%27@timestamp%27,desc))
    PRECONDITIONS: - Kibana Ladbrokes (dev) https://search-ladbrokes-logs-dev-xzdue7ziltomffcsupuiwze4f4.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:now-4h,mode:quick,to:now))&_a=(columns:!(log),index:dd957b60-b826-11e9-ba9f-b57ef4029e5c,interval:auto,query:(language:lucene,query:''),sort:!('@timestamp',desc))
    PRECONDITIONS: - Kibana Coral (tst) https://search-ladbrokescoral-logs-tst0-pmaws3wtbj22o7d3race4qthly.eu-west-2.es.amazonaws.com//_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:now-4h,mode:quick,to:now))&_a=(columns:!(log),index:'remote-betslip-tst0-*',interval:auto,query:(language:lucene,query:''),sort:!('@timestamp',desc))
    PRECONDITIONS: - Kibana Ladbrokes (tst) https://search-ladbrokes-logs-tst0-lrtq62dsd2tpbcs4kfa4fpxdh4.eu-west-2.es.amazonaws.com//_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:now-4h,mode:quick,to:now))&_a=(columns:!(log),index:a0ae89e0-a24f-11e9-b46a-cf7ecd9e68e7,interval:auto,query:(language:lucene,query:''),sort:!('@timestamp',desc))
    PRECONDITIONS: ![](index.php?/attachments/get/120999028)
    PRECONDITIONS: 4. How to find a request in Kibana:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+find+a+request+in+Kibana
    """
    keep_browser_open = True

    def test_001_open_app_and_login_with_user_from_preconditionsadd_selection_to_betslip(self):
        """
        DESCRIPTION: Open App and login with user from preconditions.
        DESCRIPTION: Add selection to betslip.
        EXPECTED: - Open Kibana tool for exact env.(from preconditions). There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        """
        pass

    def test_002_add_a_couple_of_additional_selections_to_betslip(self):
        """
        DESCRIPTION: Add a couple of additional selections to betslip.
        EXPECTED: - Open Kibana tool for exact env.(from preconditions). There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        """
        pass

    def test_003_remove_one_of_the_selections_from_the_betslip(self):
        """
        DESCRIPTION: Remove one of the selections from the betslip
        EXPECTED: - Open Kibana tool for exact env.(from preconditions). There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        """
        pass

    def test_004_remove_all_selections_from_the_betslip(self):
        """
        DESCRIPTION: Remove all selections from the betslip.
        EXPECTED: 
        """
        pass

    def test_005_for_mobileadd_selection_to_quick_bet(self):
        """
        DESCRIPTION: **For Mobile**
        DESCRIPTION: Add selection to 'Quick Bet'
        EXPECTED: - Open Kibana tool for exact env.(from preconditions). There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        """
        pass

    def test_006_for_mobilepress_x_and_remove_selection_to_quick_betopen_betslip(self):
        """
        DESCRIPTION: **For Mobile**
        DESCRIPTION: Press 'X' and remove selection to 'Quick Bet'.
        DESCRIPTION: Open Betslip.
        EXPECTED: - Selection from the 'Quick Bet' added to the betslip.
        EXPECTED: - Open Kibana tool for exact env.(from preconditions). There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        """
        pass
