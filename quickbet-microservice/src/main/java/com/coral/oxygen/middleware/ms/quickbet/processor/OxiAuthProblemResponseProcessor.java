package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.util.OxiCodes;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.OxiReturnStatus;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;

public class OxiAuthProblemResponseProcessor extends BanachResponseProcessor {
  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    OxiReturnStatus oxiReturnStatus = response.getOxiReturnStatus();
    return oxiReturnStatus != null && OxiCodes.isAuthErrorCode(oxiReturnStatus.getCode());
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(), RegularPlaceBetResponse.unauthorizedAccessError());
  }
}
