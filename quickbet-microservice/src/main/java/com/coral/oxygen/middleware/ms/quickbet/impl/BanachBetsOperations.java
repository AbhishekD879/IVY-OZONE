package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.BanachSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.BppComponent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachPlaceBetRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BanachSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.FractionalPriceDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.processor.BanachResponseProcessor;
import com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils;
import com.coral.oxygen.middleware.ms.quickbet.util.BetUtils;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachTimeoutException;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PriceResponse;
import io.vavr.control.Try;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;
import org.springframework.util.StringUtils;

@Component
@RequiredArgsConstructor
public class BanachBetsOperations {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private final BlockingBanachClient<GetPriceRequestDto, PriceResponse> priceClient;
  private final BlockingBanachClient<PlaceBetRequestDto, PlaceBetResponse> placeBetClient;
  private final BanachResponseProcessor responseProcessor;
  private final BppComponent bppComponent;

  public void restoreState(Session session) {
    if (session.getBanachSelectionData() != null) {
      BanachSelection banachSelection = new BanachSelection(session.getBanachSelectionData());
      addSelection(session, banachSelection);
    }
  }

  public void addSelection(Session session, BanachSelection selection) {
    clearSelection(session);
    Try.of(() -> executePriceRequest(session.sessionId(), selection))
        .onSuccess(resp -> processPriceResponse(session, selection, resp))
        .onFailure(t -> processPriceFailure(session, t));
  }

  private void processPriceFailure(Session session, Throwable t) {
    ASYNC_LOGGER.error("Failed to get price on Banach Selection", t);
    session.sendData(
        Messages.ADD_BANACH_SELECTION_ERROR.code(), BanachUtils.addSelectionExceptionMessage(t));
    clearSelection(session);
  }

  private void processPriceResponse(
      Session session, BanachSelection selection, PriceResponse priceResponse) {
    GetPriceResponseDto priceData = priceResponse.getData();

    if (priceData.getResponseCode() == GetPriceResponseDto.ResponseCodeEnum.OK) {
      session.setBanachSelectionData(selection.requestData());
      session.save();
      BanachSelectionResponse response =
          BanachSelectionResponse.builder()
              .data(new FractionalPriceDto(priceData.getPriceNum(), priceData.getPriceDen()))
              .roomName(selection.selectionHash())
              .build();
      session.sendData(Messages.ADD_BANACH_SELECTION_SUCCESS.code(), response);
    } else {
      clearSelection(session);
      session.sendData(
          Messages.ADD_BANACH_SELECTION_ERROR.code(),
          BanachUtils.addSelectionErrorMessage(priceData.getResponseCode()));
    }
  }

  private PriceResponse executePriceRequest(String sessionId, BanachSelection selection) {
    return priceClient.execute(
        sessionId,
        GetPriceRequestDto.builder()
            .obEventId(selection.requestData().getObEventId())
            .selectionIds(selection.requestData().getSelectionIds())
            .virtualSelectionDetails(selection.requestData().getPlayerSelections())
            .correlationId(sessionId)
            .build());
  }

  public void clearSelection(Session session) {
    session.setBanachSelectionData(null);
    session.save();
    session.unsubscribeFromAllRooms();
  }

  public void placeBet(Session session, BanachPlaceBetRequestData requestData) {
    bppComponent
        .fetchUserData(requestData.getToken())
        .onSuccess(userData -> tryPlaceBet(session, requestData, userData))
        .onFailure(t -> handleBppFailure(session, t));
  }

  public void handleBppFailure(Session session, Throwable throwable) {
    ASYNC_LOGGER.error("Failed to fetch OXI Token from BPP", throwable);
    session.sendData(
        Messages.BANACH_PLACE_BET_ERROR.code(), RegularPlaceBetResponse.unauthorizedAccessError());
  }

  private void tryPlaceBet(
      Session session, BanachPlaceBetRequestData requestData, UserDataResponse userData) {
    MDC.put("username", userData.getSportBookUserName());
    try {
      doPlace(session, requestData, userData);
    } catch (BanachTimeoutException be) {
      ASYNC_LOGGER.error("Timeout calling banach placeBet", be);
      session.sendData(
          Messages.BANACH_PLACE_BET_ERROR.code(),
          RegularPlaceBetResponse.errorResponse(
              RegularPlaceBetResponse.Error.builder()
                  .code(Messages.ERROR_CODE.code())
                  .subErrorCode(Messages.SERVICE_ERROR.code())
                  .description("Connection timeout")
                  .build()));
    } catch (Exception e) {
      ASYNC_LOGGER.error("Error during placing Banach Bet", e);
      session.sendData(
          Messages.BANACH_PLACE_BET_ERROR.code(),
          RegularPlaceBetResponse.errorResponse(
              Messages.ERROR_CODE.code(), "Exception on placing Banach Bet: " + e.getMessage()));
    }
  }

  private void doPlace(
      Session session, BanachPlaceBetRequestData requestData, UserDataResponse userData) {
    BanachSelectionRequestData activeSelection = session.getBanachSelectionData();
    Assert.notNull(activeSelection, "Selection should be added first");
    String[] price = StringUtils.trimAllWhitespace(requestData.getPrice()).split("/");
    int priceNum = Integer.parseInt(price[0]);
    int priceDen = Integer.parseInt(price[1]);

    PlaceBetRequestDto.PlaceBetRequestDtoBuilder requestBuilder = PlaceBetRequestDto.builder();
    requestBuilder
        .channel(requestData.getChannel())
        .currency(requestData.getCurrency())
        .obEventId(activeSelection.getObEventId())
        .selectionIds(activeSelection.getSelectionIds());

    Optional.ofNullable(activeSelection.getPlayerSelections())
        .filter(l -> !l.isEmpty())
        .ifPresent(requestBuilder::virtualSelectionDetails);

    requestBuilder
        .stake(getTotalStake(requestData))
        .obUserToken(userData.getOxiApiToken())
        .obUserId(userData.getSportBookUserName())
        .userPriceNum(priceNum)
        .userPriceDen(priceDen);

    if (requestData.isFreeBetIncluded()) {
      requestBuilder.freeBetId(requestData.getFreebet().getId());
    }

    PlaceBetRequestDto placeBetRequest = requestBuilder.build();
    String correlationId = "123"; // todo
    PlaceBetResponse response = placeBetClient.execute(correlationId, placeBetRequest);
    handleResponse(session, response);
  }

  private void handleResponse(Session session, PlaceBetResponse response) {
    ASYNC_LOGGER.info("Banach placeBet response: {}", response);
    responseProcessor.tryProcessResponse(session, response.getData());
  }

  private String getTotalStake(BanachPlaceBetRequestData requestData) {
    if (requestData.isFreeBetIncluded()) {
      return BetUtils.calculateTotalStakeWithFreeBet(
          requestData.getStake(), requestData.getFreebet());
    } else {
      return requestData.getStake();
    }
  }
}
