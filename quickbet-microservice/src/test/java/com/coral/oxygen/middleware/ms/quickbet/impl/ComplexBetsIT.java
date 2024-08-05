package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection.Type.COMBINATION_TRICAST;
import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection.Type.STRAIGHT_FORECAST;
import static com.coral.oxygen.middleware.ms.quickbet.utils.BetBuildUtils.outcomeToEvent;
import static com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils.deserializeWithJackson;
import static com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils.getResourceByPath;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.timeout;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BetBuildResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.BetBuildDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.Part;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PlaceBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuild;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetCombination;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.OutcomeDetails;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.service.BettingService;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.vavr.Tuple;
import io.vavr.Tuple2;
import io.vavr.collection.Array;
import io.vavr.collection.HashSet;
import io.vavr.collection.List;
import io.vavr.collection.Set;
import java.util.Iterator;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
class ComplexBetsIT {

  private static final String TOKEN =
      "6e650167ccd74b9e8232f8415559b6a498781c5623b539000cb4ed99badffb82";

  @MockBean private BettingService bettingService;

  @MockBean private SiteServerService siteServerService;

  @Autowired private WebSocketTestClient client;

  @Autowired private SessionStorage<SessionDto> sessionStorage;

  @MockBean private LiveServService liveServService;

  @AfterEach
  void cleanUp() {
    client.clearReceivedData();
    client.emitWithWaitForResponse(
        Messages.CLEAR_SELECTION_REQUEST_CODE,
        null,
        Messages.CLEAR_SELECTION_RESPONSE_CODE,
        Object.class);
  }

  @Test
  void shouldAddComplexSelectionToTheSession() throws Exception {
    // when
    addComplexSelectionsToTheBetslip(
        getResourceByPath("integration/complexLegs/addSelection.json"));

    // then
    SessionDto sessionDto = retrieveSessionDto();
    assertThat(sessionDto.getSelectedOutcomeIds()).isEmpty();
    assertThat(sessionDto.getComplexSelections()).hasSize(1);

    ComplexSelection selection = sessionDto.getComplexSelections().head();
    assertThat(selection.getType()).isEqualTo(STRAIGHT_FORECAST);
    assertThat(selection.getOutcomeIds()).hasSize(2).containsExactly("100000", "200000");
  }

  @Test
  void shouldSendBetBuildAfterAddingComplexSelection() throws Exception {
    // when
    addComplexSelectionsToTheBetslip(
        getResourceByPath("integration/complexLegs/addSelection.json"));

    // then
    ArgumentCaptor<BetBuildDto> captor = ArgumentCaptor.forClass(BetBuildDto.class);
    verify(bettingService).buildBetV2(eq(TOKEN), captor.capture());

    BetBuildDto betBuildDto = captor.getValue();
    assertThat(betBuildDto.getBet()).hasSize(1);

    com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Bet bet =
        betBuildDto.getBet().iterator().next();
    assertThat(bet.getBetNo()).isEqualTo("1");
    assertThat(bet.getLeg()).hasSize(1);

    com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Leg leg = bet.getLeg().get(0);
    assertThat(leg.getLegSort()).isEqualTo("SF");

    assertThat(leg.getPart())
        .hasSize(2)
        .extracting(p -> p.getOutcome())
        .containsExactly("100000", "200000");
  }

  @Test
  void shouldRemoveComplexSelectionFromSession() throws Exception {
    // given
    addComplexSelectionsToTheBetslip(
        getResourceByPath("integration/complexLegs/addSelection.json"),
        getResourceByPath("integration/complexLegs/removeSelection/addOtherSelection.json"));

    String removeSelectionJson =
        getResourceByPath("integration/complexLegs/removeSelection/removeSelection.json");
    when(bettingService.buildBetV2(anyString(), any(BetBuildDto.class)))
        .thenReturn(
            createResponseWithoutErrors(Array.of("100000", "200000", "300000", "400000").toList()));

    // when
    client.emit(Messages.REMOVE_COMPLEX_SELECTION, removeSelectionJson);
    client.wait(Messages.BUILD_BET_RESPONSE);

    // then
    SessionDto sessionDto = retrieveSessionDto();
    assertThat(sessionDto.getComplexSelections()).hasSize(1);
    ComplexSelection selection = sessionDto.getComplexSelections().head();
    assertThat(selection.getType()).isEqualTo(COMBINATION_TRICAST);
    assertThat(selection.getOutcomeIds())
        .hasSize(4)
        .containsExactly("100000", "200000", "300000", "400000");
  }

