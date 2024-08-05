package com.ladbrokescoral.cashout.payout.helper;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Deduction;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Leg;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.PotentialPayout;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.payout.PayoutContext;
import com.ladbrokescoral.cashout.payout.PayoutRequest;
import com.ladbrokescoral.cashout.payout.PayoutRequestFactory;
import com.ladbrokescoral.cashout.payout.PayoutUtil;
import com.ladbrokescoral.cashout.payout.PotentialReturns;
import com.ladbrokescoral.cashout.util.BetUtil;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicBoolean;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class PayoutServiceRequest {

  private PayoutRequestFactory payoutRequestFactory;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public PayoutServiceRequest(PayoutRequestFactory payoutRequestFactory) {
    this.payoutRequestFactory = payoutRequestFactory;
  }

  @Value("${payout.supported.bet-types}")
  private List<String> supportedBetTypes;

  public PayoutContext buildPayoutContext(List<BetSummaryModel> models, Selection selectionUpdate) {
    PayoutContext payoutContext = new PayoutContext();
    List<PayoutRequest> payoutRequests = new ArrayList<>();
    List<PotentialReturns> voidedBetsPotentialReturns = new ArrayList<>();
    models.forEach(
        (BetSummaryModel eachBetSummaryModel) -> {
          if (isBanachBet(selectionUpdate, eachBetSummaryModel)
              || isDeadHeatApplied(eachBetSummaryModel)
              || isSpSelection(eachBetSummaryModel)) {
            PotentialReturns voidedBetPotentialReturn = new PotentialReturns();
            voidedBetPotentialReturn.setBetId(eachBetSummaryModel.getId());
            voidedBetPotentialReturn.setReturns(0);
            voidedBetsPotentialReturns.add(voidedBetPotentialReturn);
          } else if (isBetElgibleForPayoutRequest(eachBetSummaryModel)) {
            payoutRequests.add(
                payoutRequestFactory.buildPayoutRequest(eachBetSummaryModel, selectionUpdate));
          }
        });
    payoutContext.setVoidedBetsPotentialReturns(voidedBetsPotentialReturns);
    payoutContext.setPayoutRequests(payoutRequests);
    return payoutContext;
  }

  private boolean isBanachBet(Selection selectionUpdate, BetSummaryModel eachBetSummaryModel) {
    return BetUtil.isBanachBet(eachBetSummaryModel)
        && isBetEligibleForVoid(selectionUpdate, eachBetSummaryModel);
  }

  private boolean isBetEligibleForVoid(
      Selection selectionUpdate, BetSummaryModel eachBetSummaryModel) {
    return isBetVoided(eachBetSummaryModel)
        || isBetElgibleForVoid(eachBetSummaryModel, selectionUpdate);
  }

  public List<PayoutRequest> buildPayoutRequests(List<BetSummaryModel> betSummaryModels) {
    List<PayoutRequest> payoutRequests = new ArrayList<>();
    betSummaryModels.forEach(
        (BetSummaryModel eachBetSummaryModel) -> {
          if (isBetElgibleForPayoutRequest(eachBetSummaryModel)) {
            payoutRequests.add(payoutRequestFactory.buildPayoutRequest(eachBetSummaryModel));
          }
        });
    return payoutRequests;
  }

  public boolean isBetElgibleForPayoutRequest(BetSummaryModel betSummaryModel) {
    boolean isBetElgibleForPayoutRequest = false;
    if (!BetUtil.isBanachBet(betSummaryModel)
        && isBetEligible(betSummaryModel)
        && (!isBetDeadHeatORSP(betSummaryModel))) {
      isBetElgibleForPayoutRequest = true;
    } else {
      ASYNC_LOGGER.warn(
          "Payout Service is not supported for the bettype::{}, betId::{}",
          betSummaryModel.getBetType().getName(),
          betSummaryModel.getId());
    }
    return isBetElgibleForPayoutRequest;
  }

  private boolean isBetEligible(BetSummaryModel betSummaryModel) {
    return (betSummaryModel.getBetType().getCode().equals("SGL") && isRule4Applied(betSummaryModel))
        || supportedBetTypes.contains(PayoutUtil.getBetType(betSummaryModel.getBetType()));
  }

  private boolean isBetDeadHeatORSP(BetSummaryModel betSummaryModel) {
    boolean isBetDeadHeatORSP = false;
    PotentialPayout potentialPayout = new PotentialPayout();
    List<PotentialPayout> potentialPayouts = new ArrayList<>();
    if (isDeadHeatApplied(betSummaryModel) || isSpSelection(betSummaryModel)) {
      potentialPayout.setValue("0.0");
      potentialPayouts.add(potentialPayout);
      betSummaryModel.setPotentialPayout(potentialPayouts);
      isBetDeadHeatORSP = true;
    }
    return isBetDeadHeatORSP;
  }

  private boolean isRule4Applied(BetSummaryModel model) {
    boolean isRule4Applied = false;
    if (!getPriceType(model).equals("D")) {
      Deduction result = model.getLeg().get(0).getPart().get(0).getDeduction().get(0);
      if (result.getType().equals("rule4") && !result.getValue().equals("0")) {
        isRule4Applied = true;
      }
    }
    return isRule4Applied;
  }

  private String getPriceType(BetSummaryModel model) {
    return model.getLeg().get(0).getPart().get(0).getPrice().get(0).getPriceType().getCode();
  }

  public boolean isDeadHeatApplied(BetSummaryModel model) {
    AtomicBoolean isDeadHeatApplied = new AtomicBoolean();
    isDeadHeatApplied.set(false);
    if (!getPriceType(model).equals("D")) {
      model.getLeg().stream()
          .forEach(
              (Leg leg) ->
                  leg.getPart().get(0).getDeduction().stream()
                      .forEach(
                          (Deduction deduction) -> {
                            ASYNC_LOGGER.debug(
                                "deadheatWin deduction type:{} applied for betId:{}",
                                deduction.getType(),
                                model.getId());
                            if ((deduction.getType().equalsIgnoreCase("deadheatWin")
                                    || (deduction.getType().equals("deadHeatEachWay")))
                                && !deduction.getValue().equals("0")) {
                              isDeadHeatApplied.set(true);
                            }
                          }));
    }
    return isDeadHeatApplied.get();
  }

  public boolean isSpSelection(BetSummaryModel model) {
    AtomicBoolean isDeadHeatApplied = new AtomicBoolean();
    isDeadHeatApplied.set(false);
    model.getLeg().stream()
        .forEach(
            (Leg leg) ->
                leg.getPart().get(0).getPrice().stream()
                    .forEach(
                        (Price price) -> {
                          if (price.getPriceType().getCode().equalsIgnoreCase("S")) {
                            isDeadHeatApplied.set(true);
                          }
                        }));
    return isDeadHeatApplied.get();
  }

  private boolean isBetVoided(BetSummaryModel model) {
    Optional<Leg> result =
        model.getLeg().stream()
            .filter(
                (Leg eachLeg) ->
                    "V"
                        .equalsIgnoreCase(
                            eachLeg.getPart().get(0).getOutcome().get(0).getResult().getValue()))
            .findFirst();
    return result.isPresent();
  }

  private boolean isBetElgibleForVoid(BetSummaryModel betSummaryModel, Selection selectionUpdate) {
    Optional<String> resCode = selectionUpdate.getResultCode();
    boolean isBetElgibleForVoid = false;
    if (resCode.isPresent() && "Void".equalsIgnoreCase(resCode.get())) {
      Optional<Leg> result =
          betSummaryModel.getLeg().stream()
              .filter(
                  (Leg eachLeg) ->
                      String.valueOf(selectionUpdate.getSelectionKey())
                          .equalsIgnoreCase(eachLeg.getPart().get(0).getOutcome().get(0).getId()))
              .findFirst();
      isBetElgibleForVoid = result.isPresent();
    }
    return isBetElgibleForVoid;
  }
}
