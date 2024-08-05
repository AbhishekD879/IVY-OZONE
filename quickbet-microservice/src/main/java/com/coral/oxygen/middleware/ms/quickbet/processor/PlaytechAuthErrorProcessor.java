package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;
import java.util.Arrays;
import java.util.List;

public class PlaytechAuthErrorProcessor extends BanachResponseProcessor {
  private static final List<String> PT_AUTH_ERRORS = Arrays.asList("9516", "9518");

  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return response.getResponseCode() == PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED
        && isPlaytechAuthError(response);
  }

  private boolean isPlaytechAuthError(PlaceBetResponseDto response) {
    return BanachUtils.isErrorPresent(response, PT_AUTH_ERRORS);
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(), RegularPlaceBetResponse.unauthorizedAccessError());
  }
}
