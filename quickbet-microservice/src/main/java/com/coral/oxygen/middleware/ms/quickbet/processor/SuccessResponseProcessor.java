package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;

public class SuccessResponseProcessor extends BanachResponseProcessor {
  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return response.getResponseCode() == PlaceBetResponseDto.ResponseCodeEnum.ACCEPTED;
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_SUCCESS.code(), BanachUtils.toQuickBetResponse(response));
    clearSelection(session);
  }
}
