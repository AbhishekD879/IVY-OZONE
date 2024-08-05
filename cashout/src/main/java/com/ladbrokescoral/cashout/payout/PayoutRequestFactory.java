package com.ladbrokescoral.cashout.payout;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class PayoutRequestFactory {

  @Autowired private PayoutRequestConverter payoutRequestConverter;

  public PayoutRequest buildPayoutRequest(BetSummaryModel betSummaryModel) {
    return payoutRequestConverter.buildPayoutRequest(betSummaryModel);
  }

  public PayoutRequest buildPayoutRequest(
      BetSummaryModel betSummaryModel, Selection selectionUpdate) {
    PayoutRequest payoutRequest = payoutRequestConverter.buildPayoutRequest(betSummaryModel);
    payoutRequest
        .getLegs()
        .forEach(
            (PayoutLeg eachLeg) -> {
              if (eachLeg
                  .getId()
                  .equalsIgnoreCase(String.valueOf(selectionUpdate.getSelectionKey()))) {
                eachLeg.setResult(getResultCode(selectionUpdate.getResultCode()));
              }
            });
    return payoutRequest;
  }

  private String getResultCode(Optional<String> selectionResult) {
    String resultCode = selectionResult.isPresent() ? selectionResult.get() : "";
    String result = "";
    switch (resultCode) {
      case "Win":
        result = "W";
        break;
      case "Lose":
        result = "L";
        break;
      case "Void":
        result = "V";
        break;
      case "Place":
        result = "P";
        break;
      default:
        break;
    }
    return result;
  }
}
