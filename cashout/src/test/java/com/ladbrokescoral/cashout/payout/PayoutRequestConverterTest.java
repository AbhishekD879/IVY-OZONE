package com.ladbrokescoral.cashout.payout;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.ConfirmingResult;
import com.google.gson.reflect.TypeToken;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.lang.reflect.Type;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {PayoutRequestConverter.class})
class PayoutRequestConverterTest {

  @Autowired private PayoutRequestConverter payoutRequestConverter;

  // PR Request for DBL bet type object.
  @Test
  void testBuildPayoutRequest() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel2.json");
    betSummaryModel.getBetType().setCode("DBL");
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet type object.
  @Test
  void testBuildPayoutRequestACCABetType() {
    PayoutRequest payoutRequest =
        payoutRequestConverter.buildPayoutRequest(getBets("BetSummaryModel3.json"));
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet type object.
  @Test
  void testBuildPayoutRequestACCABetTypeWithEmptyDeduction() {
    PayoutRequest payoutRequest =
        payoutRequestConverter.buildPayoutRequest(getBets("BetSummaryModel7.json"));
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet with Empty Deduction object.
  @Test
  void testBuildPayoutRequestACCABetTypeWithEmptyDeductions() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel3.json");
    betSummaryModel.getLeg().get(0).getPart().get(0).setDeduction(Collections.emptyList());
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet with Each way Deduction object..
  @Test
  void testBuildPayoutRequestACCABetTypeWithEmptyEachWayDeductions() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel4.json");
    betSummaryModel.getLeg().get(0).getPart().get(0).getEachWayTerms().get(0).setEachWayNum("");
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet with null result.
  @Test
  void testBuildPayoutRequestACCABetTypeWithEmptyResult() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel4.json");
    betSummaryModel.getLeg().get(0).getPart().get(0).getOutcome().get(0).setResult(null);
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet with empty result.
  @ParameterizedTest
  @ValueSource(strings = {"", "-"})
  void testBuildPayoutRequestACCABetTypeWithEmptyResultValue(String resultValue) {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel6.json");
    ConfirmingResult confirmResult = new ConfirmingResult();
    confirmResult.setValue(resultValue);
    betSummaryModel.getLeg().get(0).getPart().get(0).getOutcome().get(0).setResult(confirmResult);
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
    Assert.assertNotNull(payoutRequest);
  }

  // PR Request for ACCA bet with empty starting price.
  @Test
  void testBuildPayoutRequestACCABetTypeWithEmptyStartingPrice() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel5.json");
    betSummaryModel.getLeg().get(0).getPart().get(0).getPrice().get(0).setPriceStartingNum("");
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
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
