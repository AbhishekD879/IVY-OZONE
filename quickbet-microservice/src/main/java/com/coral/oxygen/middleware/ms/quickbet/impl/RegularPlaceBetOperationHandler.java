package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.component.IllegalOperationException;
import com.coral.oxygen.middleware.ms.quickbet.connector.BppComponent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapter;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetsDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.FreeBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetError;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.service.BettingService;
import com.newrelic.api.agent.NewRelic;
import io.vavr.Tuple;
import io.vavr.Tuple2;
import io.vavr.control.Either;
import java.text.MessageFormat;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;

@Component
public class RegularPlaceBetOperationHandler {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private static final String SCORECAST_OUTCOME_COMBIREF = "SCORECAST";
  private static final String LP_PRICE_TYPE = "LP";
  private static final String SP_PRICE_TYPE = "SP";
  private static final String ANDROID_CHANNEL = "S|W|A0000000";
  private static final String IOS_CHANNEL = "S|W|I0000000";

  private final BppComponent bppComponent;
  private final BettingService bettingService;
  private final BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter;
  private final NotConfirmedBetsHandler notConfirmedBetsHandler;
  private final SelectionOperations selectionOperations;
  private final LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler;

  public RegularPlaceBetOperationHandler(
      BppComponent bppComponent,
      BettingService bettingService,
      BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter,
      NotConfirmedBetsHandler notConfirmedBetsHandler,
      SelectionOperations selectionOperations,
      LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler) {
    this.bppComponent = bppComponent;
    this.bettingService = bettingService;
    this.betToReceiptResponseDtoConverter = betToReceiptResponseDtoConverter;
    this.notConfirmedBetsHandler = notConfirmedBetsHandler;
    this.selectionOperations = selectionOperations;
    this.luckDipPlaceBetOperationHandler = luckDipPlaceBetOperationHandler;
  }

