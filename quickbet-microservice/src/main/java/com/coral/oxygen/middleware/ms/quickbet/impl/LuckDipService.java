package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.util.ResponseUtils;
import com.coral.oxygen.middleware.ms.quickbet.util.ValidatorUtils;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetsDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.service.BettingService;
import java.text.MessageFormat;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class LuckDipService {

  private static final String LP_PRICE_TYPE = "LP";
  private static final String LUCKY_DIP = "LDIP";
  private static final String ANDROID_CHANNEL = "S|W|A0000000";
  private static final String IOS_CHANNEL = "S|W|I0000000";

  private final BettingService bettingService;
  private final BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter;
  private final SelectionOperations selectionOperations;

  public LuckDipService(
      BettingService bettingService,
      BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter,
      SelectionOperations selectionOperations) {
    this.bettingService = bettingService;
    this.betToReceiptResponseDtoConverter = betToReceiptResponseDtoConverter;
    this.selectionOperations = selectionOperations;
  }

  public void processLuckyDipPlaceBet(
      Session session, Outcome allottedPlayer, LuckyDipBetPlacementRequest request) {

    ValidatorUtils.validateRequest(request);
    com.egalacoral.spark.siteserver.model.Price price = findFirst(allottedPlayer.getPrices());
    BetsDto betsDto;

    if (Objects.nonNull(price)) {
      Integer priceNum = price.getPriceNum();
      Integer priceDen = price.getPriceDen();
      if (Objects.nonNull(priceNum) && Objects.nonNull(priceDen)) {
        betsDto = prepareLuckyDipBPPRequest(allottedPlayer, request, price).build();
        log.info("LuckyDip Place Bet Request: {}", betsDto);
        GeneralResponse<BetsResponse> generalResponse =
            bettingService.placeBet(request.getToken(), betsDto);
        log.info("LuckyDip Place Bet Response: {}", generalResponse.getBody());
        ResponseUtils.handleErrors(generalResponse)
            .fold(
                (RegularPlaceBetResponse error) -> {
                  session.sendData(PLACE_BET_ERROR_RESPONSE_CODE.code(), error);
                  return null;
                },
                (BetsResponse body) -> {
                  processSuccessResponse(session, body);
                  return null;
                });
      }
    } else {
      throw new SiteServException(
          PRICES_NOT_FOUND,
          PRICES_NOT_FOUND.code(),
          MessageFormat.format(" Price not found in LuckDip market {0}", request.getMarketId()));
    }
  }

  public <T> T findFirst(List<T> list) {
    return list.stream().filter(Objects::nonNull).findFirst().orElse(null);
  }

  public RegularPlaceBetResponse createSuccessResponse(BetsResponse body) {
    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    Collection<ReceiptResponseDto> dtoList =
        betToReceiptResponseDtoConverter.convert(body.getBet());
    data.getReceipt().addAll(dtoList);
    return new RegularPlaceBetResponse(data);
  }

  private BetsDto.BetsDtoBuilder prepareLuckyDipBPPRequest(
      Outcome allottedPlayer,
      LuckyDipBetPlacementRequest request,
      com.egalacoral.spark.siteserver.model.Price price) {
    return BetsDto.builder()
        .amount(request.getStake())
        .outcomeRef(allottedPlayer.getId())
        .winPlaceRef(request.getWinType())
        .channel(request.getChannel())
        .clientUserAgent(replaceClientUserAgent(request))
        .betTag(LUCKY_DIP)
        .priceTypeRef(LP_PRICE_TYPE)
        .priceNum(price.getPriceNum())
        .priceDen(price.getPriceDen());
  }

  private String replaceClientUserAgent(LuckyDipBetPlacementRequest request) {
    if (Objects.nonNull(request.getChannel())) {
      switch (request.getChannel()) {
        case "A", "a", "Z", "z":
          return ANDROID_CHANNEL;
        case "I", "i", "Y", "y":
          return IOS_CHANNEL;
        default:
          throw new IllegalArgumentException("Channel is not correct");
      }
    }
    return request.getClientUserAgent();
  }

  private void processSuccessResponse(Session session, BetsResponse body) {
    if (ResponseUtils.isConfirmed(body.getBet().get(0))) {
      session.sendData(PLACE_BET_RESPONSE_CODE.code(), createSuccessResponse(body));
      selectionOperations.clearSelection(session);
    }
  }
}
