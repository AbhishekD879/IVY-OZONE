package com.coral.oxygen.middleware.ms.quickbet.converter;

import static com.coral.oxygen.middleware.ms.quickbet.converter.PlaceBetRequestConverter.*;
import static com.coral.oxygen.middleware.ms.quickbet.impl.RegularSelectionOperationHandler.SINGLE_BET_TYPE;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.mockito.MockitoAnnotations.initMocks;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UIBet;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UILeg;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Part;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PlaceBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PrevTerm;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuild;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetCombination;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.EnhancedOdd;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.EnhancedOddContainer;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.EnhancedPrice;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.FreebetToken;
import com.google.common.collect.ImmutableList;
import io.vavr.collection.List;
import io.vavr.control.Option;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;

// todo add more tests, verifying at least basic conversion
public class PlaceBetRequestConverterTest {

  private static final String CHANNEL = "channel";
  private static final String CLIENT_USER_AGENT = "client_user_agent";
  private static final String USD_CURRENCY = "USD";
  private static final String DOUBLE_BET_TYPE = "DBL";
  private static final String OUTCOME_ID = "1111111";
  private static final String PRICE_TYPE_LIVE = "L";

  private static final String ONE_USD_FREEBET_TOKEN_ID = "123";
  private static final String FIVE_USD_FREEBET_TOKEN_ID = "456";
  private static final String TEN_USD_FREEBET_TOKEN_ID = "789";
  private static final String ODDS_BOOST_TOKEN_ID = "012";

  private static final String ODDS_BOOST_OUTCOME_ID = "222222333";
  private static final String ODDS_BOOST_OUTCOME_ID_2 = "333322222";

  @Mock private Session session;

  private PlaceBetRequestConverter placeBetRequestConverter;

  @BeforeEach
  public void setUp() {
    initMocks(this);
    placeBetRequestConverter = new PlaceBetRequestConverter();
  }

  @Test
  public void shouldConvertBasic() {
    // GIVEN
    UIPlaceBetRequest uiPlaceBetRequest = uiPlaceBetRequest(List.empty());
    // WHEN
    PlaceBetDto result = placeBetRequestConverter.convert(session, uiPlaceBetRequest);
    // THEN
    assertThat(result.getClientUserAgent()).isEqualTo(CLIENT_USER_AGENT);
    assertThat(result.getChannel()).isEqualTo(CHANNEL);
  }