  @Test
  void shouldPlaceComplexBet() throws Exception {
    // given
    addComplexSelectionsToTheBetslip(
        Tuple.of(
            "integration/complexLegs/addSelection.json",
            "integration/complexLegs/placeBet/bppBetBuildResponse.json"));

    // when
    placeBet(getResourceByPath("integration/complexLegs/placeBet/placeBet.json"));

    // then
    ArgumentCaptor<PlaceBetDto> argCaptor = ArgumentCaptor.forClass(PlaceBetDto.class);
    verify(bettingService).placeBetV2(anyString(), argCaptor.capture());

    PlaceBetDto placeBetDto = argCaptor.getValue();
    assertThat(placeBetDto.getBet()).hasSize(1);

    Bet bet = placeBetDto.getBet().iterator().next();
    assertThat(bet.getBetType()).isEqualTo("SGL");
    assertThat(bet.getLeg()).hasSize(1);

    Leg leg = bet.getLeg().iterator().next();
    assertLeg(leg, 1, "SF", 2);

    Part expectedPart1 =
        Part.builder().partNo(1).priceNum(17).priceDen(4).priceType("L").outcome("100000").build();
    Part expectedPart2 = part(2, "L", "200000");
    assertThat(leg.getPart()).containsExactly(expectedPart1, expectedPart2);
  }

  @Test
  void shouldBuildComplexTricastBet() throws Exception {
    // GIVEN
    String selectionRequest =
        TestUtils.getResourceByPath("integration/complexLegs/tricast/addSelection.json");

    mockSiteServerInteraction(extractOutcomeIds(selectionRequest));
    GeneralResponse<BetBuildResponseModel> bppResponse =
        mockBetBuildResponse("integration/complexLegs/tricast/bppBetBuild.json");

    // WHEN
    BetBuildResponse response =
        client.emitWithWaitForResponse(
            Messages.ADD_COMPLEX_SELECTION,
            selectionRequest,
            Messages.BUILD_BET_RESPONSE,
            BetBuildResponse.class);

    // THEN
    ArgumentCaptor<BetBuildDto> captor = ArgumentCaptor.forClass(BetBuildDto.class);
    verify(bettingService).buildBetV2(eq(TOKEN), captor.capture());

    BetBuildDto betBuildDto = captor.getValue();
    assertThat(betBuildDto.getBet()).hasSize(1);

    com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Bet bet =
        betBuildDto.getBet().iterator().next();
    assertThat(bet.getBetNo()).isEqualTo("1");
    assertThat(bet.getLeg()).hasSize(1);

    com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Leg leg = bet.getLeg().get(0);
    assertThat(leg.getLegSort()).isEqualTo("TC");

    assertThat(leg.getPart())
        .hasSize(3)
        .extracting(p -> p.getOutcome())
        .containsExactly("554588838", "554588841", "554588843");

    assertThat(response.getBetBuildResponseModel())
        .isEqualToComparingFieldByFieldRecursively(bppResponse.getBody());

    ArgumentCaptor<String> channelsCaptor = ArgumentCaptor.forClass(String.class);

    verify(liveServService, times(7)).subscribe(channelsCaptor.capture());
    assertThat(channelsCaptor.getAllValues())
        .containsExactlyInAnyOrder(
            "sEVENT0010008830",
            "sSCBRD0010008830",
            "sEVMKT0148619513",
            "sSELCN0554588841",
            "sCLOCK0010008830",
            "sSELCN0554588843",
            "sSELCN0554588838");
  }

