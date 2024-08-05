package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.OUTCOME_REQUEST_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.REGULAR_OUTCOME_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.REGULAR_OUTCOME_RESPONSE_ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest.AdditionalParameters;
import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest.SCORECAST_SELECTION_TYPE;
import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest.SIMPLE_SELECTION_TYPE;
import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse.Error;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.GeneralResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import com.egalacoral.spark.siteserver.model.Scorecast;
import com.fasterxml.jackson.core.type.TypeReference;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
class AddRegularSelectionIT {

  @MockBean private SiteServerService siteServerService;

  @Autowired private WebSocketTestClient client;

  @Test
  void shouldReturnErrorWhenSelectionTypeIsNotSent() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L));

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "selectionType is required");
  }

  @Test
  void shouldReturnErrorWhenSelectionTypeHasInvalidValue() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L));
    request.setSelectionType("invalid");

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "Unsupported selection type 'invalid'");
  }

  @Test
  void shouldReturnErrorWhenAdditionalParametersExistsForSimpleSelection() throws Exception {
    // given
    AdditionalParameters additionalParameters = new AdditionalParameters();
    additionalParameters.setScorecastMarketId(142L);

    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L));
    request.setSelectionType(SIMPLE_SELECTION_TYPE);
    request.setAdditional(additionalParameters);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "additional parameters aren't allowed for simple request");
  }

  @Test
  void shouldReturnErrorWhenMoreThanOneOutcomeIsGivenForSimpleSelection() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(111L, 222L, 333L));
    request.setSelectionType(SIMPLE_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "simple selection requires 1 outcomes");
  }

  @Test
  void shouldReturnErrorWhenOutcomesIsNullForScorecastSelection() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setSelectionType(SCORECAST_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE, request, "INVALID_REQUEST", "outcomeIds is null");
  }

  @Test
  void shouldReturnErrorWhenOutcomesAreEmptyForScorecastSelection() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList());
    request.setSelectionType(SCORECAST_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE, request, "INVALID_REQUEST", "empty outcomeIds");
  }

  @Test
  void shouldReturnErrorWhenOutcomeIdIsNullForScorecastSelection() throws Exception {
    // given
    List<Long> outcomeIds = new LinkedList<>();
    outcomeIds.add(123L);
    outcomeIds.add(null);

    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(outcomeIds);
    request.setSelectionType(SCORECAST_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "null outcome id in element 1");
  }

  @Test
  void shouldReturnErrorWhenOutcomesSizeIsToSmallForScorecastSelection() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L));
    request.setSelectionType(SCORECAST_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "scorecast selection requires 2 outcomes");
  }

  @Test
  void shouldReturnErrorWhenAdditionalParametersDoNotExistForScorecastSelection() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L, 321L));
    request.setSelectionType(SCORECAST_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "INVALID_REQUEST",
        "additional.scorecastMarketId parameter is required");
  }

  @Test
  void shouldReturnErrorWhenSiteServCannotFindOutcome() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L));
    request.setSelectionType(SIMPLE_SELECTION_TYPE);

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "SITESERV_ERROR",
        "Error reading outcome data. Siteserv is down");
  }

  @Test
  void shouldReturnErrorWhenSiteServResponseListIsEmpty() throws Exception {
    // given
    long outcomeId = 123;

    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(outcomeId));
    request.setSelectionType(SIMPLE_SELECTION_TYPE);

    when(siteServerService.getEventToOutcomeForOutcome(any())).thenReturn(Optional.of(emptyList()));

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "EVENT_NOT_FOUND",
        "Error reading outcome data. Data not found. OutcomeIds - [" + outcomeId + "]");
  }

  @Test
  void shouldReturnErrorWhenSiteServResponseListHasMoreThanOneEvent() throws Exception {
    // given
    long outcomeId = 123;

    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(outcomeId));
    request.setSelectionType(SIMPLE_SELECTION_TYPE);

    Event event1 = new Event();
    event1.setId("27417");

    Event event2 = new Event();
    event1.setId("37417");

    when(siteServerService.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(asList(event1, event2)));

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "EVENTS_TOO_MUCH",
        "Error reading outcome data. Too many events. OutcomeIds - [" + outcomeId + "]");
  }

  @Test
  void shouldReturnErrorWhenResponseIsEmpty() throws Exception {
    // given
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(123L));
    request.setSelectionType(SIMPLE_SELECTION_TYPE);

    when(siteServerService.getEventToOutcomeForOutcome(any())).thenReturn(Optional.empty());

    // when / then
    shouldReturnError(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        request,
        "SITESERV_ERROR",
        "Error reading outcome data. Siteserv is down");
  }

  @Test
  void shouldAddSimpleSelection() throws Exception {
    // given
    Outcome outcome = outcome("549210360");
    Market market = market("142", asList(outcome));
    Event event = event("27417", asList(market));

    List<Long> outcomeIds = asList(Long.valueOf(outcome.getId()));

    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(outcomeIds);
    request.setSelectionType("simple");

    when(siteServerService.getEventToOutcomeForOutcome(outcomeIds))
        .thenReturn(Optional.of(asList(event)));
    TypeReference<GeneralResponse<RegularSelectionResponse>> typeRef =
        new TypeReference<GeneralResponse<RegularSelectionResponse>>() {};

    // when
    client.emit(OUTCOME_REQUEST_CODE, request);
    GeneralResponse<RegularSelectionResponse> generalResponse =
        client.wait(REGULAR_OUTCOME_RESPONSE_CODE, typeRef);

    // then
    RegularSelectionResponse response = generalResponse.getData();
    assertThat(response.getEvent().getId()).isEqualTo(event.getId());
    assertThat(response.getEvent().getMarkets())
        .hasOnlyOneElementSatisfying(
            respMarket ->
                assertThat(respMarket.getOutcomes())
                    .hasOnlyOneElementSatisfying(
                        respOutcome -> assertThat(respOutcome.getId()).isEqualTo(outcome.getId())));
  }

  @Test
  void shouldAddScorecastSelection() throws Exception {
    // given
    Outcome outcome1 = outcome("549210360", 1.1);
    outcome1.setOutcomeMeaningScores("1,3");

    Outcome outcome2 = outcome("603012549", 2.5);
    outcome2.setOutcomeMeaningMinorCode("H");

    Market scoreMarket = market("111", Collections.singletonList(outcome1), "CS");
    Market goalScoreMarket = market("222", Collections.singletonList(outcome2), "FS");

    Event event = event("27417", asList(scoreMarket, goalScoreMarket));

    AdditionalParameters additionalParameters = new AdditionalParameters();
    additionalParameters.setScorecastMarketId(Long.valueOf(scoreMarket.getId()));

    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(asList(Long.valueOf(outcome1.getId()), Long.valueOf(outcome2.getId())));
    request.setSelectionType("scorecast");
    request.setAdditional(additionalParameters);

    when(siteServerService.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(asList(event)));
    TypeReference<GeneralResponse<RegularSelectionResponse>> typeRef =
        new TypeReference<GeneralResponse<RegularSelectionResponse>>() {};

    Scorecast scorecast1 = new Scorecast();
    scorecast1.setScorerOutcomeId(outcome1.getId());
    scorecast1.setScorecastPrices("999");

    Scorecast scorecast2 = new Scorecast();
    scorecast2.setScorerOutcomeId(outcome2.getId());
    scorecast2.setScorecastPrices("888");

    when(siteServerService.getScorecast(scoreMarket.getId(), outcome1.getId()))
        .thenReturn(Optional.of(scorecast1));
    when(siteServerService.getScorecast(goalScoreMarket.getId(), outcome2.getId()))
        .thenReturn(Optional.of(scorecast2));

    // when
    client.emit(OUTCOME_REQUEST_CODE, request);
    GeneralResponse<RegularSelectionResponse> generalResponse =
        client.wait(REGULAR_OUTCOME_RESPONSE_CODE, typeRef);

    // then
    RegularSelectionResponse response = generalResponse.getData();
    assertThat(response.getEvent().getId()).isEqualTo(event.getId());
    assertThat(response.getEvent().getMarkets()).hasSize(2);

    assertThat(response.getEvent().getMarkets().get(0).getOutcomes()).hasSize(1);
    assertThat(response.getEvent().getMarkets().get(0).getOutcomes().get(0).getId())
        .isEqualTo(outcome1.getId());

    assertThat(response.getEvent().getMarkets().get(1).getOutcomes()).hasSize(1);
    assertThat(response.getEvent().getMarkets().get(1).getOutcomes().get(0).getId())
        .isEqualTo(outcome2.getId());
  }

  private void shouldReturnError(
      Messages message, RegularSelectionRequest request, String errorCode, String errorMessage)
      throws Exception {
    // when
    client.emit(OUTCOME_REQUEST_CODE, request);
    RegularPlaceBetResponse response = client.wait(message, RegularPlaceBetResponse.class);

    // then
    Error error = response.getData().getError();
    assertThat(error.getCode()).isEqualTo(errorCode);
    assertThat(error.getDescription()).isEqualTo(errorMessage);
  }

  private Children asChildren(Outcome outcome) {
    Children children = new Children();
    children.setOutcome(outcome);

    return children;
  }

  private Children asChildren(Market market) {
    Children children = new Children();
    children.setMarket(market);

    return children;
  }

  private Children asChildren(Price price) {
    Children children = new Children();
    children.setPrice(price);

    return children;
  }

  private Outcome outcome(String id) {
    return outcome(id, null);
  }

  private Outcome outcome(String id, Double priceDec) {
    Price price = new Price();
    price.setPriceDec(priceDec);

    Outcome outcome = new Outcome();
    outcome.setId(id);
    outcome.setChildren(Collections.singletonList(asChildren(price)));

    return outcome;
  }

  private Market market(String id, List<Outcome> outcomes) {
    return market(id, outcomes, null);
  }

  private Market market(String id, List<Outcome> outcomes, String dispSortName) {
    Market market = new Market();
    market.setId(id);
    market.setDispSortName(dispSortName);
    market.setChildren(
        outcomes.stream().map(outcome -> asChildren(outcome)).collect(Collectors.toList()));

    return market;
  }

  private Event event(String id, List<Market> markets) {
    Event event = new Event();
    event.setId(id);
    event.setChildren(
        markets.stream().map(outcome -> asChildren(outcome)).collect(Collectors.toList()));

    return event;
  }
}
