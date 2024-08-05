package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.impl.RegularSelectionOperationHandler.SINGLE_BET_TYPE;
import static com.coral.oxygen.middleware.ms.quickbet.utils.BetBuildUtils.outcomeToEvent;
import static com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils.getResourceByPath;
import static java.util.Collections.singleton;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BetBuildResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.BetBuildDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Part;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PlaceBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BaseBetError;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuild;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetCombination;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetFailure;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetFailureDetail;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.OutcomeDetails;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
public class MultibetsIT {

  private static final String PLACE_BET_JSON_RESOURCES_PATH = "integration/placeBet/";
  private static final String DOUBLE_BET_TYPE = "DBL";
  private static final String ADD_SELECTION_REQUEST_JSON =
      PLACE_BET_JSON_RESOURCES_PATH + "addSelectionRequest.json";
  private static final String ADD_OTHER_SELECTION_REQUEST_JSON =
      PLACE_BET_JSON_RESOURCES_PATH + "addOtherSelectionRequest.json";
  private static final String TWO_SINGLE_PLACE_BET_REQUEST_JSON =
      PLACE_BET_JSON_RESOURCES_PATH + "twoSinglePlaceBetRequest.json";

  private static final String[] SELECTED_OUTCOMES = new String[] {"100000001", "100000002"};
  private static final String ERROR = "ERROR";
  public static final String TOKEN =
      "6e650167ccd74b9e8232f8415559b6a498781c5623b539000cb4ed99badffb82";

  @Autowired private WebSocketTestClient client;

  @Captor private ArgumentCaptor<String> channelsCaptor;

  @MockBean private BettingService bettingService;

  @MockBean private LiveServService liveServService;

  @MockBean private SiteServerService siteServerService;

  @AfterEach
  public void cleanUp() {
    client.clearReceivedData();
    client.emitWithWaitForResponse(
        Messages.CLEAR_SELECTION_REQUEST_CODE,
        null,
        Messages.CLEAR_SELECTION_RESPONSE_CODE,
        Object.class);
  }

  @Test
  public void shouldBuildBetAfterAddingOneSelection() {
    // GIVEN
    String outcomeId = "12345678";
    AddSelectionRequest request = addSelectionRequest(outcomeId);

    GeneralResponse<BetBuildResponseModel> bppResponse = createResponseWithoutErrors(outcomeId);
    when(bettingService.buildBetV2(isNull(), any(BetBuildDto.class))).thenReturn(bppResponse);

    when(siteServerService.getEventsForOutcomeIds(List.of(outcomeId)))
        .thenReturn(outcomeToEvent(outcomeId));

    // WHEN
    BetBuildResponse response =
        client.emitWithWaitForResponse(
            Messages.ADD_SELECTION, request, Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);

    // THEN
    assertThat(response.getBetBuildResponseModel())
        .isEqualToComparingFieldByFieldRecursively(bppResponse.getBody());
    verify(liveServService, times(5)).subscribe(channelsCaptor.capture());
    assertThat(channelsCaptor.getAllValues())
        .containsExactlyInAnyOrder(
            "sEVENT0000000001",
            "sCLOCK0000000001",
            "sSCBRD0000000001",
            "sEVMKT0000000002",
            "sSELCN0012345678");
  }

  private GeneralResponse<BetBuildResponseModel> createResponseWithoutErrors(String... outcomeIds) {
    BetBuildResponseModel betBuild = new BetBuildResponseModel();
    List.of(outcomeIds)
        .forEach(outcomeId -> betBuild.getOutcomeDetails().add(createOutcomeDetails(outcomeId)));

    return new GeneralResponse<>(betBuild, null);
  }

  private BetBuild createBetBuildWithBetCombination(
      String betNo, String betType, String betNoOfLine) {
    BetBuild betBuild = new BetBuild();
    betBuild.setBetNo(betNo);

    BetCombination betCombination = new BetCombination();
    betCombination.setBetType(betType);
    betCombination.setBetNoOfLines(betNoOfLine);

    betBuild.getBetCombination().add(betCombination);

    return betBuild;
  }

