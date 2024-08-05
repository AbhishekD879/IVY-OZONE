package com.ladbrokescoral.cashout.util;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.math.BigInteger;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.experimental.UtilityClass;
import org.apache.commons.lang3.math.NumberUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.util.CollectionUtils;

@UtilityClass
public class BetUtil {

  private static final String HR_CATEGORY_ID = "21";

  public static boolean isBetCashoutAvailable(Bet bet) {
    return NumberUtils.isNumber(bet.getCashoutValue());
  }

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public static List<Bet> filterEventBets(List<Bet> bets, String eventId) {
    return bets.stream()
        .filter(bet -> isBetBelongsToEvent(bet, eventId))
        .collect(Collectors.toList());
  }

  public List<BetSummaryModel> filterAccHistoryBetsWithCashoutValuePresent(
      InitialAccountHistoryBetResponse bets) {
    List<BetSummaryModel> betList =
        Optional.ofNullable(bets.getBets()).orElse(Collections.emptyList());
    return betList.stream()
        .filter(
            bet ->
                NumberUtils.isCreatable(bet.getCashoutValue())
                    || "CASHOUT_SELN_SUSPENDED".equals(bet.getCashoutValue())
                    || "CASHOUT_SELN_NO_CASHOUT".equals(getCashoutValueFromHRBet(bet)))
        .collect(Collectors.toList());
  }

  public static String getCashoutValueFromHRBet(BetSummaryModel bet) {
    boolean flag =
        Optional.ofNullable(bet.getLeg())
            .map(
                legs ->
                    legs.stream()
                        .flatMap(leg -> leg.getPart().stream())
                        .flatMap(part -> part.getOutcome().stream())
                        .anyMatch(
                            outcome ->
                                HR_CATEGORY_ID.equalsIgnoreCase(
                                    outcome.getEventCategory().getId())))
            .orElse(false);
    ASYNC_LOGGER.debug(
        "BetUtil getCashoutValueFromHRBet betId {} CashoutValue {} flag {} ",
        bet.getId(),
        bet.getCashoutValue(),
        flag);
    return flag ? bet.getCashoutValue() : "SELN_NOT_MATCHED";
  }

  private static boolean isBetBelongsToEvent(Bet bet, String eventId) {
    return Optional.ofNullable(bet.getLeg())
        .map(
            legs ->
                legs.stream()
                    .filter(leg -> !CollectionUtils.isEmpty(leg.getPart()))
                    .flatMap(leg -> leg.getPart().stream())
                    .anyMatch(part -> eventId.equals(part.getEventId())))
        .orElse(false);
  }

  public static boolean isBanachBet(Bet bet) {
    String betChannel = bet.getSource();
    return "e".equalsIgnoreCase(betChannel) || "f".equalsIgnoreCase(betChannel);
  }

  public static boolean isBanachBet(BetSummaryModel bet) {
    String betChannel = bet.getSource();
    return "e".equalsIgnoreCase(betChannel) || "f".equalsIgnoreCase(betChannel);
  }

  public static boolean isBetOnSPPrice(BetSummaryModel bet, BigInteger selectionId) {
    return isBetOnPriceType(bet, selectionId, "S");
  }

  public static boolean isBetOnLPPrice(BetSummaryModel bet, BigInteger selectionId) {
    return isBetOnPriceType(bet, selectionId, "L", "G");
  }

  private static boolean isBetOnPriceType(
      BetSummaryModel bet, BigInteger selectionId, String priceType) {
    return getPartStream(bet, selectionId)
        .filter(p -> Objects.nonNull(p.getPrice()))
        .flatMap(p -> p.getPrice().stream())
        .filter(price -> price.getPriceType() != null && price.getPriceType().getCode() != null)
        .anyMatch(price -> priceType.equals(price.getPriceType().getCode()));
  }

  private static boolean isBetOnPriceType(
      BetSummaryModel bet,
      BigInteger selectionId,
      String primaryPriceType,
      String secondaryPriceType) {
    return getPartStream(bet, selectionId)
        .filter(p -> Objects.nonNull(p.getPrice()))
        .flatMap(p -> p.getPrice().stream())
        .filter(price -> price.getPriceType() != null && price.getPriceType().getCode() != null)
        .anyMatch(
            price ->
                primaryPriceType.equals(price.getPriceType().getCode())
                    || secondaryPriceType.equals(price.getPriceType().getCode()));
  }

  private static Stream<Part> getPartStream(BetSummaryModel bet, BigInteger selectionId) {
    return bet.getLeg().stream()
        .flatMap(l -> l.getPart().stream())
        .filter(p -> String.valueOf(selectionId).equals(getOutcome(p).getId()));
  }

  public static boolean isBetOnHandicapMarket(BetSummaryModel bet, BigInteger selectionId) {
    return getPartStream(bet, selectionId).anyMatch(part -> isHandicap(part));
  }

  private static boolean isHandicap(Part part) {
    return getOutcome(part).getMarket().isHandicap();
  }

  private static Outcome getOutcome(Part part) {
    return part.getOutcome().get(0);
  }
}
