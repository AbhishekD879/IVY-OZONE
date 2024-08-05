package com.ladbrokescoral.cashout.payout;

import static com.ladbrokescoral.cashout.util.StringUtil.ifNotEmptyOrNull;
import static org.apache.commons.lang3.StringUtils.isNotEmpty;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetType;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicReference;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
public class PayoutRequestConverter {

  private static final String NO_DEDUCTION = "0";
  private static final String ACCA_BET_TYPE = "ACCA";
  private static final String EMPTY_STRING = "";
  private static final Pattern pattern = Pattern.compile("\\D");
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  /**
   * Building PayoutRequest using BetSummaryModel object
   *
   * @param betSummaryModel
   * @return PayoutRequest
   */
  public PayoutRequest buildPayoutRequest(BetSummaryModel betSummaryModel) {
    String foldSize = EMPTY_STRING;
    String betType = PayoutUtil.getBetType(betSummaryModel.getBetType());
    if (betType.equalsIgnoreCase(ACCA_BET_TYPE)) {
      foldSize = getFoldSize(betSummaryModel.getBetType());
    }
    return PayoutRequest.builder()
        .betId(betSummaryModel.getId())
        .stake(betSummaryModel.getStake().getStakePerLine())
        .betType(betType)
        .foldSize(foldSize)
        .tokenValue(getTokenValue(betSummaryModel.getStake().getTokenValue()))
        .legType(
            (betSummaryModel.getLeg().stream()
                .findAny()
                .map(leg -> leg.getLegType().getCode())
                .orElse(null)))
        .legs(betSummaryModel.getLeg().stream().map(this::buildLeg).collect(Collectors.toList()))
        .build();
  }

  private String getTokenValue(String tokenValue) {
    return Objects.nonNull(tokenValue) ? String.format("%.2f", Double.valueOf(tokenValue)) : null;
  }

  private String getFoldSize(BetType betType) {
    String accaBetCode = betType.getCode();
    if (accaBetCode.startsWith("AC")) {
      Matcher matcher = pattern.matcher(accaBetCode);
      return matcher.replaceAll(EMPTY_STRING);
    } else {
      return String.valueOf(accaBetCode.charAt(1));
    }
  }

  /**
   * Building PayoutLeg object using part object from bet
   *
   * @param leg
   * @return PayoutLeg
   */
  private PayoutLeg buildLeg(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.Leg leg) {
    AtomicReference<PayoutLeg> legs = new AtomicReference<>();
    List<PayoutLeg> payoutLeg =
        leg.getPart().stream()
            .map(
                (Part part) -> {
                  legs.set(
                      PayoutLeg.builder()
                          .id(part.getOutcome().get(0).getId())
                          .result(buildResult(part.getOutcome().get(0).getResult()))
                          .priceType(
                              part.getPrice().stream()
                                  .findAny()
                                  .map(price -> price.getPriceType().getCode())
                                  .orElse(EMPTY_STRING))
                          .strikePrice(buildStrikePrice(part.getPrice().stream().findAny()))
                          .startingPrice(buildStartingPrice(part.getPrice().stream().findAny()))
                          .eachWayFactor(
                              buildEachWayPrice(
                                  Optional.ofNullable(part.getEachWayTerms())
                                      .flatMap(eachWayTerms -> eachWayTerms.stream().findAny())))
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
                          .build());
                  return legs.get();
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug("payoutLeg:{}", payoutLeg);
    return legs.get();
  }

  /**
   * Building result object using ConfirmingResult object from bet
   *
   * @param result
   * @return
   */
  private String buildResult(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.ConfirmingResult result) {
    if (Objects.nonNull(result)
        && isNotEmpty(result.getValue())
        && !result.getValue().equals("-")) {
      return result.getValue();
    } else {
      return null;
    }
  }

  private PayoutPrice buildStrikePrice(
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price> priceOpt) {
    return priceOpt
        .map(
            price ->
                isNotEmpty(price.getPriceNum())
                    ? PayoutPrice.builder()
                        .numerator(price.getPriceNum())
                        .denominator(price.getPriceDen())
                        .build()
                    : null)
        .orElse(null);
  }

  private PayoutPrice buildStartingPrice(
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.Price> priceOpt) {
    return priceOpt
        .map(
            price ->
                isNotEmpty(price.getPriceStartingNum())
                    ? PayoutPrice.builder()
                        .numerator(price.getPriceStartingNum())
                        .denominator(ifNotEmptyOrNull(price.getPriceStartingDen()))
                        .build()
                    : null)
        .orElse(null);
  }

  private PayoutPrice buildEachWayPrice(
      Optional<com.coral.bpp.api.model.bet.api.response.accountHistory.response.EachWayTerms>
          eachWayTerms) {
    return eachWayTerms
        .map(
            eachWayTermsValue ->
                isNotEmpty(eachWayTermsValue.getEachWayNum())
                    ? PayoutPrice.builder()
                        .numerator(eachWayTermsValue.getEachWayNum())
                        .denominator(ifNotEmptyOrNull(eachWayTermsValue.getEachWayDen()))
                        .build()
                    : null)
        .orElse(null);
  }

  // building deduction object for betsummary model
  private Deduction buildDeduction(
      com.coral.bpp.api.model.bet.api.response.accountHistory.response.Deduction betDeduction) {
    ASYNC_LOGGER.debug(
        "betDeductionType::{},betDeductionValue::{}",
        betDeduction.getType(),
        betDeduction.getValue());
    if (NO_DEDUCTION.equals(betDeduction.getValue())) {
      return null;
    }
    if ("rule4".equals(betDeduction.getType())) {
      return buildDeductionRule4(betDeduction.getPriceType(), betDeduction.getValue());
    }
    return null;
  }

  // Rule4 deduction object

  private Deduction buildDeductionRule4(String priceType, String val) {
    return Deduction.builder()
        .deductionType("rule4")
        .deductionDetail(buildDeductionsRule4(val, priceType))
        .build();
  }

  private DeductionDetails buildDeductionsRule4(String val, String priceType) {
    return DeductionDetails.builder()
        .priceType(ifNotEmptyOrNull(priceType))
        .deductionFactor(Objects.nonNull(val) ? getDeductionVal(val) : 0)
        .build();
  }

  private Object getDeductionVal(String val) {
    if (val.contains(".")) {
      return (int) Double.parseDouble(val);
    } else {
      return Integer.parseInt(val);
    }
  }
}
