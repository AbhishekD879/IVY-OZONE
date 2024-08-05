package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UIBet;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UILeg;
import com.coral.oxygen.middleware.ms.quickbet.util.codes.ErrorDetailLevel;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Part;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PlaceBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PrevTerm;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PrevTerms;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Token;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuild;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetCombination;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.EnhancedOdd;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.EnhancedPrice;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.FreebetToken;
import io.vavr.collection.List;
import io.vavr.collection.Set;
import io.vavr.control.Option;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.util.Collections;
import java.util.UUID;
import org.springframework.stereotype.Component;

@Component
public class PlaceBetRequestConverter {

  public static final String BETBOOST_FREEBET_TOKEN_TYPE = "BETBOOST";
  public static final String ODDS_BOOST_REASON_CODE = "ODDS_BOOST";
  static final String PRICE_TYPE_GUARANTEED = "G";

  public PlaceBetDto convert(Session session, UIPlaceBetRequest placeBetRequest) {

    String bppToken = session.getToken();
    Set<Bet> bets = createBets(session, placeBetRequest);

    return PlaceBetDto.builder()
        .token(Token.builder().value(bppToken).build())
        .errorDetail(ErrorDetailLevel.ALL.getCode())
        .channel(placeBetRequest.getChannel())
        .fullDetails(YesNo.Y.name())
        .clientUserAgent(placeBetRequest.getClientUserAgent())
        .remoteUniqueId(generateUniqueDigitBasedId())
        .bet(bets.toJavaSet())
        .errorOnDelay(YesNo.N)
        .build();
  }

  private Set<Bet> createBets(Session session, UIPlaceBetRequest placeBetRequest) {
    return placeBetRequest.getUiBets().map(bet -> convertBet(session, bet)).toSet();
  }

  private Bet convertBet(Session session, UIBet uiBet) {
    BetBuild betBuild = getBetBuild(session, uiBet);
    String betNoOfLines = getBetNoOfLines(betBuild, uiBet.getBetType());
    boolean isBetBoost = isBetBoost(uiBet, betBuild);
    Bet.BetBuilder builder =
        Bet.builder()
            .legType(uiBet.getWinType())
            .leg(convertLegs(betBuild, uiBet, isBetBoost, session).toJavaSet())
            .betType(uiBet.getBetType())
            .stakePerLine(calculateStakePerLine(uiBet, betBuild, new BigDecimal(betNoOfLines)))
            .betNo(uiBet.getBetNo());
    Option.of(uiBet.getFreebetTokenIds()).map(List::asJava).forEach(builder::freebetTokenId);
    if (isBetBoost) {
      builder.prevTerms(createPrevTerms(betBuild, uiBet, session));
    }
    return builder.build();
  }

  private PrevTerms createPrevTerms(BetBuild betBuild, UIBet uiBet, Session session) {
    PrevTerm prevTerm =
        PrevTerm.builder()
            .reasonCode(ODDS_BOOST_REASON_CODE)
            .priorityOrder("1")
            .leg(convertLegs(betBuild, uiBet, false, session).toJavaSet())
            .build();

    return PrevTerms.builder().prevTerm(Collections.singletonList(prevTerm)).build();
  }

  private boolean isBetBoost(UIBet uiBet, BetBuild betBuild) {
    return uiBet.getFreebetTokenIds() != null
        && betBuild.getFreebetToken().stream()
            .filter(this::isBetBoostToken)
            .map(FreebetToken::getFreebetTokenId)
            .anyMatch(freebetTokenId -> uiBet.getFreebetTokenIds().contains(freebetTokenId));
  }

  private String generateUniqueDigitBasedId() {

    return String.format(
        "%040d", new BigInteger(UUID.randomUUID().toString().replace("-", ""), 16));
  }

  private String getBetNoOfLines(BetBuild betBuild, String betType) {

    return betBuild.getBetCombination().stream()
        .filter(betCombination -> betCombination.getBetType().equals(betType))
        .findFirst()
        .map(BetCombination::getBetNoOfLines)
        .orElseThrow(
            () ->
                new IllegalArgumentException(
                    "Cannot find in BetBuild number of lines corresponding to: " + betType));
  }

  private BetBuild getBetBuild(Session session, UIBet uiBet) {

    return session.getBetBuildResponseModel().getBetBuild().stream()
        .filter(betBuild -> betBuild.getBetNo().equals(uiBet.getBetNo()))
        .findFirst()
        .orElseThrow(
            () ->
                new IllegalArgumentException(
                    "Cannot find corresponding BetBuild to UIBet: " + uiBet));
  }