  @Test
  public void shouldRetryBuildBetWithoutFailedBets() {
    // GIVEN
    String activeOutcomeId = "11111111";
    String suspendedOutcomeId = "99999999";
    AddSelectionRequest activeOutcomeRequest = addSelectionRequest(activeOutcomeId);
    AddSelectionRequest suspendedOutcomeRequest = addSelectionRequest(suspendedOutcomeId);

    when(bettingService.buildBetV2(any(), any(BetBuildDto.class)))
        .thenReturn(
            createResponseWithoutErrors(
                suspendedOutcomeId), // at first we add one selection (that is active at the time)
            createResponseWithErrors(
                suspendedOutcomeId), // when we add second selection, the first one gets suspended
            // and causes buildBet to fail
            createResponseWithoutErrors(activeOutcomeId) // we retry with only active selection
            );

    when(siteServerService.getEventsForOutcomeIds(any()))
        .thenReturn(outcomeToEvent(activeOutcomeId, suspendedOutcomeId));

    client.login(TOKEN);

    // WHEN
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        suspendedOutcomeRequest,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    BetBuildResponse response =
        client.emitWithWaitForResponse(
            Messages.ADD_SELECTION,
            activeOutcomeRequest,
            Messages.BUILD_BET_RESPONSE,
            BetBuildResponse.class);

    // THEN
    ArgumentCaptor<BetBuildDto> betBuildDtoCaptor = ArgumentCaptor.forClass(BetBuildDto.class);
    assertThat(response.getFailedOutcomeIds()).contains(suspendedOutcomeId);
    verify(bettingService, times(3)).buildBetV2(eq(TOKEN), betBuildDtoCaptor.capture());
    assertThat(betBuildDtoCaptor.getAllValues().get(0).getOutcomeGroup().size()).isEqualTo(1);
    assertThat(betBuildDtoCaptor.getAllValues().get(1).getOutcomeGroup().size()).isEqualTo(3);
    assertThat(betBuildDtoCaptor.getAllValues().get(2).getOutcomeGroup().size()).isEqualTo(1);
  }

  private AddSelectionRequest addSelectionRequest(String outcomeId) {
    return new AddSelectionRequest(outcomeId);
  }

  private GeneralResponse<BetBuildResponseModel> createResponseWithoutErrors(String outcomeId) {
    BetBuildResponseModel betBuild = new BetBuildResponseModel();
    betBuild.getOutcomeDetails().add(createOutcomeDetails(outcomeId));

    return new GeneralResponse<>(betBuild, null);
  }

  private GeneralResponse<BetBuildResponseModel> createResponseWithErrors(
      String... suspendedOutcomeIds) {
    BetBuildResponseModel betBuildResponse = new BetBuildResponseModel();

    BetFailure anotherBetFailed = new BetFailure();
    anotherBetFailed.getBetError().add(new BaseBetError());
    betBuildResponse.getBetFailure().add(anotherBetFailed);

    List.of(suspendedOutcomeIds)
        .map(this::getBetFailure)
        .forEach(betBuildResponse.getBetFailure()::add);

    return new GeneralResponse<>(betBuildResponse, null);
  }

  private BetFailure getBetFailure(String suspendedOutcomeId) {
    BetFailure betOverrideFound = new BetFailure();
    BaseBetError overrideBetError = new BaseBetError();
    BetFailureDetail betFailureDetail = new BetFailureDetail();
    betFailureDetail.setOutcomeId(suspendedOutcomeId);
    overrideBetError.setBetFailureDetail(betFailureDetail);
    betOverrideFound.getBetError().add(overrideBetError);
    return betOverrideFound;
  }

