package com.ladbrokescoral.cashout.payout;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.PotentialPayout;
import com.corundumstudio.socketio.SocketIOClient;
import com.google.common.reflect.TypeToken;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.payout.helper.PayoutServiceRequest;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.lang.reflect.Type;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.kafka.core.KafkaTemplate;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class PayoutUpdatesPublisherTest {

  @InjectMocks private PayoutUpdatesPublisher payoutUpdatesPublisher;
  @Mock private PayoutService payoutService;
  @Mock private KafkaTemplate<String, Object> kafkaTemplate;
  @Mock private PayoutServiceRequest payoutServiceRequest;
  SocketIOClient client = Mockito.mock(SocketIOClient.class);

  @Test
  void testPayoutRequest() {
    Selection selection = new Selection();
    selection.setSelectionKey(BigInteger.valueOf(193796721));
    selection.setResultCode("Void");

    PayoutContext payoutContext = new PayoutContext();
    payoutContext.setPayoutRequests(getReturns("PayoutRequest.json"));
    payoutContext.setVoidedBetsPotentialReturns(Collections.emptyList());

    when(payoutServiceRequest.buildPayoutContext(Mockito.any(), Mockito.any()))
        .thenReturn(payoutContext);
    List<PotentialReturns> potentialReturns = new ArrayList<>();
    PotentialReturns potentialReturn = new PotentialReturns();
    potentialReturn.setBetId("2147633437");
    potentialReturn.setReturns(0.001);
    PotentialReturns potentialReturn1 = new PotentialReturns();
    potentialReturn1.setBetId("21476334378");
    potentialReturn1.setReturns(0.02);
    potentialReturns.add(potentialReturn1);
    potentialReturns.add(potentialReturn);
    when(payoutService.getPotentialReturns(Mockito.any())).thenReturn(potentialReturns);

    payoutUpdatesPublisher.invokePayoutRequest("123", selection, getBets("BetSummaryModel.json"));
    Mockito.verify(kafkaTemplate).send(Mockito.any(), Mockito.any(), Mockito.any());
  }

  @ParameterizedTest
  @CsvSource({"2147633437,true", "2147633438,false"})
  void testSendingInitialUpdates(String betId, boolean val) {
    InitialAccountHistoryBetResponse initialAccountHistoryBetResponse =
        new InitialAccountHistoryBetResponse(
            getBets("BetSummaryModel.json"), null, null, new Paging(), "1234", "1");
    PotentialReturns potentialReturns = new PotentialReturns();
    potentialReturns.setBetId(betId);
    potentialReturns.setReturns(3.1);

    when(payoutServiceRequest.buildPayoutRequests(Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json"));
    when(payoutService.getPotentialReturns(Mockito.any()))
        .thenReturn(Collections.singletonList(potentialReturns));
    when(payoutServiceRequest.isDeadHeatApplied(Mockito.any())).thenReturn(val);

    payoutUpdatesPublisher.sendInitialUpdates(client, "initial", initialAccountHistoryBetResponse);
    Mockito.verify(client, times(1)).sendEvent(Mockito.any(), Mockito.any());
  }

  @Test
  void testSendingInitialUpdates() {
    InitialAccountHistoryBetResponse initialAccountHistoryBetResponse =
        new InitialAccountHistoryBetResponse(
            getBets("BetSummaryModel.json"), null, null, new Paging(), "1234", "1");

    PotentialReturns potential = new PotentialReturns();
    potential.setBetId("214763343723");
    potential.setReturns(3.1);
    List<PotentialReturns> potentialReturns = new ArrayList<>();
    PotentialReturns potentialReturn = new PotentialReturns();
    potentialReturn.setBetId("2147633437");
    potentialReturn.setReturns(0.001);
    PotentialReturns potentialReturn1 = new PotentialReturns();
    potentialReturn1.setBetId("21476334378");
    potentialReturn1.setReturns(0.02);
    potentialReturns.add(potentialReturn1);
    potentialReturns.add(potentialReturn);
    potentialReturns.add(potential);

    when(payoutServiceRequest.buildPayoutRequests(Mockito.any()))
        .thenReturn(getReturns("PayoutRequest.json"));
    when(payoutService.getPotentialReturns(Mockito.any())).thenReturn(potentialReturns);
    when(payoutServiceRequest.isDeadHeatApplied(Mockito.any())).thenReturn(false);

    payoutUpdatesPublisher.sendInitialUpdates(client, "initial", initialAccountHistoryBetResponse);
    Mockito.verify(client, times(1)).sendEvent(Mockito.any(), Mockito.any());
  }

  @Test
  void testSetPrices() {
    Selection selection = new Selection();
    selection.getDeadHeat();
    payoutUpdatesPublisher.setPrices(
        BigInteger.valueOf(193796721), 2, 1, getBets("BetSummaryModel7.json"));
    payoutUpdatesPublisher.setDeductionPrices(
        BigInteger.valueOf(193796721), 3, 2, getBets("BetSummaryModel7.json"));
    payoutUpdatesPublisher.setRule4DeductionFactor(
        BigInteger.valueOf(46742978), 2.3, getBets("BetSummaryModel7.json"));
    payoutUpdatesPublisher.setRule4DeductionFactor(
        BigInteger.valueOf(46742972), 2.3, getBets("BetSummaryModel7.json"));
    Mockito.verify(kafkaTemplate, times(0)).send(Mockito.any(), Mockito.any(), Mockito.any());
  }

  @Test
  void testGetPotentialValue_null() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json").get(0);
    betSummaryModel.setPotentialPayout(null);
    Double potentialValue = payoutUpdatesPublisher.getPotentialValue(betSummaryModel);
    Assertions.assertEquals(0.0, potentialValue);
  }

  @Test
  void testGetPotentialValue_empty() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json").get(0);
    List<PotentialPayout> potentialPayouts = new ArrayList<>();
    PotentialPayout potentialPayout = new PotentialPayout();
    potentialPayout.setValue("");
    potentialPayouts.add(potentialPayout);
    betSummaryModel.setPotentialPayout(potentialPayouts);
    Double potentialValue = payoutUpdatesPublisher.getPotentialValue(betSummaryModel);
    Assertions.assertEquals(0.0, potentialValue);
  }

  @Test
  void testGetPotentialValue() {
    BetSummaryModel betSummaryModel = getBets("BetSummaryModel.json").get(0);
    List<PotentialPayout> potentialPayouts = new ArrayList<>();
    PotentialPayout potentialPayout = new PotentialPayout();
    potentialPayout.setValue("0.02");
    potentialPayouts.add(potentialPayout);
    betSummaryModel.setPotentialPayout(potentialPayouts);
    Double potentialValue = payoutUpdatesPublisher.getPotentialValue(betSummaryModel);
    Assertions.assertEquals(0.02, potentialValue);
  }

  private List<BetSummaryModel> getBets(String fileName) {
    Type type =
        new TypeToken<List<BetSummaryModel>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<BetSummaryModel> bets = GsonUtil.fromJson(fileName, type);
    return bets;
  }

  private List<PayoutRequest> getReturns(String fileName) {
    Type type =
        new TypeToken<List<PayoutRequest>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<PayoutRequest> returns = GsonUtil.fromJson(fileName, type);
    return returns;
  }
}