  @Test
  void shouldAddTwoComplexSelectionsAndPlaceBetForBoth() throws Exception {
    // given
    String resourcesRoot = "integration/complexLegs/placeBetWithTwoSelections/";
    addComplexSelectionsToTheBetslip(
        Tuple.of(
            resourcesRoot + "addFirstSelection.json", resourcesRoot + "firstBetBuildResponse.json"),
        Tuple.of(
            resourcesRoot + "addSecondSelection.json",
            resourcesRoot + "secondBetBuildResponse.json"));

    // when
    placeBet(getResourceByPath(resourcesRoot + "placeBetWithBothSelections.json"));

    // then
    verify(bettingService, times(2)).buildBetV2(eq(TOKEN), any());

    ArgumentCaptor<PlaceBetDto> argCaptor = ArgumentCaptor.forClass(PlaceBetDto.class);
    verify(bettingService).placeBetV2(eq(TOKEN), argCaptor.capture());

    PlaceBetDto placeBetDto = argCaptor.getValue();
    assertThat(placeBetDto.getBet()).hasSize(2);
    Iterator<Bet> betsIterator = placeBetDto.getBet().iterator();

    // VERIFY FORECAST BET
    Bet forecastBet = betsIterator.next();
    assertThat(forecastBet.getBetType()).isEqualTo("SGL");
    assertThat(forecastBet.getLeg()).hasSize(1);

    Leg forecastLeg = forecastBet.getLeg().iterator().next();
    assertLeg(forecastLeg, 1, "SF", 2);

    assertThat(forecastLeg.getPart())
        .containsExactly(part(1, "D", "557374867"), part(2, "D", "557374865"));

    // VERIFY TRICAST BET
    Bet tricastBet = betsIterator.next();
    assertThat(tricastBet.getBetType()).isEqualTo("SGL");
    assertThat(tricastBet.getLeg()).hasSize(1);

    Leg tricastLeg = tricastBet.getLeg().iterator().next();
    assertLeg(tricastLeg, 1, "CT", 5);

    assertThat(tricastLeg.getPart())
        .containsExactly(
            part(1, "D", "557374865"),
            part(2, "D", "557374856"),
            part(3, "D", "557374860"),
            part(4, "D", "557374866"),
            part(5, "D", "557374861"));

    assertAllSelectionsAreClearedAfterPlaceBet();
  }

  @Test
  void shouldAddTwoSelectionsAndPlaceBetWithOnlyOneOfThem() throws Exception {
    // given
    String resourcesRoot = "integration/complexLegs/placeBetWithTwoSelections/";
    addComplexSelectionsToTheBetslip(
        Tuple.of(
            resourcesRoot + "addFirstSelection.json", resourcesRoot + "firstBetBuildResponse.json"),
        Tuple.of(
            resourcesRoot + "addSecondSelection.json",
            resourcesRoot + "secondBetBuildResponse.json"));

    // when
    placeBet(getResourceByPath(resourcesRoot + "placeBetWithOnlySecondSelection.json"));

    // then
    verify(bettingService, times(2)).buildBetV2(eq(TOKEN), any());

    ArgumentCaptor<PlaceBetDto> argCaptor = ArgumentCaptor.forClass(PlaceBetDto.class);
    verify(bettingService).placeBetV2(eq(TOKEN), argCaptor.capture());

    PlaceBetDto placeBetDto = argCaptor.getValue();
    assertThat(placeBetDto.getBet()).hasSize(1);
    Iterator<Bet> betsIterator = placeBetDto.getBet().iterator();

    Bet tricastBet = betsIterator.next();
    assertThat(tricastBet.getBetType()).isEqualTo("SGL");
    assertThat(tricastBet.getLeg()).hasSize(1);

    Leg tricastLeg = tricastBet.getLeg().iterator().next();
    assertLeg(tricastLeg, 1, "CT", 5);

    assertThat(tricastLeg.getPart())
        .containsExactly(
            part(1, "D", "557374865"),
            part(2, "D", "557374856"),
            part(3, "D", "557374860"),
            part(4, "D", "557374866"),
            part(5, "D", "557374861"));

    assertAllSelectionsAreClearedAfterPlaceBet();
  }

  @Test
  void removingSelectionOnEmptyBetslipShouldNotTriggerBetBuild() {
    // given
    String removeSelectionJson =
        getResourceByPath("integration/complexLegs/removeSelection/removeSelection.json");

    // when
    client.emit(Messages.REMOVE_COMPLEX_SELECTION, removeSelectionJson);
    client.wait(Messages.SELECTION_TO_REMOVE_NOT_PRESENT);

    // then
    verify(bettingService, never()).buildBetV2(any(), any());
  }

