package com.ladbrokescoral.cashout.converter;

import static com.ladbrokescoral.cashout.util.StringUtil.ifNotEmptyOrDefault;
import static com.ladbrokescoral.cashout.util.StringUtil.ifNotEmptyOrNull;
import static org.apache.commons.lang3.StringUtils.isEmpty;
import static org.apache.commons.lang3.StringUtils.isNotEmpty;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.EachWayTerms;
import com.ladbrokescoral.cashout.api.client.entity.request.*;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

@Component
public class BetToCashoutOfferRequestConverter
    implements Converter<List<BetSummaryModel>, CashoutRequest> {

  private static final String HANDICAP_RESULT = "H";

  private static final String DEAD_HEAT_WIN_DEDUCTION = "deadheatWin";
  private static final String DEAD_HEAT_EACH_WAY_DEDUCTION = "deadheatPlace";
  private static final String RULE_4_SP_DEDUCTION = "rule4SP";
  private static final String RULE_4_LP_DEDUCTION = "rule4LP";
  private static final String NO_DEDUCTION = "0";

  @Override
  public CashoutRequest convert(List<BetSummaryModel> bets) {
    return CashoutRequest.builder()
        .cashoutOfferRequests(bets.stream().map(this::convert).collect(Collectors.toList()))
        .build();
  }

  private CashoutOfferRequest convert(com.coral.bpp.api.model.bet.api.response.oxi.base.Bet obBet) {
    return CashoutOfferRequest.builder()
        .cashoutOfferReqRef(obBet.getBetId())
        .bet(buildBet(obBet))
        .build();
  }

  private CashoutOfferRequest convert(BetSummaryModel obBet) {
    return CashoutOfferRequest.builder()
        .cashoutOfferReqRef(obBet.getId())
        .bet(buildBet(obBet))
        .build();
  }

  private CashoutBet buildBet(com.coral.bpp.api.model.bet.api.response.oxi.base.Bet obBet) {
    return CashoutBet.builder()
        .stakeAmount(obBet.getStake())
        .tokenValue(obBet.getTokenValue())
        .betType(obBet.getBetType())
        .legType(ifNotEmptyOrNull(obBet.getLegType()))
        .legs(obBet.getLeg().stream().map(this::buildLeg).collect(Collectors.toList()))
        .build();
  }

  private CashoutBet buildBet(BetSummaryModel obBet) {
    return CashoutBet.builder()
        .stakeAmount(obBet.getStake().getValue())
        .tokenValue(obBet.getStake().getTokenValue())
        .betType(obBet.getBetType().getCode())
        .cashoutProfile(obBet.getCashoutProfile())
        .legType(
            ifNotEmptyOrNull(
                obBet.getLeg().stream()
                    .findAny()
                    .map(leg -> leg.getLegType().getCode())
                    .orElse(null)))
        .legs(obBet.getLeg().stream().map(this::buildLeg).collect(Collectors.toList()))
        .build();
  }

  private CashoutLeg buildLeg(com.coral.bpp.api.model.bet.api.response.oxi.base.Leg leg) {
    return CashoutLeg.builder()
        .legNo(leg.getLegNo())
        .legSort(leg.getLegSort())
        .parts(leg.getPart().stream().map(this::buildPart).collect(Collectors.toList()))
        .build();
  }

  private CashoutLeg buildLeg(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.Leg leg) {
    return CashoutLeg.builder()
        .legNo(leg.getLegNo())
        .legSort(leg.getLegSort().getCode())
        .parts(
            leg.getPart().stream()
                .map(
                    part ->
                        buildPart(
                            part,
                            Optional.ofNullable(part.getEachWayTerms())
                                .flatMap(eachWayTerms -> eachWayTerms.stream().findAny()),
                            part.getPrice().stream().findAny()))
                .collect(Collectors.toList()))
        .build();
  }

  private CashoutPart buildPart(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part part,
      Optional<EachWayTerms> eachWayTerms,
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price> price) {
    return CashoutPart.builder()
        .partNo(part.getPartNo())
        .type(part.getCashoutLadder().getType())
        .ladder(part.getCashoutLadder().getValue())
        .result(part.getOutcome().get(0).getResult().getValue())
        .categoryId(part.getOutcome().get(0).getEventCategory().getId())
        .isOff(part.getOutcome().get(0).getEvent().getIsOff())
        .resultPlaces(
            ifNotEmptyOrNull(
                part.getOutcome().stream()
                    .findAny()
                    .map(outcome -> outcome.getResult().getPlaces())
                    .orElse("")))
        .eachWayDen(ifNotEmptyOrNull(eachWayTerms.map(EachWayTerms::getEachWayDen).orElse("")))
        .eachWayPlaces(
            ifNotEmptyOrNull(eachWayTerms.map(EachWayTerms::getEachWayPlaces).orElse("")))
        .previousOfferedPlaces(
            ifNotEmptyOrNull(eachWayTerms.map(EachWayTerms::getPreviousOfferedPlaces).orElse("")))
        .priceType(price.map(price1 -> price1.getPriceType().getCode()).orElse(""))
        .strikePrice(buildStrikePrice(price))
        .spotPrice(buildSpotPrice(price))
        .returnedSP(buildReturnedSPPrice(price))
        .deductions(
            Optional.ofNullable(part.getDeduction())
                .map(
                    deductions ->
                        deductions.stream()
                            .map(this::buildDeduction)
                            .filter(Objects::nonNull)
                            .collect(Collectors.toList()))
                .filter(list -> !list.isEmpty())
                .orElse(null))
        .build();
  }

  private CashoutPart buildPart(com.coral.bpp.api.model.bet.api.response.oxi.base.Part part) {
    return CashoutPart.builder()
        .partNo(part.getPartNo())
        .type(part.getCashoutLadder().getType())
        .ladder(part.getCashoutLadder().getValue())
        .result(buildResult(part))
        .resultPlaces(ifNotEmptyOrNull(part.getResultPlaces()))
        .eachWayDen(ifNotEmptyOrNull(part.getEachWayDen()))
        .eachWayPlaces(ifNotEmptyOrNull(part.getEachWayPlaces()))
        .priceType(part.getPriceType())
        .strikePrice(buildStrikePrice(part))
        .spotPrice(buildSpotPrice(part))
        .returnedSP(buildReturnedSPPrice(part))
        .deductions(buildDeductions(part))
        .build();
  }

  /*-
   * The ‘result’ for a handicap selection is always ‘H’, and the actual result is in ‘dispResult’.
   */
  private String buildResult(com.coral.bpp.api.model.bet.api.response.oxi.base.Part part) {
    return part.getResult().equals(HANDICAP_RESULT) ? part.getDispResult() : part.getResult();
  }

  private String buildResult(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part part) {
    return part.getOutcome().stream()
        .findAny()
        .map(outcome -> outcome.getResult().getValue())
        .orElse(null); // todo check Handicap
  }

  /*-
   * strike price - price bet was placed on
   */
  private CashoutPrice buildStrikePrice(
      com.coral.bpp.api.model.bet.api.response.oxi.base.Part part) {
    return isNotEmpty(part.getPriceNum())
        ? CashoutPrice.builder().num(part.getPriceNum()).den(part.getPriceDen()).build()
        : null;
  }

  private CashoutPrice buildStrikePrice(
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price> priceOpt) {
    return priceOpt
        .map(
            price ->
                isNotEmpty(price.getPriceNum())
                    ? CashoutPrice.builder()
                        .num(price.getPriceNum())
                        .den(price.getPriceDen())
                        .build()
                    : null)
        .orElse(null);
  }

  /*-
   * spotPrice - up-to-date price of the bet
   */
  private CashoutPrice buildSpotPrice(com.coral.bpp.api.model.bet.api.response.oxi.base.Part part) {
    if (isEmpty(part.getCurrentPriceNum()) && isEmpty(part.getPriceNum())) {
      return null;
    }
    return CashoutPrice.builder()
        .num(ifNotEmptyOrDefault(part.getCurrentPriceNum(), part.getPriceNum()))
        .den(ifNotEmptyOrDefault(part.getCurrentPriceDen(), part.getPriceDen()))
        .build();
  }

  private CashoutPrice buildSpotPrice(
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price> priceOpt) {
    return priceOpt
        .map(
            price -> {
              if (isEmpty(price.getCurrentPriceNum()) && isEmpty(price.getPriceNum())) {
                return null;
              }
              return CashoutPrice.builder()
                  .num(ifNotEmptyOrDefault(price.getCurrentPriceNum(), price.getPriceNum()))
                  .den(ifNotEmptyOrDefault(price.getCurrentPriceDen(), price.getPriceDen()))
                  .build();
            })
        .orElse(null);
  }

  /*-
   * returnedSp - returned starting price
   */
  private CashoutPrice buildReturnedSPPrice(
      com.coral.bpp.api.model.bet.api.response.oxi.base.Part part) {
    return isNotEmpty(part.getStartPriceNum())
        ? CashoutPrice.builder().num(part.getStartPriceNum()).den(part.getStartPriceDen()).build()
        : null;
  }

  private CashoutPrice buildReturnedSPPrice(
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price> priceOpt) {
    return priceOpt
        .map(
            price ->
                isNotEmpty(price.getPriceStartingNum())
                    ? CashoutPrice.builder()
                        .num(price.getPriceStartingNum())
                        .den(price.getPriceStartingDen())
                        .build()
                    : null)
        .orElse(null);
  }

  private List<Deduction> buildDeductions(
      com.coral.bpp.api.model.bet.api.response.oxi.base.Part part) {

    List<Deduction> deductions = new ArrayList<>();

    if (Objects.nonNull(part.getDeadHeatWinDeductions())
        && !NO_DEDUCTION.equals(part.getDeadHeatWinDeductions())) {
      deductions.add(buildDeduction(DEAD_HEAT_WIN_DEDUCTION, part.getDeadHeatWinDeductions()));
    }
    if (Objects.nonNull(part.getDeadHeatEachWayDeductions())
        && !NO_DEDUCTION.equals(part.getDeadHeatEachWayDeductions())) {
      deductions.add(
          buildDeduction(DEAD_HEAT_EACH_WAY_DEDUCTION, part.getDeadHeatEachWayDeductions()));
    }
    if (Objects.nonNull(part.getRule4Deductions())
        && !NO_DEDUCTION.equals(part.getRule4Deductions())) {
      deductions.add(buildDeduction(RULE_4_SP_DEDUCTION, part.getRule4Deductions()));
      deductions.add(buildDeduction(RULE_4_LP_DEDUCTION, part.getRule4Deductions()));
    }
    return !deductions.isEmpty() ? deductions : null;
  }

  private Deduction buildDeduction(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.Deduction betDeduction) {
    if ("0".equals(betDeduction.getValue())) {
      return null;
    }
    if ("deadHeatWin".equals(betDeduction.getType())) {
      return buildDeduction(DEAD_HEAT_WIN_DEDUCTION, betDeduction.getValue());
    }
    if ("deadHeatEachWay".equals(betDeduction.getType())) {
      return buildDeduction(DEAD_HEAT_EACH_WAY_DEDUCTION, betDeduction.getValue());
    }
    if ("rule4".equals(betDeduction.getType())) {
      if ("L".equals(betDeduction.getPriceType())) {
        return buildDeduction(RULE_4_LP_DEDUCTION, betDeduction.getValue());
      }
      if ("S".equals(betDeduction.getPriceType())) {
        return buildDeduction(RULE_4_SP_DEDUCTION, betDeduction.getValue());
      }
    }
    return null;
  }

  /*-
   * Converting percentageValue to num & den
   */
  private Deduction buildDeduction(String name, String percentageValue) {
    return Deduction.builder().type(name).num(percentageValue).den("100").build();
  }
}