  @Test
  public void shouldNotRetryAfterLastSelectionFails() {
    // GIVEN
    String firstSuspendedOutcomeId = "12345678";
    String secondSuspendedOutcomeId = "550543454";

    when(bettingService.buildBetV2(any(), any()))
        .thenReturn(
            createResponseWithErrors(firstSuspendedOutcomeId),
            createResponseWithErrors(firstSuspendedOutcomeId, secondSuspendedOutcomeId));

    when(siteServerService.getEventsForOutcomeIds(any()))
        .thenReturn(outcomeToEvent(firstSuspendedOutcomeId, secondSuspendedOutcomeId));

    // WHEN
    BetBuildResponse resp1 =
        client.emitWithWaitForResponse(
            Messages.ADD_SELECTION,
            addSelectionRequest(firstSuspendedOutcomeId),
            Messages.BUILD_BET_RESPONSE,
            BetBuildResponse.class);
    BetBuildResponse resp2 =
        client.emitWithWaitForResponse(
            Messages.ADD_SELECTION,
            addSelectionRequest(secondSuspendedOutcomeId),
            Messages.BUILD_BET_RESPONSE,
            BetBuildResponse.class);

    // THEN
    verify(bettingService, times(2)).buildBetV2(any(), any());
    assertThat(resp1.getFailedOutcomeIds()).contains(firstSuspendedOutcomeId);
    assertThat(resp2.getFailedOutcomeIds()).contains(secondSuspendedOutcomeId);
  }

  @Test
  public void shouldNotCallBppWhenNoSelection() {
    // GIVEN
    String emptyAddSelectionRequest = "{\"token\": \"someToken\"}";

    // WHEN
    client.emit(Messages.ADD_SELECTION, emptyAddSelectionRequest);
    client.wait(Messages.SELECTION_EMPTY_OR_ALREADY_ADDED);

    // THEN
    verify(bettingService, never()).buildBetV2(any(), any());
  }

  private OutcomeDetails createOutcomeDetails(String outcomeId) {
    OutcomeDetails outcomeDetails = new OutcomeDetails();
    outcomeDetails.setId(outcomeId);
    outcomeDetails.setMarketId("2");
    outcomeDetails.setEventId("1");
    return outcomeDetails;
  }

  @Test
  public void shouldNotPlaceBetAfterBuildingBetWithTwoSelections() {
    // given
    String addSelRequestBody = getResourceByPath(ADD_SELECTION_REQUEST_JSON);
    String addOtherSelRequestBody = getResourceByPath(ADD_OTHER_SELECTION_REQUEST_JSON);
    String placeBetRequestBody = getResourceByPath(TWO_SINGLE_PLACE_BET_REQUEST_JSON);

    GeneralResponse<BetBuildResponseModel> bppBuildBetResponse =
        buildBetBuildResponseModelWithTwoBuildBet(SELECTED_OUTCOMES, false);

    GeneralResponse<RespBetPlace> betPlaceResponseWithError =
        new GeneralResponse<>(null, errorBody());

    when(bettingService.buildBetV2(any(), any())).thenReturn(bppBuildBetResponse);
    when(bettingService.placeBetV2(any(), any(PlaceBetDto.class)))
        .thenReturn(betPlaceResponseWithError);

    when(siteServerService.getEventsForOutcomeIds(any()))
        .thenReturn(outcomeToEvent(SELECTED_OUTCOMES));

    client.login(TOKEN);

    // when
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        addSelRequestBody,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        addOtherSelRequestBody,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    ErrorBody error =
        client.emitWithWaitForResponse(
            Messages.PLACE_BET,
            placeBetRequestBody,
            Messages.PLACE_BET_ERROR_RESPONSE_CODE,
            ErrorBody.class);

    // then
    verify(bettingService).placeBetV2(anyString(), any(PlaceBetDto.class));
    assertThat(error.getError()).isEqualTo(ERROR);
    assertThat(error.getStatus()).isEqualTo(ERROR);
  }

