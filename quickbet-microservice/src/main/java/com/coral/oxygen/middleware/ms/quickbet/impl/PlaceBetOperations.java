package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_ERROR_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_RESPONSE_CODE;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiPlaceBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiPlaceBetResponseAdapterFactory;
import com.coral.oxygen.middleware.ms.quickbet.converter.PlaceBetRequestConverter;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PlaceBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.service.BettingService;
import org.springframework.stereotype.Component;

@Component
public class PlaceBetOperations {

  private final PlaceBetRequestConverter placeBetRequestConverter;
  private final BettingService bettingService;
  private final NotConfirmedBetsHandler notConfirmedBetsHandler;
  private final MultiPlaceBetResponseAdapterFactory multiPlaceBetResponseAdapterFactory;

  public PlaceBetOperations(
      PlaceBetRequestConverter placeBetRequestConverter,
      BettingService bettingService,
      NotConfirmedBetsHandler notConfirmedBetsHandler,
      MultiPlaceBetResponseAdapterFactory multiPlaceBetResponseAdapterFactory) {
    this.placeBetRequestConverter = placeBetRequestConverter;
    this.bettingService = bettingService;
    this.notConfirmedBetsHandler = notConfirmedBetsHandler;
    this.multiPlaceBetResponseAdapterFactory = multiPlaceBetResponseAdapterFactory;
  }

  public void placeBet(Session session, UIPlaceBetRequest placeBetRequest) {
    String token = session.getToken();
    PlaceBetDto placeBetDto = placeBetRequestConverter.convert(session, placeBetRequest);
    GeneralResponse<RespBetPlace> response = bettingService.placeBetV2(token, placeBetDto);
    if (betWasPlacedSuccessfully(response)) {
      MultiPlaceBetResponseAdapter placeBetResponse =
          multiPlaceBetResponseAdapterFactory.from(response.getBody());
      if (placeBetResponse.allFinished()) {
        session.clearAllSelections();
        session.save();
        session.sendData(PLACE_BET_RESPONSE_CODE.code(), response.getBody());
      } else {
        notConfirmedBetsHandler.handle(session, placeBetResponse, token);
      }
    } else {
      session.sendData(PLACE_BET_ERROR_RESPONSE_CODE.code(), response.getErrorBody());
    }
  }

  private boolean betWasPlacedSuccessfully(GeneralResponse<RespBetPlace> response) {
    return response.getErrorBody() == null && response.getBody() != null;
  }
}