  @Test
  void duplicatedAddSelectionRequestShouldBeIgnoredAndNotTriggerNewBetBuild() throws Exception {
    // given
    String addSelectionRequest = getResourceByPath("integration/complexLegs/addSelection.json");
    addComplexSelectionsToTheBetslip(addSelectionRequest);

    // when
    client.emit(Messages.ADD_COMPLEX_SELECTION, addSelectionRequest);
    client.wait(Messages.SELECTION_EMPTY_OR_ALREADY_ADDED);

    // then
    verify(bettingService).buildBetV2(any(), any());
    assertThat(retrieveSessionDto().getComplexSelections()).hasSize(1);
  }

  @Test
  @DisplayName("should clear session after bet in run is accepted")
  void betInRunAccepted() throws Exception {
    // given
    addComplexSelectionsToTheBetslip(
        Tuple.of(
            "integration/complexLegs/addSelection.json",
            "integration/complexLegs/placeBet/bppBetBuildResponse.json"));

    String placeBetJson = getResourceByPath("integration/complexLegs/placeBet/placeBet.json");
    RespBetPlace respBetPlace =
        deserializeWithJackson(
            "integration/complexLegs/betInRun/placeBetResponse.json", RespBetPlace.class);
    when(bettingService.placeBetV2(eq(TOKEN), any(PlaceBetDto.class)))
        .thenReturn(new GeneralResponse<>(respBetPlace, null));

    BetsResponse readBetResponse =
        deserializeWithJackson(
            "integration/complexLegs/betInRun/readBetResponseAccepted.json", BetsResponse.class);
    when(bettingService.readBet(anyString(), anyList()))
        .thenReturn(new GeneralResponse<>(readBetResponse, null));

    // when
    client.emit(Messages.PLACE_BET, placeBetJson);

    // then
    assertThat(retrieveSessionDto().getComplexSelections())
        .isNotEmpty(); // selections are stored during bet in run
    // processing
    client.wait(Messages.CLEAR_SELECTION_RESPONSE_CODE);
    verify(bettingService).readBet(anyString(), anyList());
    assertThat(retrieveSessionDto().getComplexSelections())
        .isEmpty(); // selections are cleared after bet in run
    // acceptance
  }

  @Test
  @DisplayName("should not clear session if bet in run is rejected")
  void betInRunRejected() throws Exception {
    // given
    addComplexSelectionsToTheBetslip(
        Tuple.of(
            "integration/complexLegs/addSelection.json",
            "integration/complexLegs/placeBet/bppBetBuildResponse.json"));

    String placeBetJson = getResourceByPath("integration/complexLegs/placeBet/placeBet.json");
    RespBetPlace respBetPlace =
        deserializeWithJackson(
            "integration/complexLegs/betInRun/placeBetResponse.json", RespBetPlace.class);
    when(bettingService.placeBetV2(eq(TOKEN), any(PlaceBetDto.class)))
        .thenReturn(new GeneralResponse<>(respBetPlace, null));

    BetsResponse readBetResponse =
        deserializeWithJackson(
            "integration/complexLegs/betInRun/readBetResponseRejected.json", BetsResponse.class);
    when(bettingService.readBet(anyString(), anyList()))
        .thenReturn(new GeneralResponse<>(readBetResponse, null));

    // when
    client.emit(Messages.PLACE_BET, placeBetJson);

    // then
    assertThat(retrieveSessionDto().getComplexSelections())
        .isNotEmpty(); // selections are stored during bet in run
    // processing
    verify(bettingService, timeout(5000)).readBet(anyString(), anyList());
    assertThat(retrieveSessionDto().getComplexSelections())
        .isNotEmpty(); // selections are not cleared
  }

  private SessionDto retrieveSessionDto() {
    return sessionStorage.find(client.getSessionId()).get();
  }

  // TODO: extract as much of below methods as possible to some Utils class

  private Part part(int i, String d, String s) {
    return Part.builder().partNo(i).priceType(d).outcome(s).build();
  }

  private void assertLeg(Leg forecastLeg, Integer legNo, String legSort, Integer partsSize) {
    assertThat(forecastLeg.getLegNo()).isEqualTo(legNo);
    assertThat(forecastLeg.getLegSort()).isEqualTo(legSort);
    assertThat(forecastLeg.getPart()).hasSize(partsSize);
  }

