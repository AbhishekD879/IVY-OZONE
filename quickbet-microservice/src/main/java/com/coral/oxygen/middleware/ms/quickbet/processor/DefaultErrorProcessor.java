package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;

public class DefaultErrorProcessor extends BanachResponseProcessor {
  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return true;
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(),
        RegularPlaceBetResponse.errorResponse(
            RegularPlaceBetResponse.Error.builder()
                .code(Messages.ERROR_CODE.code())
                .subErrorCode(Messages.DEFAULT_BANACH_ERROR.code())
                .description(
                    String.format("Banach response code: %s", response.getResponseCode().ordinal()))
                .build()));
  }
}