  @Test
  public void shouldBoostSingle() {
    // GIVEN
    int regularNum = 5;
    int regularDen = 3;
    int boostedNum = 2;
    int boostedDen = 1;
    String stakePerLine = "1.00";
    UILeg leg = leg(regularNum, regularDen, ODDS_BOOST_OUTCOME_ID, PRICE_TYPE_LIVE);
    UIBet bet = singleWithOddsBoost(stakePerLine, List.of(leg));

    EnhancedOdd enhancedOdd =
        getEnhancedOddsForOutcome(
            ODDS_BOOST_OUTCOME_ID, boostedNum, boostedDen, ODDS_BOOST_TOKEN_ID);
    BetBuild betBuild = createBetBuildWithEnhancedOdds(bet, SINGLE_BET_TYPE, "1", enhancedOdd);
    BetBuildResponseModel responseModel = betBuildResponseModel(betBuild);

    Event event = event(false);

    when(session.getBetBuildResponseModel()).thenReturn(responseModel);
    when(session.getOutcomeEvent(ODDS_BOOST_OUTCOME_ID)).thenReturn(Option.of(event));
    // WHEN
    PlaceBetDto result = placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(bet)));
    // THEN
    assertThat(result.getBet()).hasSize(1);

    Bet placedBet = extractBet(result, bet.getBetNo());
    assertThat(placedBet.getBetType()).isEqualTo(SINGLE_BET_TYPE);
    assertThat(placedBet.getFreebetTokenId()).contains(ODDS_BOOST_TOKEN_ID);
    assertThat(String.valueOf(placedBet.getLeg().size())).hasSize(1);
    assertThat(placedBet.getStakePerLine()).isEqualTo(stakePerLine);
    assertThat(placedBet.getPrevTerms().getPrevTerm()).hasSize(1);

    Part placedPart = extractPart(placedBet, ODDS_BOOST_OUTCOME_ID);
    assertThat(placedPart.getPriceNum()).isEqualTo(boostedNum);
    assertThat(placedPart.getPriceDen()).isEqualTo(boostedDen);

    PrevTerm prevTerm = placedBet.getPrevTerms().getPrevTerm().stream().findFirst().get();
    assertThat(prevTerm.getReasonCode()).isEqualTo(ODDS_BOOST_REASON_CODE);

    Part previousPart = extractPreviousPart(placedBet, ODDS_BOOST_OUTCOME_ID);
    assertThat(previousPart.getPriceDen()).isEqualTo(regularDen);
    assertThat(previousPart.getPriceNum()).isEqualTo(regularNum);
  }

  @Test
  public void shouldNotBoostOddsWhenAvailableButNotRequested() {
    // GIVEN
    int regularNum = 5;
    int regularDen = 3;
    int boostedNum = 2;
    int boostedDen = 1;
    String stakePerLine = "12.3";
    UILeg leg = leg(regularNum, regularDen, ODDS_BOOST_OUTCOME_ID, PRICE_TYPE_LIVE);
    UIBet bet = singleBet(stakePerLine, List.of(leg));
    EnhancedOdd enhancedOdd =
        getEnhancedOddsForOutcome(
            ODDS_BOOST_OUTCOME_ID, boostedNum, boostedDen, ODDS_BOOST_TOKEN_ID);
    BetBuild betBuild = createBetBuildWithEnhancedOdds(bet, SINGLE_BET_TYPE, "1", enhancedOdd);
    BetBuildResponseModel responseModel = betBuildResponseModel(betBuild);

    Event event = event(false);

    when(session.getOutcomeEvent(ODDS_BOOST_OUTCOME_ID)).thenReturn(Option.of(event));
    when(session.getBetBuildResponseModel()).thenReturn(responseModel);
    // WHEN
    PlaceBetDto result = placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(bet)));
    // THEN
    assertThat(result.getBet()).hasSize(1);

    Bet placedBet = extractBet(result, bet.getBetNo());
    assertThat(placedBet.getBetType()).isEqualTo(SINGLE_BET_TYPE);
    assertThat(placedBet.getFreebetTokenId()).isNullOrEmpty();
    assertThat(String.valueOf(placedBet.getLeg().size())).hasSize(1);
    assertThat(placedBet.getStakePerLine()).isEqualTo(stakePerLine);
    assertThat(placedBet.getPrevTerms()).isNull();

    Part placedPart = extractPart(placedBet, ODDS_BOOST_OUTCOME_ID);
    assertThat(placedPart.getPriceNum()).isEqualTo(regularNum);
    assertThat(placedPart.getPriceDen()).isEqualTo(regularDen);
  }

  @Test
  public void shouldBoostDoubleBets() {
    // GIVEN
    int regularNum = 5;
    int regularDen = 3;
    int boostedNum = 2;
    int boostedDen = 1;
    int boostedNum2 = 7;
    int boostedDen2 = 4;
    String stakePerLine = "1.23";
    UILeg leg1 = leg(regularNum, regularDen, ODDS_BOOST_OUTCOME_ID, PRICE_TYPE_LIVE);
    UILeg leg2 = leg(regularNum, regularDen, ODDS_BOOST_OUTCOME_ID_2, PRICE_TYPE_LIVE);
    UIBet doubleBet = doubleBetWithOddsBoost(stakePerLine, List.of(leg1, leg2));
    EnhancedOdd enhancedOdd1 =
        getEnhancedOddsForOutcome(
            ODDS_BOOST_OUTCOME_ID, boostedNum, boostedDen, ODDS_BOOST_TOKEN_ID);
    EnhancedOdd enhancedOdd2 =
        getEnhancedOddsForOutcome(
            ODDS_BOOST_OUTCOME_ID_2, boostedNum2, boostedDen2, ODDS_BOOST_TOKEN_ID);
    BetBuild betBuild =
        createBetBuildWithEnhancedOdds(doubleBet, DOUBLE_BET_TYPE, "2", enhancedOdd1, enhancedOdd2);
    BetBuildResponseModel responseModel = betBuildResponseModel(betBuild);

    Event event1 = event(false);
    Event event2 = event(false);

    when(session.getOutcomeEvent(ODDS_BOOST_OUTCOME_ID)).thenReturn(Option.of(event1));
    when(session.getOutcomeEvent(ODDS_BOOST_OUTCOME_ID_2)).thenReturn(Option.of(event2));
    when(session.getBetBuildResponseModel()).thenReturn(responseModel);
    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(doubleBet)));
    // THEN
    assertThat(result.getBet()).hasSize(1);

    Bet placedBet = extractBet(result, betBuild.getBetNo());
    assertThat(placedBet.getBetType()).isEqualTo(DOUBLE_BET_TYPE);
    assertThat(placedBet.getFreebetTokenId()).contains(ODDS_BOOST_TOKEN_ID);
    assertThat(placedBet.getLeg()).hasSize(2);
    assertThat(placedBet.getStakePerLine()).isEqualTo(stakePerLine);
    assertThat(placedBet.getPrevTerms().getPrevTerm()).hasSize(1);

    Part placedPart1 = extractPart(placedBet, ODDS_BOOST_OUTCOME_ID);
    assertThat(placedPart1.getPriceNum()).isEqualTo(boostedNum);
    assertThat(placedPart1.getPriceDen()).isEqualTo(boostedDen);

    Part placedPart2 = extractPart(placedBet, ODDS_BOOST_OUTCOME_ID_2);
    assertThat(placedPart2.getPriceNum()).isEqualTo(boostedNum2);
    assertThat(placedPart2.getPriceDen()).isEqualTo(boostedDen2);

    PrevTerm prevTerm = placedBet.getPrevTerms().getPrevTerm().get(0);
    assertThat(prevTerm.getReasonCode()).isEqualTo(ODDS_BOOST_REASON_CODE);

    Part previousPart1 = extractPreviousPart(placedBet, ODDS_BOOST_OUTCOME_ID);
    assertThat(previousPart1.getPriceDen()).isEqualTo(regularDen);
    assertThat(previousPart1.getPriceNum()).isEqualTo(regularNum);

    Part previousPart2 = extractPreviousPart(placedBet, ODDS_BOOST_OUTCOME_ID_2);
    assertThat(previousPart2.getPriceDen()).isEqualTo(regularDen);
    assertThat(previousPart2.getPriceNum()).isEqualTo(regularNum);
  }

  @Test
  public void shouldIncreaseSingleBetStakePerLineByValueOfTwoRequestedFreebetTokens() {
    // GIVEN
    UIBet singleUIBet = singleBetWithOneAndTenDollarFreebetTokens("1.43");
    BetBuild betBuildForSingleUIBet = betBuild(singleUIBet, SINGLE_BET_TYPE, "1");
    BetBuildResponseModel singleBetBuildResponseModel =
        betBuildResponseModel(betBuildForSingleUIBet);
    String expectedStakePerLine = "12.43"; // bet stake + freebet for 1 USD + freebet for 10 USD
    when(session.getBetBuildResponseModel()).thenReturn(singleBetBuildResponseModel);

    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(singleUIBet)));

    // THEN
    assertThat(result.getBet()).hasSize(1);
    Bet placedBet = extractBet(result, singleUIBet.getBetNo());

    assertThat(placedBet.getBetType()).isEqualTo(SINGLE_BET_TYPE);
    assertThat(placedBet.getStakePerLine()).isEqualTo(expectedStakePerLine);
  }

  @Test
  public void shouldIncreaseDoubleAndSingleBetsStakePerLineByValueOfRequestedFreebetTokens() {
    // GIVEN
    UIBet singleUIBetWithTwoTokens = singleBetWithOneAndTenDollarFreebetTokens("1.43");
    UIBet doubleUIBetWithOneToken = doubleBetWithFiveAndTenDollarFreebetTokens("2.43");

    BetBuild betBuildForSingleBet = betBuild(singleUIBetWithTwoTokens, SINGLE_BET_TYPE, "1");
    BetBuild betBuildForDoubleBet = betBuild(doubleUIBetWithOneToken, DOUBLE_BET_TYPE, "3");

    BetBuildResponseModel betBuildResponseModel =
        betBuildResponseModel(betBuildForSingleBet, betBuildForDoubleBet);

    String expectedStakeForSingleBet =
        "12.43"; // stake for single bet + two freebet tokens: 10 USD + 1 USD
    String expectedStakeForDoubleBet =
        "5.76"; // stake for single bet + one freebet token: 10 USD / betNoOfLines(3)

    when(session.getBetBuildResponseModel()).thenReturn(betBuildResponseModel);

    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(
            session, uiPlaceBetRequest(List.of(singleUIBetWithTwoTokens, doubleUIBetWithOneToken)));

    // THEN
    assertThat(result.getBet()).hasSize(2);

    Bet placedSingleBet = extractBet(result, singleUIBetWithTwoTokens.getBetNo());
    Bet placedDoubleBet = extractBet(result, doubleUIBetWithOneToken.getBetNo());

    assertThat(placedSingleBet.getBetType()).isEqualTo(SINGLE_BET_TYPE);
    assertThat(placedSingleBet.getStakePerLine()).isEqualTo(expectedStakeForSingleBet);

    assertThat(placedDoubleBet.getBetType()).isEqualTo(DOUBLE_BET_TYPE);
    assertThat(placedDoubleBet.getStakePerLine()).isEqualTo(expectedStakeForDoubleBet);
  }

  @Test
  public void shouldNotIncreaseStakePerLineWhenFreebetsAreAvailableButNotRequested() {
    // GIVEN
    String stakePerLine = "3.43"; // this is also expectedStake as no tokens are added for the bet
    UIBet doubleBetWithoutToken = doubleBetWithoutFreebetTokens(stakePerLine);
    BetBuild betBuildFordoubleBetWithoutToken =
        betBuild(doubleBetWithoutToken, DOUBLE_BET_TYPE, "3");
    BetBuildResponseModel betBuildResponseModel =
        betBuildResponseModel(betBuildFordoubleBetWithoutToken);

    when(session.getBetBuildResponseModel()).thenReturn(betBuildResponseModel);

    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(
            session, uiPlaceBetRequest(List.of(doubleBetWithoutToken)));

    // THEN
    assertThat(result.getBet()).hasSize(1);

    Bet placedBet = extractBet(result, doubleBetWithoutToken.getBetNo());

    assertThat(placedBet.getBetType()).isEqualTo(DOUBLE_BET_TYPE);
    assertThat(placedBet.getStakePerLine()).isEqualTo(stakePerLine);
  }

  @Test
  public void shouldSetPriceTypeAsGuaranteedWhenGpIsAvailable() {
    // GIVEN
    String originalPriceType = PRICE_TYPE_LIVE;
    Event eventWithGpAvailable = event(true);
    UILeg uiLeg =
        UILeg.builder()
            .priceNum(1)
            .priceDen(2)
            .outcomeIds(List.of(OUTCOME_ID))
            .priceType(originalPriceType)
            .selectionType(Option.none())
            .build();
    UIBet singleBet = singleBet("11", List.of(uiLeg));

    BetBuild betBuildForSingleBet = betBuild(singleBet, SINGLE_BET_TYPE, "1");
    BetBuildResponseModel betBuildResponseModel = betBuildResponseModel(betBuildForSingleBet);

    when(session.getBetBuildResponseModel()).thenReturn(betBuildResponseModel);

    when(session.getOutcomeEvent(OUTCOME_ID)).thenReturn(Option.of(eventWithGpAvailable));

    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(singleBet)));

    // THEN
    Bet placedBet = extractBet(result, singleBet.getBetNo());
    Part part = extractPart(placedBet, OUTCOME_ID);

    assertThat(part.getPriceType()).isEqualTo(PRICE_TYPE_GUARANTEED);
  }

  @Test
  public void shouldNotSetPriceTypeAsGuaranteedWhenGpIsNotAvailable() {
    // GIVEN
    String originalPriceType = PRICE_TYPE_LIVE;
    Event eventWithoutGpAvailable = event(false);
    UILeg uiLeg = leg(1, 2, OUTCOME_ID, originalPriceType);
    UIBet singleBet = singleBet("11", List.of(uiLeg));

    BetBuild betBuildForSingleBet = betBuild(singleBet, SINGLE_BET_TYPE, "1");
    BetBuildResponseModel betBuildResponseModel = betBuildResponseModel(betBuildForSingleBet);

    when(session.getBetBuildResponseModel()).thenReturn(betBuildResponseModel);

    when(session.getOutcomeEvent(OUTCOME_ID)).thenReturn(Option.of(eventWithoutGpAvailable));

    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(singleBet)));

    // THEN
    Bet placedBet = extractBet(result, singleBet.getBetNo());
    Part part = extractPart(placedBet, OUTCOME_ID);

    assertThat(part.getPriceType()).isEqualTo(originalPriceType);
  }

  @Test
  public void shouldSetPriceTypeAsGuaranteedForFirstLegAndNotForSecondForDoubleBet() {
    // GIVEN
    String firstLegOriginalPriceType = PRICE_TYPE_LIVE;
    String outcomeIdSecondLeg = "2222";
    Event eventWithoutGpAvailable = event(false);
    Event eventWithGpAvailable = event(true);
    UILeg firstUILeg = leg(1, 2, OUTCOME_ID, firstLegOriginalPriceType);
    UILeg secondUILeg = leg(2, 3, outcomeIdSecondLeg, PRICE_TYPE_LIVE);
    UIBet doubleBet = doubleBet("11", List.of(firstUILeg, secondUILeg));

    BetBuild betBuildForSingleBet = betBuild(doubleBet, DOUBLE_BET_TYPE, "1");
    BetBuildResponseModel betBuildResponseModel = betBuildResponseModel(betBuildForSingleBet);

    when(session.getBetBuildResponseModel()).thenReturn(betBuildResponseModel);
    when(session.getOutcomeEvent(OUTCOME_ID)).thenReturn(Option.of(eventWithoutGpAvailable));
    when(session.getOutcomeEvent(outcomeIdSecondLeg)).thenReturn(Option.of(eventWithGpAvailable));

    // WHEN
    PlaceBetDto result =
        placeBetRequestConverter.convert(session, uiPlaceBetRequest(List.of(doubleBet)));

    // THEN
    Bet placedBet = extractBet(result, doubleBet.getBetNo());
    Part firstLegPart = extractPart(placedBet, OUTCOME_ID);
    Part secondLegPart = extractPart(placedBet, outcomeIdSecondLeg);

    assertThat(firstLegPart.getPriceType()).isEqualTo(firstLegOriginalPriceType);
    assertThat(secondLegPart.getPriceType()).isEqualTo(PRICE_TYPE_GUARANTEED);
  }

  private Part extractPart(Bet placedBet, String outcomeId) {
    return placedBet.getLeg().stream()
        .flatMap(leg -> leg.getPart().stream())
        .filter(part -> part.getOutcome().equals(outcomeId))
        .findFirst()
        .orElseThrow(
            () ->
                new IllegalArgumentException(
                    "Placed bet does not contain leg part associated with outcome: " + outcomeId));
  }

  private Part extractPreviousPart(Bet placedBet, String outcomeId) {
    return placedBet.getPrevTerms().getPrevTerm().stream()
        .flatMap(prevTerm -> prevTerm.getLeg().stream())
        .flatMap(leg -> leg.getPart().stream())
        .filter(part -> part.getOutcome().equals(outcomeId))
        .findFirst()
        .orElseThrow(
            () ->
                new IllegalArgumentException(
                    "Placed bet does not contain previous term leg part associated with outcome: "
                        + outcomeId));
  }

  private Event event(boolean isGpAvailable) {
    Market market = new Market();
    market.setIsGpAvailable(isGpAvailable);
    Event event = mock(Event.class);
    when(event.getMarkets()).thenReturn(ImmutableList.of(market));

    return event;
  }

  private BetBuildResponseModel betBuildResponseModel(BetBuild... betBuilds) {

    BetBuildResponseModel betBuildResponseModel = new BetBuildResponseModel();
    Collections.addAll(betBuildResponseModel.getBetBuild(), betBuilds);

    return betBuildResponseModel;
  }

  private BetBuild createBetBuildWithEnhancedOdds(
      UIBet uiBet, String betType, String betNoOfLines, EnhancedOdd... enhancedOdds) {
    BetBuild betBuild = betBuild(uiBet, betType, betNoOfLines);
    EnhancedOddContainer oddsContainer = new EnhancedOddContainer();
    Collections.addAll(oddsContainer.getEnhancedOdd(), enhancedOdds);
    betBuild.setEnhancedOdds(oddsContainer);
    betBuild.getFreebetToken().add(getOddsBoostToken());
    return betBuild;
  }

  private BetBuild betBuild(UIBet uiBet, String betType, String betNoOfLines) {
    BetBuild betBuild = new BetBuild();
    betBuild.setBetNo(uiBet.getBetNo());
    BetCombination betCombination = new BetCombination();
    betCombination.setBetType(betType);
    betCombination.setBetNoOfLines(betNoOfLines);
    betBuild.getBetCombination().add(betCombination);
    betBuild.getFreebetToken().addAll(getFreebetTokens().asJava());

    return betBuild;
  }

  private UILeg leg(int priceNum, int priceDen, String outcomeId, String priceType) {
    return UILeg.builder()
        .outcomeIds(List.of(outcomeId))
        .priceNum(priceNum)
        .priceDen(priceDen)
        .priceType(priceType)
        .selectionType(Option.none())
        .build();
  }

  private UIBet singleWithOddsBoost(String stakePerLine, List<UILeg> legs) {
    return UIBet.builder()
        .betNo("1")
        .winType("W")
        .freebetTokenIds(List.of(ODDS_BOOST_TOKEN_ID))
        .betType(SINGLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .legs(legs)
        .build();
  }

  private UIBet doubleBetWithOddsBoost(String stakePerLine, List<UILeg> legs) {
    return UIBet.builder()
        .betNo("2")
        .winType("W")
        .freebetTokenIds(List.of(ODDS_BOOST_TOKEN_ID))
        .betType(DOUBLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .legs(legs)
        .build();
  }

  private UIBet singleBetWithOneAndTenDollarFreebetTokens(String stakePerLine) {
    return UIBet.builder()
        .betNo("1")
        .winType("W")
        .freebetTokenIds(List.of(ONE_USD_FREEBET_TOKEN_ID, TEN_USD_FREEBET_TOKEN_ID))
        .betType(SINGLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .build();
  }

  private UIBet doubleBetWithoutFreebetTokens(String stakePerLine) {
    return UIBet.builder()
        .betNo("2")
        .winType("W")
        .freebetTokenIds(null)
        .betType(DOUBLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .build();
  }

  private UIBet doubleBetWithFiveAndTenDollarFreebetTokens(String stakePerLine) {
    return UIBet.builder()
        .betNo("3")
        .winType("W")
        .freebetTokenIds(List.of(FIVE_USD_FREEBET_TOKEN_ID, TEN_USD_FREEBET_TOKEN_ID))
        .betType(DOUBLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .build();
  }

  private UIBet singleBet(String stakePerLine, List<UILeg> legs) {
    return UIBet.builder()
        .betNo("4")
        .winType("W")
        .betType(SINGLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .legs(legs)
        .build();
  }

  private UIBet doubleBet(String stakePerLine, List<UILeg> legs) {
    return UIBet.builder()
        .betNo("5")
        .winType("W")
        .betType(DOUBLE_BET_TYPE)
        .stakePerLine(stakePerLine)
        .legs(legs)
        .build();
  }

  private Bet extractBet(PlaceBetDto result, String betNo) {
    return result.getBet().stream()
        .filter(bet -> bet.getBetNo().equals(betNo))
        .findFirst()
        .orElseThrow(
            () -> new IllegalArgumentException("PlaceBetDto does not contain betNo: " + betNo));
  }

  private UIPlaceBetRequest uiPlaceBetRequest(List<UIBet> uiBets) {
    return new UIPlaceBetRequest(CHANNEL, CLIENT_USER_AGENT, USD_CURRENCY, uiBets);
  }

  private List<FreebetToken> getFreebetTokens() {

    FreebetToken oneUSDFreebetToken = new FreebetToken();
    oneUSDFreebetToken.setFreebetTokenId(ONE_USD_FREEBET_TOKEN_ID);
    oneUSDFreebetToken.setFreebetTokenValue("1");
    oneUSDFreebetToken.setCurrency(USD_CURRENCY);

    FreebetToken fiveUSDFreebetToken = new FreebetToken();
    fiveUSDFreebetToken.setFreebetTokenId(FIVE_USD_FREEBET_TOKEN_ID);
    fiveUSDFreebetToken.setFreebetTokenValue("5");
    fiveUSDFreebetToken.setCurrency(USD_CURRENCY);

    FreebetToken tenUSDFreebetToken = new FreebetToken();
    fiveUSDFreebetToken.setFreebetTokenId(TEN_USD_FREEBET_TOKEN_ID);
    fiveUSDFreebetToken.setFreebetTokenValue("10");
    fiveUSDFreebetToken.setCurrency(USD_CURRENCY);

    return List.of(oneUSDFreebetToken, fiveUSDFreebetToken, tenUSDFreebetToken);
  }

  private FreebetToken getOddsBoostToken() {
    FreebetToken oddsBoostToken = new FreebetToken();
    oddsBoostToken.setFreebetTokenId(ODDS_BOOST_TOKEN_ID);
    oddsBoostToken.setFreebetTokenType(BETBOOST_FREEBET_TOKEN_TYPE);
    return oddsBoostToken;
  }

  private EnhancedOdd getEnhancedOddsForOutcome(
      String outcomeId, int priceNum, int priceDen, String tokenId) {
    EnhancedPrice enhancedPrice = new EnhancedPrice();
    enhancedPrice.setPriceNum(Integer.toString(priceNum));
    enhancedPrice.setPriceDen(Integer.toString(priceDen));
    enhancedPrice.setTokenId(tokenId);
    EnhancedOdd enhancedOdd = new EnhancedOdd();
    enhancedOdd.setOutcome(outcomeId);
    enhancedOdd.setEnhancedPrice(enhancedPrice);
    return enhancedOdd;
  }
}