  private void assertAllSelectionsAreClearedAfterPlaceBet() {
    SessionDto sessionDto = retrieveSessionDto();
    assertThat(sessionDto.getSelectedOutcomeIds()).isEmpty();
    assertThat(sessionDto.getComplexSelections()).isEmpty();
  }

  private void placeBet(String placeBetJson) {
    when(bettingService.placeBetV2(eq(TOKEN), any(PlaceBetDto.class)))
        .thenReturn(new GeneralResponse<>(new RespBetPlace(), null));
    client.emit(Messages.PLACE_BET, placeBetJson);
    client.wait(Messages.PLACE_BET_RESPONSE_CODE);
  }

  private void addComplexSelectionsToTheBetslip(String... addSelectionJsons) throws Exception {
    for (String addSelJson : addSelectionJsons) {
      mockSiteServerInteraction(extractOutcomeIds(addSelJson));
      when(bettingService.buildBetV2(anyString(), any(BetBuildDto.class)))
          .thenReturn(createResponseWithoutErrors(extractOutcomeIds(addSelJson)));
      emitAddComplexSelectionMessage(addSelJson);
    }
  }

  private void addComplexSelectionsToTheBetslip(
      Tuple2<String, String>... addSelectionRequestsWithBetBuildResponses) throws Exception {
    Set<String> siteServerOutcomeIds = HashSet.empty();
    for (Tuple2<String, String> addSelReqWithBetBuildResp :
        addSelectionRequestsWithBetBuildResponses) {
      String betBuildRespPath = addSelReqWithBetBuildResp._2;
      String addSelectionJson = getResourceByPath(addSelReqWithBetBuildResp._1);

      siteServerOutcomeIds = siteServerOutcomeIds.addAll(extractOutcomeIds(addSelectionJson));
      mockSiteServerInteraction(siteServerOutcomeIds.toList());
      mockBetBuildResponse(betBuildRespPath);
      emitAddComplexSelectionMessage(addSelectionJson);
    }
  }

  private void emitAddComplexSelectionMessage(String addSelectionJson) {
    client.login(TOKEN);
    client.emit(Messages.ADD_COMPLEX_SELECTION, addSelectionJson);
    client.wait(Messages.BUILD_BET_RESPONSE);
    client.clearReceivedData();
  }

  private void mockSiteServerInteraction(List<String> outcomeIds) {
    when(siteServerService.getEventsForOutcomeIds(any())).thenReturn(outcomeToEvent(outcomeIds));
  }

  private List<String> extractOutcomeIds(String json) throws Exception {
    ObjectMapper mapper = new ObjectMapper();
    return mapper.readValue(json, AddComplexSelectionRequest.class).getOutcomeIds();
  }

  private GeneralResponse<BetBuildResponseModel> mockBetBuildResponse(String path) {
    BetBuildResponseModel bppResponseModel =
        deserializeWithJackson(path, BetBuildResponseModel.class);
    GeneralResponse<BetBuildResponseModel> bppResponse =
        createBppResponseWithoutErrors(bppResponseModel);
    when(bettingService.buildBetV2(any(), any(BetBuildDto.class))).thenReturn(bppResponse);
    return bppResponse;
  }

  private GeneralResponse<BetBuildResponseModel> createBppResponseWithoutErrors(
      BetBuildResponseModel betBuild) {
    return new GeneralResponse<>(betBuild, null);
  }

  private GeneralResponse<BetBuildResponseModel> createResponseWithoutErrors(
      List<String> outcomeIds) {
    BetBuildResponseModel responseModel = new BetBuildResponseModel();
    outcomeIds.forEach(otcId -> responseModel.getOutcomeDetails().add(createOutcomeDetails(otcId)));

    BetBuild betBuild = new BetBuild();
    betBuild.setBetNo("1");
    BetCombination combination = new BetCombination();
    combination.setBetType("SGL");
    betBuild.getBetCombination().add(combination);
    responseModel.getBetBuild().add(betBuild);

    return new GeneralResponse<>(responseModel, null);
  }

  private OutcomeDetails createOutcomeDetails(String outcomeId) {
    OutcomeDetails outcomeDetails = new OutcomeDetails();
    outcomeDetails.setId(outcomeId);
    outcomeDetails.setMarketId("2");
    outcomeDetails.setEventId("1");
    return outcomeDetails;
  }
}
