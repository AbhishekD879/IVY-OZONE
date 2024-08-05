package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;
import java.util.Collections;
import java.util.List;

public class EventAlreadyStartedProcessor extends BanachResponseProcessor {
  private static final List<String> EVENT_STARTED_ERROR_CODE = Collections.singletonList("537");

  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return response.getResponseCode() == PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED
        && BanachUtils.isErrorPresent(response, EVENT_STARTED_ERROR_CODE);
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(),
        RegularPlaceBetResponse.errorResponse(
            RegularPlaceBetResponse.Error.builder()
                .code(Messages.ERROR_CODE.code())
                .subErrorCode(Messages.EVENT_STARTED.code())
                .description(response.getBetFailure().getBetError().get(0).getBetFailureReason())
                .build()));
  }
}