  private ErrorBody errorBody() {
    ErrorBody errorBody = new ErrorBody();
    errorBody.setStatus(ERROR);
    errorBody.setError(ERROR);
    return errorBody;
  }

  @Test
  public void shouldPlaceBetAfterBuildingBetWithTwoSingleAndDoubleSelections() {
    // given
    String addSelRequestBody = getResourceByPath(ADD_SELECTION_REQUEST_JSON);
    String addOtherSelRequestBody = getResourceByPath(ADD_OTHER_SELECTION_REQUEST_JSON);
    String placeBetRequestBody =
        getResourceByPath(PLACE_BET_JSON_RESOURCES_PATH + "twoSingleOneDoublePlaceBetRequest.json");

    GeneralResponse<BetBuildResponseModel> bppBuildBetResponse1 =
        buildBetBuildResponseModelWithTwoBuildBet(new String[] {"100000002"}, false);
    GeneralResponse<BetBuildResponseModel> bppBuildBetResponse2 =
        buildBetBuildResponseModelWithTwoBuildBet(SELECTED_OUTCOMES, true);

    GeneralResponse<RespBetPlace> betPlaceResponseWoError =
        new GeneralResponse<>(new RespBetPlace(), null);

    when(bettingService.buildBetV2(any(), any()))
        .thenReturn(bppBuildBetResponse1, bppBuildBetResponse2);
    when(bettingService.placeBetV2(any(), any(PlaceBetDto.class)))
        .thenReturn(betPlaceResponseWoError);

    when(siteServerService.getEventsForOutcomeIds(any()))
        .thenReturn(outcomeToEvent("100000002"), outcomeToEvent(SELECTED_OUTCOMES));

    client.login(TOKEN);

    // when
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        addSelRequestBody,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        addOtherSelRequestBody,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    client.emitWithWaitForResponse(
        Messages.PLACE_BET,
        placeBetRequestBody,
        Messages.PLACE_BET_RESPONSE_CODE,
        RespBetPlace.class);

    // then
    ArgumentCaptor<PlaceBetDto> reqCaptor = ArgumentCaptor.forClass(PlaceBetDto.class);
    verify(bettingService).placeBetV2(anyString(), reqCaptor.capture());

    PlaceBetDto placeBetDto = reqCaptor.getValue();
    assertThat(placeBetDto.getBet()).hasSize(3);
    assertThat(placeBetDto.getBet())
        .extracting(Bet::getBetType)
        .containsExactlyInAnyOrder(SINGLE_BET_TYPE, SINGLE_BET_TYPE, DOUBLE_BET_TYPE);

    Optional<Bet> doubleBet = extractBet(placeBetDto, DOUBLE_BET_TYPE);

    assertThat(doubleBet).isPresent();
    assertThat(doubleBet.get().getLeg()).hasSize(2);

    Set<String> doubleBetOutcomes = extractOutcomeIdsFromBet(singleton(doubleBet.get()));

    assertThat(doubleBetOutcomes).containsExactlyInAnyOrder(SELECTED_OUTCOMES);
  }

  @Test
  public void shouldPlaceBetAfterBuildingBetWithTwoSelections() {
    // given
    String addSelRequestBody = getResourceByPath(ADD_SELECTION_REQUEST_JSON);
    String addOtherSelRequestBody = getResourceByPath(ADD_OTHER_SELECTION_REQUEST_JSON);
    String placeBetRequestBody = getResourceByPath(TWO_SINGLE_PLACE_BET_REQUEST_JSON);

    GeneralResponse<BetBuildResponseModel> bppBuildBetResponse =
        buildBetBuildResponseModelWithTwoBuildBet(SELECTED_OUTCOMES, false);

    GeneralResponse<RespBetPlace> betPlaceResponseWoError =
        new GeneralResponse<>(new RespBetPlace(), null);

    when(bettingService.buildBetV2(any(), any())).thenReturn(bppBuildBetResponse);
    when(bettingService.placeBetV2(any(), any(PlaceBetDto.class)))
        .thenReturn(betPlaceResponseWoError);

    when(siteServerService.getEventsForOutcomeIds(any()))
        .thenReturn(outcomeToEvent(SELECTED_OUTCOMES));

    client.login(TOKEN);

    // when
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        addSelRequestBody,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION,
        addOtherSelRequestBody,
        Messages.BUILD_BET_RESPONSE,
        BetBuildResponse.class);
    client.emitWithWaitForResponse(
        Messages.PLACE_BET,
        placeBetRequestBody,
        Messages.PLACE_BET_RESPONSE_CODE,
        RespBetPlace.class);