  private String calculateStakePerLine(UIBet uiBet, BetBuild betBuild, BigDecimal betNoOfLines) {

    List<FreebetToken> allAvailableFreebetTokensForBet = List.ofAll(betBuild.getFreebetToken());
    List<FreebetToken> requestedFreebetTokens =
        getRequestedFreebetTokens(uiBet, allAvailableFreebetTokensForBet);

    BigDecimal freebetStakePerLine =
        requestedFreebetTokens
            .filter(this::isNotBetBoostToken)
            .map(freebetToken -> new BigDecimal(freebetToken.getFreebetTokenValue()))
            .fold(
                BigDecimal.ZERO,
                (sum, freebetTokenValue) ->
                    sum.add(freebetTokenValue.divide(betNoOfLines, 2, RoundingMode.DOWN)));

    return new BigDecimal(uiBet.getStakePerLine()).add(freebetStakePerLine).toString();
  }

  private boolean isBetBoostToken(FreebetToken freebetToken) {
    return BETBOOST_FREEBET_TOKEN_TYPE.equals(freebetToken.getFreebetTokenType());
  }

  private boolean isNotBetBoostToken(FreebetToken freebetToken) {
    return !isBetBoostToken(freebetToken);
  }

  private List<FreebetToken> getRequestedFreebetTokens(
      UIBet uiBet, List<FreebetToken> allAvailableFreebetTokensForBet) {
    return allAvailableFreebetTokensForBet.filter(
        freebetToken -> isRequestedFreeBetToken(uiBet, freebetToken));
  }

  private boolean isRequestedFreeBetToken(UIBet uiBet, FreebetToken freebetToken) {

    return Option.of(uiBet.getFreebetTokenIds())
        .map(uiBetFreebetTokens -> uiBetFreebetTokens.contains(freebetToken.getFreebetTokenId()))
        .getOrElse(false);
  }

  private Set<Leg> convertLegs(
      BetBuild betBuild, UIBet uiBet, boolean isBetBoost, Session session) {
    List<UILeg> uiLegs = Option.of(uiBet.getLegs()).getOrElse(List.empty());
    return uiLegs
        .zipWithIndex((leg, index) -> convertLeg(index + 1, leg, betBuild, isBetBoost, session))
        .toSet();
  }

  private Leg convertLeg(
      int legNo, UILeg uiLeg, BetBuild betBuild, boolean isBetBoost, Session session) {

    List<Part.PartBuilder> partBuilders = initPartBuilders(uiLeg, session);
    setPriceOnFirstPart(uiLeg, partBuilders);

    if (isBetBoost) {
      handleBetBoost(uiLeg, betBuild, partBuilders);
    }
    Set<Part> parts = partBuilders.map(Part.PartBuilder::build).toLinkedSet();

    Leg.LegBuilder legBuilder = Leg.builder().part(parts.toJavaSet()).legNo(legNo);
    uiLeg
        .getSelectionType()
        .map(ComplexSelection.Type::getLegSortCode)
        .forEach(legBuilder::legSort);
    return legBuilder.build();
  }

  private void handleBetBoost(UILeg uiLeg, BetBuild betBuild, List<Part.PartBuilder> partBuilders) {
    Option<EnhancedPrice> enhancedPrice =
        List.ofAll(betBuild.getEnhancedOdds().getEnhancedOdd())
            .filter(enhancedOdd -> uiLeg.getOutcomeIds().contains(enhancedOdd.getOutcome()))
            .headOption()
            .map(EnhancedOdd::getEnhancedPrice);
    enhancedPrice.forEach(
        ep ->
            partBuilders.update(
                0,
                partBuilder -> {
                  setBetboostPrice(partBuilder, ep);
                  return partBuilder;
                }));
  }

  private List<Part.PartBuilder> initPartBuilders(UILeg uiLeg, Session session) {
    return uiLeg
        .getOutcomeIds()
        .zipWithIndex(
            (outcomeId, index) ->
                Part.builder()
                    .outcome(outcomeId)
                    .priceType(getPriceType(uiLeg, session))
                    .partNo(index + 1));
  }

  private List<Part.PartBuilder> setPriceOnFirstPart(
      UILeg uiLeg, List<Part.PartBuilder> partBuilders) {
    return partBuilders.update(
        0,
        partBuilder -> {
          partBuilder.priceNum(uiLeg.getPriceNum());
          partBuilder.priceDen(uiLeg.getPriceDen());
          return partBuilder;
        });
  }

  private void setBetboostPrice(Part.PartBuilder builder, EnhancedPrice enhancedPrice) {
    builder
        .priceDen(Integer.valueOf(enhancedPrice.getPriceDen()))
        .priceNum(Integer.valueOf(enhancedPrice.getPriceNum()));
  }

  private String getPriceType(UILeg uiLeg, Session session) {
    return isGpAvailable(uiLeg, session) ? PRICE_TYPE_GUARANTEED : uiLeg.getPriceType();
  }

  private boolean isGpAvailable(UILeg uiLeg, Session session) {
    return uiLeg
        .getOutcomeIds()
        .exists(
            outcomeId ->
                session
                    .getOutcomeEvent(outcomeId)
                    .map(event -> event.getMarkets().get(0).getIsGpAvailable())
                    .getOrElse(false));
  }
}
