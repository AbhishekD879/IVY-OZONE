package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;

public class PriceChangeResponseProcessor extends BanachResponseProcessor {

  @Override
  protected boolean canBeProcessed(PlaceBetResponseDto response) {
    return response.getResponseCode() == PlaceBetResponseDto.ResponseCodeEnum.PRICE_NOT_AVAILABLE;
  }

  @Override
  protected void doProcessResponse(Session session, PlaceBetResponseDto response) {
    GetPriceResponseDto validPrice = response.getValidPrice();
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(),
        RegularPlaceBetResponse.priceChangeError(
            validPrice.getPriceNum(), validPrice.getPriceDen(), response.getResponseMessage()));
  }
}
