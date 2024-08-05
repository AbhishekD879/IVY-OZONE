package com.coral.oxygen.middleware.ms.quickbet.util;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.ValidPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.DataResponseWrapper;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.*;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.*;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class BanachUtils {

  public static final String UNKNOWN_ERROR_CODE = "UNKNOWN_SELECTION_ERROR";
  public static final String UNKNOWN_ERROR_MESSAGE = "Unknown selection error";
  public static final String COMPONENT_SUSPENDED_ERROR_CODE = "COMPONENT_SUSPENDED";
  public static final String COMPONENT_SUSPENDED_ERROR_MESSAGE =
      "One or more of the selection component(s) are suspended";
  public static final String INVALID_COMBINATION_ERROR_CODE = "INVALID_COMBINATION";
  public static final String INVALID_COMBINATION_ERROR_MESSAGE =
      "Selection components cannot be combined";
  public static final String INVALID_MARGINATED_PRICE_ERROR_CODE = "INVALID_MARGINATED_PRICE";
  public static final String INVALID_MARGINATED_PRICE_ERROR_MESSAGE =
      "Selection price has imposibly low probability";

  private BanachUtils() {}

  public static ErrorMessage addSelectionErrorMessage(
      GetPriceResponseDto.ResponseCodeEnum responseCode) {
    int responseCodeValue = responseCode.ordinal();
    switch (responseCode) {
      case UNKNOWN:
        return new ErrorMessage(UNKNOWN_ERROR_CODE, responseCodeValue, UNKNOWN_ERROR_MESSAGE);
      case COMPONENT_SUSPENDED:
        return new ErrorMessage(
            COMPONENT_SUSPENDED_ERROR_CODE, responseCodeValue, COMPONENT_SUSPENDED_ERROR_MESSAGE);
      case INVALID_COMBINATION:
        return new ErrorMessage(
            INVALID_COMBINATION_ERROR_CODE, responseCodeValue, INVALID_COMBINATION_ERROR_MESSAGE);
      case INVALID_MARGINATED_PRICE:
        return new ErrorMessage(
            INVALID_MARGINATED_PRICE_ERROR_CODE,
            responseCodeValue,
            INVALID_MARGINATED_PRICE_ERROR_MESSAGE);
      default:
        throw new IllegalArgumentException(responseCode.name() + " is not error response code");
    }
  }

  public static DataResponseWrapper<BanachPlaceBetResponse> toQuickBetResponse(
      PlaceBetResponseDto banachData) {
    BanachPlaceBetResponse.BanachPlaceBetResponseBuilder responseBuilder =
        BanachPlaceBetResponse.builder();

    Optional.ofNullable(banachData.getBetPlacement())
        .filter(list -> !list.isEmpty())
        .ifPresent(
            betPlacementResponseDtos ->
                betPlacementResponseDtos.stream()
                    .map(BanachUtils::mapBetPlacement)
                    .forEach(responseBuilder::betPlacementItem));

    Optional.ofNullable(banachData.getBetFailure())
        .ifPresent(
            banachBetFailure ->
                responseBuilder.betFailure(
                    BetFailure.builder()
                        .betNo(banachBetFailure.getBetNo())
                        .betMaxStake(banachBetFailure.getBetMaxStake())
                        .betMinStake(banachBetFailure.getBetMaxStake())
                        .betError(BanachUtils.mapBetErrors(banachBetFailure.getBetError()))
                        .build()));

    Optional.ofNullable(banachData.getValidPrice())
        .ifPresent(
            banachValidPrice ->
                responseBuilder.validPrice(
                    ValidPrice.builder()
                        .priceNum(banachValidPrice.getPriceNum())
                        .priceDen(banachValidPrice.getPriceDen())
                        .build()));

    Optional.ofNullable(banachData.getResponseCode())
        .map(PlaceBetResponseDto.ResponseCodeEnum::ordinal)
        .ifPresent(responseBuilder::responseCode);

    return new DataResponseWrapper<>(responseBuilder.build());
  }

  private static List<BetErrorItem> mapBetErrors(List<BetErrorDto> banachBetErrors) {
    return banachBetErrors.stream().map(BanachUtils::mapBetError).collect(Collectors.toList());
  }

  private static BetErrorItem mapBetError(BetErrorDto banachBetError) {
    Optional<BetFailureDetailDto> banachBetFailureDetail =
        Optional.ofNullable(banachBetError.getBetFailureDetail());
    BetErrorItem.BetErrorItemBuilder betErrorItemBuilder = BetErrorItem.builder();
    betErrorItemBuilder
        .betFailureCode(banachBetError.getBetFailureCode())
        .betFailureDesc(banachBetError.getBetFailureDesc())
        .betFailureDebug(banachBetError.getBetFailureDebug())
        .betFailureReason(banachBetError.getBetFailureReason());
    banachBetFailureDetail.ifPresent(
        detail ->
            betErrorItemBuilder.betFailureDetail(
                BetFailureDetail.builder()
                    .eventId(detail.getEventId())
                    .eventName(detail.getEventName())
                    .outcomeId(detail.getOutcomeId())
                    .outcomeName(detail.getOutcomeName())
                    .priceNum(detail.getPriceNum())
                    .priceDen(detail.getPriceDen())
                    .variantId(detail.getVariantId())
                    .build()));

    return betErrorItemBuilder.build();
  }

  private static BetPlacementItem mapBetPlacement(BetPlacementResponseDto betPlacementDto) {
    return BetPlacementItem.builder()
        .betId(betPlacementDto.getBetId())
        .betNo(betPlacementDto.getBetNo())
        .betPotentialWin(betPlacementDto.getBetPotentialWin())
        .date(betPlacementDto.getDate())
        .numLines(betPlacementDto.getNumLines())
        .totalStake(betPlacementDto.getTotalStake())
        .receipt(betPlacementDto.getReceipt())
        .build();
  }

  public static ErrorMessage addSelectionExceptionMessage(Throwable t) {
    return new ErrorMessage(
        Messages.ERROR_CODE.code(), "Failed to get price on Banach selection: " + t.getMessage());
  }

  public static boolean isErrorPresent(
      PlaceBetResponseDto response, Collection<String> betFailureCodes) {
    return Optional.ofNullable(response)
        .map(PlaceBetResponseDto::getBetFailure)
        .map(BetFailureResponseDto::getBetError)
        .filter(
            betErrors ->
                betErrors.stream()
                    .map(BetErrorDto::getBetFailureCode)
                    .map(String::valueOf)
                    .anyMatch(betFailureCodes::contains))
        .isPresent();
  }
}