  public void placeBet(Session session, RegularPlaceBetRequest request) {

    bppComponent
        .fetchUserData(request.getToken())
        .onSuccess(userData -> MDC.put("username", userData.getSportBookUserName()));

    try {
      RegularSelectionResponse selectionResponse = session.getRegularSelectionResponse();
      ASYNC_LOGGER.info(
          "Regular PlaceBet Input Request :{}, session selection Response: {}",
          request,
          selectionResponse);
      if (selectionResponse == null) {
        throw new IllegalOperationException(
            "Can't find selection data in remote bet slip for session " + session);
      }
      validateRequest(request);
      if (selectionResponse.isLDip()) {
        LuckyDipBetPlacementRequest luckyDipRequest =
            buildLuckyDipRequest(request, selectionResponse.getLDipMar());
        luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, luckyDipRequest);
      } else {
        RegularSelectionRequest selectionRequest = selectionResponse.getRequest();
        String outcomeId = String.valueOf(selectionRequest.getOutcomeIds().get(0));

        BetsDto betsDto =
            buildWhenOneMarketAndOurcome(selectionResponse)
                .andThen(b -> buildWhenScoreCast(selectionRequest).apply(b))
                .andThen(
                    b -> buildHandicap(request, selectionResponse.getSelectionPrice()).apply(b))
                .andThen(b -> buildPrice(session, request, selectionResponse).apply(b))
                .andThen(b -> buildFreebet(request, selectionResponse).apply(b))
                .apply(
                    BetsDto.builder()
                        .amount(request.getStake())
                        .outcomeRef(outcomeId)
                        .winPlaceRef(request.getWinType())
                        .channel(request.getChannel())
                        .clientUserAgent(replaceClientUserAgent(request)))
                .build();

        GeneralResponse<BetsResponse> generalResponse =
            bettingService.placeBet(request.getToken(), betsDto);
        handleErrors(generalResponse, selectionRequest)
            .fold(
                error -> {
                  session.sendData(PLACE_BET_ERROR_RESPONSE_CODE.code(), error);
                  return null;
                },
                body -> {
                  Long freebetId = null;
                  if (Objects.nonNull(request.getFreebet())) {
                    freebetId = request.getFreebet().getId();
                  }
                  processSuccessResponse(session, body, request.getToken(), freebetId);
                  return null;
                });
      }

    } catch (SiteServException e) {
      NewRelic.noticeError(e);
      ASYNC_LOGGER.error("Error place bet. {}", e.getDesc(), e);
      sendSiteServerException(session, e);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      ASYNC_LOGGER.error("Error place bet", e);
      session.sendData(
          PLACE_BET_ERROR_RESPONSE_CODE.code(),
          RegularPlaceBetResponse.errorResponse(
              INTERNAL_PLACE_BET_PROCESSING.code(), e.getMessage()));
    }
  }

  private LuckyDipBetPlacementRequest buildLuckyDipRequest(
      RegularPlaceBetRequest request, String luckyDipMarket) {
    LuckyDipBetPlacementRequest luckyDipBetPlacementRequest =
        new LuckyDipBetPlacementRequest(
            request.getToken(), request.getStake(), luckyDipMarket, request.getWinType());
    luckyDipBetPlacementRequest.setChannel(request.getChannel());
    luckyDipBetPlacementRequest.setClientUserAgent(request.getClientUserAgent());
    luckyDipBetPlacementRequest.setIp(request.getIp());
    return luckyDipBetPlacementRequest;
  }

  private void validateRequest(RegularPlaceBetRequest request) {
    if (org.apache.commons.lang3.StringUtils.isEmpty(request.getWinType())) {
      throw new IllegalArgumentException("WinType can't be empty");
    }
    if (request.getStake() == null || request.getStake().equals("")) {
      throw new SiteServException(
          PLACE_BET_ERROR_RESPONSE_CODE, STAKE_EMPTY.code(), "Stake is empty");
    }
  }

  private Function<BetsDto.BetsDtoBuilder, BetsDto.BetsDtoBuilder> buildWhenOneMarketAndOurcome(
      RegularSelectionResponse selectionResponse) {
    return builder -> {
      if (selectionResponse.getEvent().getMarkets().size() == 1
          && selectionResponse.getEvent().getMarkets().get(0).getOutcomes().size() == 1) {
        builder.outcomeMeaningMajorCode(
            selectionResponse
                .getEvent()
                .getMarkets()
                .get(0)
                .getOutcomes()
                .get(0)
                .getOutcomeMeaningMajorCode());
      }
      return builder;
    };
  }

  private Function<BetsDto.BetsDtoBuilder, BetsDto.BetsDtoBuilder> buildWhenScoreCast(
      RegularSelectionRequest selectionRequest) {
    return builder -> {
      if (isScorecast(selectionRequest)) {
        builder.outcomeCombiRef(SCORECAST_OUTCOME_COMBIREF);
        builder.additionalOutcomeRefs(
            selectionRequest
                .getOutcomeIds()
                .subList(1, selectionRequest.getOutcomeIds().size())
                .stream()
                .map(String::valueOf)
                .toList());
      }
      return builder;
    };
  }

  private Either<RegularPlaceBetResponse, BetsResponse> handleErrors(
      GeneralResponse<BetsResponse> generalResponse, RegularSelectionRequest selectionRequest) {
    ErrorBody errorBody = generalResponse.getErrorBody();
    if (errorBody != null) {
      return Either.left(createErrorResponse(errorBody));
    } else {
      BetsResponse body = generalResponse.getBody();
      List<BetError> betError = body.getBetError();
      if (betError != null && !betError.isEmpty()) {
        RegularPlaceBetResponse errorResponse = createErrorResponse(body);
        if (isScorecast(selectionRequest)) {
          errorResponse.getData().getError().setPrice(null);
        }
        return Either.left(errorResponse);
      } else {
        return Either.right(body);
      }
    }
  }

  private boolean isScorecast(RegularSelectionRequest selectionRequest) {
    return RegularSelectionRequest.SCORECAST_SELECTION_TYPE.equals(
        selectionRequest.getSelectionType());
  }

  private RegularPlaceBetResponse createErrorResponse(BetsResponse body) {
    return RegularPlaceBetResponse.errorResponse(body);
  }

  private RegularPlaceBetResponse createErrorResponse(ErrorBody errorBody) {
    return RegularPlaceBetResponse.errorResponse(errorBody.getStatus(), errorBody.getError());
  }

  private void processSuccessResponse(
      Session session, BetsResponse body, String bppToken, Long freeBetId) {
    ASYNC_LOGGER.info(
        "BetsResponse:{} session:{}", body.getBet().get(0), session.getRegularSelectionResponse());
    if (isConfirmed(body.getBet().get(0))) {
      session.sendData(PLACE_BET_RESPONSE_CODE.code(), createSuccessResponse(body, freeBetId));
      selectionOperations.clearSelection(session);
    } else {
      notConfirmedBetsHandler.handle(session, new MultiReadBetResponseAdapter(body), bppToken);
    }
  }

  private boolean isConfirmed(Bet bet) {
    return YesNo.Y.equals(bet.getIsConfirmed());
  }

  private RegularPlaceBetResponse createSuccessResponse(BetsResponse body, Long freebetId) {
    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    Collection<ReceiptResponseDto> dtoList =
        betToReceiptResponseDtoConverter.convert(body.getBet());
    data.getReceipt().addAll(dtoList);
    data.getReceipt().get(0).setFreebetId(freebetId);
    return new RegularPlaceBetResponse(data);
  }

  private Function<BetsDto.BetsDtoBuilder, BetsDto.BetsDtoBuilder> buildHandicap(
      RegularPlaceBetRequest request, OutputPrice price) {
    return builder -> {
      if (price != null) {
        String handicapValueDec =
            (request.getHandicap() == null || request.getHandicap().equals(""))
                ? price.getHandicapValueDec()
                : request.getHandicap();
        builder.handicapValueDec(fixHandicapValueDec(handicapValueDec));
      }
      return builder;
    };
  }

  private Function<BetsDto.BetsDtoBuilder, BetsDto.BetsDtoBuilder> buildPrice(
      Session session, RegularPlaceBetRequest request, RegularSelectionResponse selectionResponse) {
    return builder -> {
      if (SP_PRICE_TYPE.equalsIgnoreCase(request.getPrice())) {
        builder.priceTypeRef(SP_PRICE_TYPE);
      } else {
        final Tuple2<Integer, Integer> numAndDen =
            convertPrice(request.getPrice(), session.sessionId());
        builder.priceTypeRef(LP_PRICE_TYPE).priceNum(numAndDen._1).priceDen(numAndDen._2);

        if (isGuaranteedPrice(selectionResponse)) {
          builder.priceTypeRef("GUARANTEED");
        }
      }
      return builder;
    };
  }

  private Function<BetsDto.BetsDtoBuilder, BetsDto.BetsDtoBuilder> buildFreebet(
      RegularPlaceBetRequest request, RegularSelectionResponse selectionResponse) {
    return builder -> {
      if (Objects.nonNull(request.getFreebet())) {
        if (Objects.nonNull(selectionResponse.getOddsBoost())
            && request.getFreebet().isOddsBoost()) {
          builder.enhancedPriceDen(
              Integer.valueOf(selectionResponse.getOddsBoost().getEnhancedOddsPriceDen()));
          builder.enhancedPriceNum(
              Integer.valueOf(selectionResponse.getOddsBoost().getEnhancedOddsPriceNum()));
          builder.freebet(
              new FreeBetDto(Long.valueOf(selectionResponse.getOddsBoost().getId()), "0"));
        } else {
          builder.freebet(
              new FreeBetDto(request.getFreebet().getId(), request.getFreebet().getStake()));
        }
      }
      return builder;
    };
  }

  private Tuple2<Integer, Integer> convertPrice(String price, String sessionId) {
    try {
      int priceNum = Integer.parseInt(price.split("/")[0]);
      int priceDen = Integer.parseInt(price.split("/")[1]);
      return Tuple.of(priceNum, priceDen);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      ASYNC_LOGGER.warn("Error parsing price {} in session {}. ", price, sessionId);
      throw new SiteServException(
          PLACE_BET_ERROR_RESPONSE_CODE,
          BAD_PRICE.code(),
          MessageFormat.format(
              " Exception during parsing price {0} for session {1} ", price, sessionId));
    }
  }

  private String replaceClientUserAgent(RegularPlaceBetRequest request) {
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

  private String fixHandicapValueDec(String handicapValueDec) {
    if (handicapValueDec == null) {
      return null;
    } else if (handicapValueDec.endsWith(",")) {
      return handicapValueDec.substring(0, handicapValueDec.length() - 1);
    }
    return handicapValueDec;
  }

  private boolean isGuaranteedPrice(RegularSelectionResponse selectionResponse) {
    RegularSelectionRequest request = selectionResponse.getRequest();
    return RegularSelectionRequest.SIMPLE_SELECTION_TYPE.equals(request.getSelectionType())
        && Boolean.TRUE.equals(selectionResponse.getEvent().getMarkets().get(0).getIsGpAvailable());
  }

  private void sendSiteServerException(Session session, SiteServException e) {
    session.sendData(e.getMsg().code(), e.getResponse());
  }
}