    // then
    ArgumentCaptor<PlaceBetDto> reqCaptor = ArgumentCaptor.forClass(PlaceBetDto.class);
    verify(bettingService).placeBetV2(anyString(), reqCaptor.capture());

    PlaceBetDto placeBetDto = reqCaptor.getValue();
    assertThat(placeBetDto.getBet()).hasSize(2);

    assertThat(placeBetDto.getBet())
        .allMatch(b -> SINGLE_BET_TYPE.equalsIgnoreCase(b.getBetType()));
    assertThat(placeBetDto.getBet()).anyMatch(b -> "1".equalsIgnoreCase(b.getBetNo()));
    assertThat(placeBetDto.getBet()).anyMatch(b -> "2".equalsIgnoreCase(b.getBetNo()));

    Set<String> allOutcomes = extractOutcomeIdsFromBet(placeBetDto.getBet());

    assertThat(allOutcomes).containsExactlyInAnyOrder(SELECTED_OUTCOMES);
  }

  private Set<String> extractOutcomeIdsFromBet(Set<Bet> bets) {
    return bets.stream()
        .flatMap(b -> b.getLeg().stream())
        .flatMap(l -> l.getPart().stream())
        .map(Part::getOutcome)
        .collect(Collectors.toSet());
  }

  private Optional<Bet> extractBet(PlaceBetDto placeBetDto, String betType) {
    return placeBetDto.getBet().stream().filter(bet -> betType.equals(bet.getBetType())).findAny();
  }

  private GeneralResponse<BetBuildResponseModel> buildBetBuildResponseModelWithTwoBuildBet(
      String[] outcomes, boolean withDouble) {
    GeneralResponse<BetBuildResponseModel> bppBuildBetResponse =
        createResponseWithoutErrors(outcomes);

    bppBuildBetResponse
        .getBody()
        .getBetBuild()
        .add(createBetBuildWithBetCombination("1", SINGLE_BET_TYPE, "1"));
    bppBuildBetResponse
        .getBody()
        .getBetBuild()
        .add(createBetBuildWithBetCombination("2", SINGLE_BET_TYPE, "1"));

    if (withDouble) {
      bppBuildBetResponse
          .getBody()
          .getBetBuild()
          .add(createBetBuildWithBetCombination("3", DOUBLE_BET_TYPE, "2"));
    }

    return bppBuildBetResponse;
  }

  @Test
  public void shouldSendYesForReturnOffers() {
    // GIVEN
    String outcomeId = "12345678";
    AddSelectionRequest request = addSelectionRequest(outcomeId);

    when(bettingService.buildBetV2(any(), any(BetBuildDto.class)))
        .thenReturn(createResponseWithoutErrors(outcomeId));

    when(siteServerService.getEventsForOutcomeIds(List.of(outcomeId)))
        .thenReturn(outcomeToEvent(outcomeId));

    // WHEN
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION, request, Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);

    // THEN
    ArgumentCaptor<BetBuildDto> argument = ArgumentCaptor.forClass(BetBuildDto.class);
    verify(bettingService).buildBetV2(any(), argument.capture());
    assertThat(argument.getValue().getReturnOffers()).isEqualTo(YesNo.Y.name());
  }
}
