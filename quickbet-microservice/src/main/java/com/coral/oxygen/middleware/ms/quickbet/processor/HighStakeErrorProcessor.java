package com.coral.oxygen.middleware.ms.quickbet.processor;

import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.isErrorPresent;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;
import java.util.Collection;
import java.util.Collections;

public class HighStakeErrorProcessor extends BanachResponseProcessor {
  private static final Collection<String> HIGH_STAKE_ERROR_CODE = Collections.singletonList("538");

  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return response.getResponseCode() == PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED
        && isHighStakeError(response);
  }

  private boolean isHighStakeError(PlaceBetResponseDto response) {
    return isErrorPresent(response, HIGH_STAKE_ERROR_CODE);
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(),
        RegularPlaceBetResponse.errorResponse(
            RegularPlaceBetResponse.Error.builder()
                .code(Messages.ERROR_CODE.code())
                .description(response.getBetFailure().getBetError().get(0).getBetFailureDebug())
                .subErrorCode(Messages.STAKE_HIGH.code())
                .maxStake(response.getBetFailure().getBetMaxStake())
                .build()));
  }
}
