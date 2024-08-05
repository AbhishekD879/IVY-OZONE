package com.ladbrokescoral.cashout.payout;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.google.gson.reflect.TypeToken;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.lang.reflect.Type;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class PayoutRequestFactoryTest {

  @InjectMocks PayoutRequestFactory payoutServiceImpl;
  @Mock PayoutRequestConverter payoutRequestConverter;

  @Test
  void testBuildPayoutRequestBetSummaryModel() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json");
    PayoutRequest payoutRequest = payoutServiceImpl.buildPayoutRequest(betSummaryModel);
    Assert.assertNull(payoutRequest);
  }

  @ParameterizedTest
  @ValueSource(strings = {"Win", "Lose", "Void", "Place", ""})
  void testBuildPayoutRequestBetSummaryModelSelection(String resultCode) {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json");
    PayoutRequest payoutRequestValue = new PayoutRequest();
    PayoutLeg payoutLeg = new PayoutLeg();
    payoutLeg.setId("12345");
    List<PayoutLeg> payoutLegs = new ArrayList<>();
    payoutLegs.add(payoutLeg);
    payoutRequestValue.setLegs(payoutLegs);
    Mockito.when(payoutRequestConverter.buildPayoutRequest(betSummaryModel))
        .thenReturn(payoutRequestValue);
    Selection selectionUpdate = new Selection();
    selectionUpdate.setSelectionKey(BigInteger.valueOf(12345));
    selectionUpdate.setResultCode(resultCode);
    PayoutRequest payoutRequest =
        payoutServiceImpl.buildPayoutRequest(betSummaryModel, selectionUpdate);
    Assert.assertNotNull(payoutRequest);
  }

  @Test
  void testBuildPayoutRequestBetSummaryModelSelectionWithEmptyResultCode() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json");
    PayoutRequest payoutRequestValue = new PayoutRequest();
    PayoutLeg payoutLeg = new PayoutLeg();
    payoutLeg.setId("12345");
    List<PayoutLeg> payoutLegs = new ArrayList<>();
    payoutLegs.add(payoutLeg);
    payoutRequestValue.setLegs(payoutLegs);
    Mockito.when(payoutRequestConverter.buildPayoutRequest(betSummaryModel))
        .thenReturn(payoutRequestValue);
    Selection selectionUpdate = new Selection();
    selectionUpdate.setSelectionKey(BigInteger.valueOf(12345));
    PayoutRequest payoutRequest =
        payoutServiceImpl.buildPayoutRequest(betSummaryModel, selectionUpdate);
    Assert.assertNotNull(payoutRequest);
  }

  @Test
  void testBuildPayoutRequestBetSummaryModelSelection() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json");
    PayoutRequest payoutRequestValue = new PayoutRequest();
    PayoutLeg payoutLeg = new PayoutLeg();
    payoutLeg.setId("123456");
    List<PayoutLeg> payoutLegs = new ArrayList<>();
    payoutLegs.add(payoutLeg);
    payoutRequestValue.setLegs(payoutLegs);
    Mockito.when(payoutRequestConverter.buildPayoutRequest(betSummaryModel))
        .thenReturn(payoutRequestValue);
    Selection selectionUpdate = new Selection();
    PayoutRequest payoutRequest =
        payoutServiceImpl.buildPayoutRequest(betSummaryModel, selectionUpdate);
    Assert.assertNotNull(payoutRequest);
  }

  private BetSummaryModel getBets(String fileName) {
    Type type =
        new TypeToken<List<BetSummaryModel>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<BetSummaryModel> bets = GsonUtil.fromJson(fileName, type);
    return bets.get(0);
  }
}
