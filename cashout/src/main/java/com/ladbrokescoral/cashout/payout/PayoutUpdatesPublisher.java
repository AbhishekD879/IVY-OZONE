package com.ladbrokescoral.cashout.payout;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Deduction;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Leg;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.PotentialPayout;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price;
import com.corundumstudio.socketio.SocketIOClient;
import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.payout.helper.PayoutServiceRequest;
import java.math.BigInteger;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@Service
public class PayoutUpdatesPublisher {

  private PayoutService payoutService;
  private KafkaTemplate<String, Object> kafkaTemplate;
  private PayoutServiceRequest payoutServiceRequest;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public PayoutUpdatesPublisher(
      PayoutService payoutService,
      KafkaTemplate<String, Object> kafkaTemplate,
      PayoutServiceRequest payoutServiceRequest) {
    this.payoutService = payoutService;
    this.kafkaTemplate = kafkaTemplate;
    this.payoutServiceRequest = payoutServiceRequest;
  }

  public void sendInitialUpdates(SocketIOClient client, String channelName, Object data) {
    InitialAccountHistoryBetResponse initialAccountHistoryBetResponse =
        (InitialAccountHistoryBetResponse) data;
    List<BetSummaryModel> betSummaryModels = initialAccountHistoryBetResponse.getBets();
    List<PayoutRequest> payoutRequests = payoutServiceRequest.buildPayoutRequests(betSummaryModels);
    List<PotentialReturns> potentialReturns = payoutService.getPotentialReturns(payoutRequests);
    ASYNC_LOGGER.debug(
        "PayoutUpdatesPublisher::sendInitialUpdates::potentialReturns::{}", potentialReturns);
    Map<String, Double> betWisePotentialValue =
        potentialReturns
            .parallelStream()
            .collect(
                Collectors.toConcurrentMap(
                    PotentialReturns::getBetId, PotentialReturns::getReturns));
    List<BetSummaryModel> bets =
        betSummaryModels
            .parallelStream()
            .map(
                (BetSummaryModel eachBetSummaryModel) -> {
                  List<PotentialPayout> potentialPayouts = eachBetSummaryModel.getPotentialPayout();
                  if (betWisePotentialValue.keySet().contains(eachBetSummaryModel.getId())) {
                    potentialPayouts.forEach(
                        (PotentialPayout eachPayout) -> {
                          double intialPotentialValue = Double.parseDouble(eachPayout.getValue());
                          if (betWisePotentialValue.get(eachBetSummaryModel.getId())
                              < intialPotentialValue) {
                            eachPayout.setValue(
                                String.valueOf(
                                    betWisePotentialValue.get(eachBetSummaryModel.getId())));
                          }
                        });
                    eachBetSummaryModel.setPotentialPayout(potentialPayouts);
                  }
                  return eachBetSummaryModel;
                })
            .collect(Collectors.toList());
    initialAccountHistoryBetResponse.setBets(bets);
    client.sendEvent(channelName, initialAccountHistoryBetResponse);
  }

  public void invokePayoutRequest(
      String token, Selection selectionUpdate, List<BetSummaryModel> betSummaryModels) {
    Map<String, Double> betWiseInitialPotentialValues =
        betSummaryModels
            .parallelStream()
            .collect(Collectors.toConcurrentMap(BetSummaryModel::getId, this::getPotentialValue));
    PayoutContext payoutContext =
        payoutServiceRequest.buildPayoutContext(betSummaryModels, selectionUpdate);
    List<PotentialReturns> potentialReturns =
        payoutService.getPotentialReturns(payoutContext.getPayoutRequests());
    List<PotentialReturns> filteredPotentialReturns =
        potentialReturns
            .parallelStream()
            .filter(
                (PotentialReturns eachReturns) ->
                    eachReturns.getReturns()
                        < betWiseInitialPotentialValues.get(eachReturns.getBetId()))
            .collect(Collectors.toList());
    filteredPotentialReturns.addAll(payoutContext.getVoidedBetsPotentialReturns());
    String topicName = InternalKafkaTopics.PAYOUT_UDPATES.getTopicName();
    kafkaTemplate.send(topicName, token, filteredPotentialReturns);
  }

  public Double getPotentialValue(BetSummaryModel betSummaryModel) {
    Double potentialValue = 0.0;
    List<PotentialPayout> potentialPayouts = betSummaryModel.getPotentialPayout();
    if (!CollectionUtils.isEmpty(potentialPayouts)) {
      PotentialPayout potentialPayout = potentialPayouts.get(0);
      potentialValue =
          StringUtils.hasLength(potentialPayout.getValue())
              ? Double.parseDouble(potentialPayout.getValue())
              : 0.0;
    }
    return potentialValue;
  }

  public void setPrices(
      BigInteger id, Integer num, Integer dec, List<BetSummaryModel> betSummaryModels) {
    betSummaryModels.stream()
        .forEach(
            bet ->
                bet.getLeg().stream()
                    .forEach(
                        (Leg leg) -> {
                          String selectionId = leg.getPart().get(0).getOutcome().get(0).getId();
                          if (selectionId.equalsIgnoreCase(String.valueOf(id))) {
                            Price price = leg.getPart().get(0).getPrice().get(0);
                            price.setPriceStartingNum(String.valueOf(num));
                            price.setPriceStartingDen(String.valueOf(dec));
                          }
                        }));
  }

  public void setDeductionPrices(
      BigInteger id, Integer num, Integer dec, List<BetSummaryModel> betSummaryModels) {
    betSummaryModels.stream()
        .forEach(
            bet ->
                bet.getLeg().stream()
                    .forEach(
                        (Leg leg) -> {
                          String selectionId = leg.getPart().get(0).getOutcome().get(0).getId();
                          if (selectionId.equalsIgnoreCase(String.valueOf(id))) {
                            List<Deduction> deductions = leg.getPart().get(0).getDeduction();
                            Deduction deduction = new Deduction();
                            deduction.setType("deadheatWin");
                            deduction.setValue(String.valueOf((double) num / dec));
                            deductions.add(deduction);
                          }
                        }));
  }

  public void setRule4DeductionFactor(
      BigInteger marketKey, double deduction, List<BetSummaryModel> betSummaryModels) {
    betSummaryModels.stream()
        .forEach(
            bet ->
                bet.getLeg().stream()
                    .forEach(
                        (Leg leg) -> {
                          String marketId =
                              leg.getPart().get(0).getOutcome().get(0).getMarket().getId();
                          if (marketId.equalsIgnoreCase(String.valueOf(marketKey))) {
                            leg.getPart().get(0).getDeduction().stream()
                                .forEach(
                                    (Deduction deductionobj) -> {
                                      if (deductionobj.getType().equalsIgnoreCase("rule4")) {
                                        deductionobj.setValue(String.valueOf(deduction));
                                      }
                                    });
                          }
                        }));
  }
}
