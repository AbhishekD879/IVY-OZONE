package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.OxiReturnStatus;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;
import java.util.Objects;
import java.util.Optional;

/**
 * Presence of betError in response is treated like success, but session isn't cleared, so user
 * could try to place once again
 */
public class ObBetErrorResponseProcessor extends BanachResponseProcessor {
  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return betErrorPresentWithOxiStatusSuccess(response);
  }

  private boolean betErrorPresentWithOxiStatusSuccess(PlaceBetResponseDto response) {
    return Objects.nonNull(response.getBetFailure())
        && Optional.ofNullable(response.getOxiReturnStatus())
            .map(OxiReturnStatus::getCode)
            .filter(code -> code.equals("1"))
            .isPresent();
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_SUCCESS.code(), BanachUtils.toQuickBetResponse(response));
  }
}
