package com.ladbrokescoral.oxygen.buildyourbetms;

import static org.springframework.restdocs.payload.PayloadDocumentation.fieldWithPath;
import static org.springframework.restdocs.payload.PayloadDocumentation.requestFields;
import static org.springframework.restdocs.payload.PayloadDocumentation.responseFields;
import static org.springframework.restdocs.request.RequestDocumentation.parameterWithName;
import static org.springframework.restdocs.request.RequestDocumentation.pathParameters;
import static org.springframework.restdocs.request.RequestDocumentation.requestParameters;
import static org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation.document;

import com.ladbrokescoral.oxygen.buildyourbetms.dto.MarketGroup;
import com.ladbrokescoral.oxygen.buildyourbetms.dto.MarketsGroupedDto;
import com.ladbrokescoral.oxygen.buildyourbetms.dto.PriceRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetMarketResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.StatusEnum;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.VirtualSelectionDto;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import java.util.Arrays;
import lombok.SneakyThrows;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockserver.client.MockServerClient;
import org.mockserver.junit.jupiter.MockServerExtension;
import org.mockserver.junit.jupiter.MockServerSettings;
import org.mockserver.model.HttpRequest;
import org.mockserver.model.HttpResponse;
import org.mockserver.model.JsonBody;
import org.mockserver.model.Parameter;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.http.MediaType;
import org.springframework.restdocs.RestDocumentationContextProvider;
import org.springframework.restdocs.RestDocumentationExtension;
import org.springframework.restdocs.payload.FieldDescriptor;
import org.springframework.restdocs.payload.ResponseFieldsSnippet;
import org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.reactive.server.WebTestClient;

@ExtendWith({SpringExtension.class, RestDocumentationExtension.class, MockServerExtension.class})
@MockServerSettings(ports = {8099})
@Tag("restdocs")
@ActiveProfiles("UNIT")
@SpringBootTest
class BuildYourBetMsApplicationTests {

  private WebTestClient webTestClient;
  private MockServerClient mockServerClient;

  @TestConfiguration
  static class TestContextConfiguration {

    @Bean
    public Clock clock() {
      return Clock.fixed(Instant.ofEpochSecond(1527601168), ZoneId.of("UTC"));
    }
  }

  @BeforeEach
  void setUp(
      ApplicationContext webApplicationContext,
      RestDocumentationContextProvider restDocumentationContextProvider,
      MockServerClient mockServerClient) {

    this.mockServerClient = mockServerClient;

    this.webTestClient =
        WebTestClient.bindToApplicationContext(webApplicationContext)
            .configureClient()
            .baseUrl("https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com")
            .filter(
                WebTestClientRestDocumentation.documentationConfiguration(
                        restDocumentationContextProvider)
                    .snippets())
            .build();
  }

  @AfterEach
  void tearDown() {
    mockServerClient.reset();
  }

  @Test
  void testLeagues() {
    mockUrlWithFile(
        "/api/buildabet/leagues",
        "leagues.json",
        Parameter.param("fromEpochMillis", "1526990364000"),
        Parameter.param("toEpochMillis", "1526991369000"));

    this.webTestClient
        .get()
        .uri("/api/v1/leagues?fromEpochMillis=1526990364000&toEpochMillis=1526991369000")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "leagues",
                requestParameters(
                    parameterWithName("fromEpochMillis")
                        .description(
                            "To return leagues with events which start time is after timestamp(milliseconds)"),
                    parameterWithName("toEpochMillis")
                        .description(
                            "To return leagues with events which start time is before timestamp(milliseconds)")),
                responseFields().andWithPrefix("data[].", leaguesDescription())));
  }

  private FieldDescriptor[] leaguesDescription() {
    return new FieldDescriptor[] {obTypeId(), fieldWithPath("title").description("League Title")};
  }

  @Test
  void testLeaguesUpcoming() {
    mockUrlWithFile(
        "/api/buildabet/leagues",
        "leaguesToday.json",
        Parameter.param("fromEpochMillis", "1527601168000"),
        Parameter.param("toEpochMillis", "1527631199000"));
    mockUrlWithFile(
        "/api/buildabet/leagues",
        "leaguesAfterToday.json",
        Parameter.param("fromEpochMillis", "1527631200000"),
        Parameter.param("toEpochMillis", "1527717599000"));

    this.webTestClient
        .get()
        .uri("/api/v1/leagues-upcoming?days=2&tz=2")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "leagues-upcoming",
                requestParameters(
                    parameterWithName("days")
                        .description(
                            "How many days to search leagues for. days=1 will return just today's leagues"),
                    parameterWithName("tz")
                        .description("Client's timezone offset in hours. For example 3, -2, 0")),
                responseFields()
                    .andWithPrefix("data.today[]", leaguesDescription())
                    .andWithPrefix("data.upcoming[]", leaguesDescription())));
  }

  @Test
  void testEvents() {
    mockEvents();

    this.webTestClient
        .get()
        .uri("/api/v1/events")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(document("events", eventsResponse()));
  }

  @Test
  void testEventsByLeagueId() {
    mockEventByLeagueId();

    this.webTestClient
        .get()
        .uri(
            "/api/v1/events?leagueIds=382,442&dateFrom=2018-05-23T17:14:00.000Z&dateTo=2018-05-23T21:00:00.000Z")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "eventsByLeague",
                requestParameters(
                    parameterWithName("leagueIds")
                        .description("List of leagues ids for which to get events"),
                    parameterWithName("dateFrom")
                        .description("To return events which start time is after specified date"),
                    parameterWithName("dateTo")
                        .description("To return events which start time is before date")),
                eventsResponse()));
  }

  @Test
  void testEventsWhenLeaguesIdsContainMalformedId() {
    this.webTestClient
        .get()
        .uri("/api/v1/events?leagueIds=abc,557")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }

  @Test
  void testEvent() {
    mockUrlWithFile(
        "/api/buildabet/event", "eventById.json", Parameter.param("obEventId", "8168883"));

    this.webTestClient
        .get()
        .uri("/api/v1/events/{id}", 8168883)
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .jsonPath("$.data.obEventId")
        .isEqualTo(8168883)
        .consumeWith(
            document(
                "event",
                eventResponse(),
                pathParameters(parameterWithName("id").description("OpenBet Event Id"))));
  }

  @Test
  void testEvent404Returns200() {
    mockServerClient
        .when(
            HttpRequest.request("/api/buildabet/event")
                .withQueryStringParameters(Parameter.param("obEventId", "123")))
        .respond(HttpResponse.response().withStatusCode(404));

    this.webTestClient.get().uri("/api/v1/events/{id}", 123).exchange().expectStatus().isOk();
  }

  @Test
  void testEventWithMalformedId() {
    this.webTestClient
        .get()
        .uri("/api/v1/events/{id}", "abc")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }

  @Test
  void testMarkets() {
    mockUrlWithFile(
        "/api/buildabet/markets", "markets.json", Parameter.param("obEventId", "6167221"));

    this.webTestClient
        .get()
        .uri("/api/v1/markets?obEventId=6167221")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "markets",
                responseFields().andWithPrefix("data[].", marketFieldDescription()),
                requestParameters(parameterWithName("obEventId").description("OpenBet Event Id"))));
  }

  @Test
  void testMarketsGrouped() {
    mockUrlWithFile(
        "/api/buildabet/markets-grouped",
        "marketsGrouped.json",
        Parameter.param("obEventId", "6167221"));

    this.webTestClient
        .get()
        .uri("/api/v1/markets-grouped?obEventId=6167221")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "marketsGrouped",
                responseFields(
                        fieldWithPath("data[].incidentGrouping").description("Incident Grouping"),
                        fieldWithPath("data[].marketGrouping").description("Market Grouping"))
                    .andWithPrefix("data[].markets[]", marketFieldDescription()),
                requestParameters(parameterWithName("obEventId").description("OpenBet Event Id"))));
  }

  @Test
  void testMarketsGroupedV2() {
    mockUrlWithFile(
        "/api/buildabet/markets",
        "marketsWithEmptyGroups.json",
        Parameter.param("obEventId", "6167221"));

    MarketsGroupedDto expected =
        MarketsGroupedDto.builder()
            .groupedMarket(
                MarketGroup.builder()
                    .marketGroupName("NO_GROUP")
                    .market(
                        GetMarketResponseDto.builder()
                            .groupName("NO_GROUP")
                            .id(4L)
                            .title("WITHOUT GROUP 1")
                            .status(StatusEnum.NUMBER_1)
                            .build())
                    .market(
                        GetMarketResponseDto.builder()
                            .groupName("NO_GROUP")
                            .id(5L)
                            .title("WITHOUT GROUP 2")
                            .status(StatusEnum.NUMBER_1)
                            .build())
                    .market(
                        GetMarketResponseDto.builder()
                            .groupName("NO_GROUP")
                            .id(6L)
                            .title("WITHOUT GROUP 3")
                            .status(StatusEnum.NUMBER_1)
                            .build())
                    .build())
            .groupedMarket(
                MarketGroup.builder()
                    .marketGroupName("Group 2")
                    .market(
                        GetMarketResponseDto.builder()
                            .id(3L)
                            .title("SECOND HALF BETTING")
                            .status(StatusEnum.NUMBER_1)
                            .groupName("Group 2")
                            .build())
                    .build())
            .groupedMarket(
                MarketGroup.builder()
                    .marketGroupName("Group 1")
                    .market(
                        GetMarketResponseDto.builder()
                            .id(1L)
                            .title("MATCH BETTING")
                            .status(StatusEnum.NUMBER_1)
                            .groupName("Group 1")
                            .build())
                    .market(
                        GetMarketResponseDto.builder()
                            .id(2L)
                            .title("FIRST HALF BETTING")
                            .status(StatusEnum.NUMBER_1)
                            .groupName("Group 1")
                            .build())
                    .build())
            .build();

    this.webTestClient
        .get()
        .uri("/api/v2/markets-grouped?obEventId=6167221")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(MarketsGroupedDto.class)
        .isEqualTo(expected)
        .consumeWith(
            document(
                "marketsGroupedV2",
                responseFields(
                        fieldWithPath("data[].marketGroupName").description("Market Group Name"))
                    .andWithPrefix("data[].markets[].", marketFieldDescription()),
                requestParameters(parameterWithName("obEventId").description("OpenBet Event Id"))));
  }

  @Test
  void testPrice() {
    mockPrice();

    VirtualSelectionDto playerSelection = new VirtualSelectionDto();
    playerSelection.setPlayerId(1L);
    playerSelection.setLine(10L);
    playerSelection.setStatId(2L);

    this.webTestClient
        .post()
        .uri("/api/v1/price")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(
            PriceRequestDto.builder()
                .obEventId(8168883L)
                .selectionId(1L)
                .selectionId(4L)
                .playerSelection(playerSelection)
                .build())
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "price",
                requestFields(
                    obEventId(),
                    fieldWithPath("selectionIds").description("Array of Selection ids (Banach)"),
                    fieldWithPath("playerSelections[].statId")
                        .description("Id of statisticic (passes, tackles, etc)"),
                    fieldWithPath("playerSelections[].playerId").description("Player Id"),
                    fieldWithPath("playerSelections[].line")
                        .description("Statistic value, for example 10 passes")),
                responseFields(
                    fieldWithPath("data.priceNum").description("Price numerator"),
                    fieldWithPath("data.priceDen").description("Price denumerator"),
                    fieldWithPath("data.hundredPcLine").description("Real probability"),
                    fieldWithPath("data.responseCode")
                        .description(
                            "0 - Unkown, 1 - Ok, 2 - InvalidCombination, 3 - ComponentSuspended, 4 - InvalidMarginatedPrice"),
                    fieldWithPath("data.responseMessage").description("Response message"))));
  }

  @Test
  void testSelections() {
    mockSelection();

    this.webTestClient
        .get()
        .uri("/api/v1/selections?obEventId=6167221&marketIds=1")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "selections",
                responseFields(
                    fieldWithPath("data[].id").description("Market id"),
                    fieldWithPath("data[].selections[].id").description("Selection Id"),
                    fieldWithPath("data[].selections[].relatedTeamType")
                        .description("Team Type. 1 - Home, 2 - Away, 0 - Draw or Neither"),
                    fieldWithPath("data[].selections[].relatedPlayerId")
                        .description("Player Id in Banach system. 0 - means no player applicable"),
                    fieldWithPath("data[].selections[].title").description("Selection title"),
                    fieldWithPath("data[].selections[].odds").description("Selection odds"),
                    fieldWithPath("data[].selections[].status").description("Selection status"),
                    fieldWithPath("data[].selections[].bettingValue1")
                        .description(
                            "Home Score or Under line or Handicap line depending on market context"),
                    fieldWithPath("data[].selections[].bettingValue2")
                        .description(
                            "Away Score or Over line or Handicap line depending on market context"),
                    fieldWithPath("data[].selections[].displayOrder").description("Display order")),
                requestParameters(
                    parameterWithName("obEventId").description("OpenBet Event Id"),
                    parameterWithName("marketIds").description("Array of Market ids (Banach)"))));
  }

  @Test
  void testPlayers() {
    // todo mockPlayers
    mockUrlWithFile(
        "/api/buildabet/players", "players.json", Parameter.param("obEventId", "6167221"));

    this.webTestClient
        .get()
        .uri("/api/v1/players?obEventId=6167221")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "players",
                responseFields(
                        fieldWithPath("data[].id").description("Player id"),
                        fieldWithPath("data[].optaId").description("Null"),
                        fieldWithPath("data[].number").description(""),
                        fieldWithPath("data[].optaId").description("opta player id"),
                        fieldWithPath("data[].name").description("Player name"),
                        fieldWithPath("data[].position.id").description("Player's position id"),
                        fieldWithPath("data[].position.title")
                            .description("Player's position titile"),
                        fieldWithPath("data[].status").description("Player's status"))
                    .andWithPrefix("data[].team.", teamFieldDescription()),
                requestParameters(parameterWithName("obEventId").description("OpenBet Event Id"))));
  }

  @Test
  void testPlayerStatistics() {
    mockUrlWithFile(
        "/api/buildabet/playerStatistics",
        "playerStatistics.json",
        Parameter.param("id", "2"),
        Parameter.param("obEventId", "6167221"));

    this.webTestClient
        .get()
        .uri("/api/v1/player-statistics?obEventId=6167221&playerId=2")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "playerStatistics",
                responseFields()
                    .andWithPrefix(
                        "data[].",
                        fieldWithPath("id").description("Statistic id"),
                        fieldWithPath("title").description("Statistic title")),
                requestParameters(
                    parameterWithName("obEventId").description("OpenBet Event Id"),
                    parameterWithName("playerId").description("Player id"))));
  }

  @Test
  void testStatisticValueRange() {
    mockUrlWithFile(
        "/api/buildabet/statisticValueRange",
        "statisticValueRange.json",
        Parameter.param("statId", "2"),
        Parameter.param("obEventId", "6167221"),
        Parameter.param("playerId", "3"));

    this.webTestClient
        .get()
        .uri("/api/v1/statistic-value-range?obEventId=6167221&statId=2&playerId=3")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "statisticValueRange",
                responseFields(
                    fieldWithPath("data.minValue").description("Minimum value for statistic"),
                    fieldWithPath("data.maxValue").description("Maximum value for statistic"),
                    fieldWithPath("data.average").description("Average value for statistic")),
                requestParameters(
                    parameterWithName("obEventId").description("OpenBet Event id"),
                    parameterWithName("playerId").description("Player id in banach system"),
                    parameterWithName("statId").description("Statistic id in banach system"))));
  }

  @Test
  void testPlayerStatsByOptaId() {
    mockUrlWithFile(
        "/api/buildabet/playerByOptaId",
        "playerStatisticsByOptaId.json",
        Parameter.param("obEventId", "72134"),
        Parameter.param("optaPlayerId", "23"));

    this.webTestClient
        .get()
        .uri("/api/v1/player-stats-by-opta-id?obEventId=72134&optaPlayerId=23")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .consumeWith(
            document(
                "playerStatsByOptaId",
                responseFields(
                        fieldWithPath("data.id").description("id of the player"),
                        fieldWithPath("data.optaId").description("optaId of that player"))
                    .andWithPrefix("data.stats.", playerStatsByOpta()),
                requestParameters(
                    parameterWithName("obEventId").description("Open bet event Id"),
                    parameterWithName("optaPlayerId").description("opta player id"))));
  }

  // if url is matched - returns contents of file in the body
  private void mockUrlWithFile(String url, String jsonFile, Parameter... parameters) {
    mockServerClient
        .when(HttpRequest.request(url).withQueryStringParameters(parameters))
        .respond(
            HttpResponse.response()
                .withHeader("Content-Type", "application/json")
                .withBody(fromFile(jsonFile)));
  }

  private void mockEvents() {
    mockServerClient
        .when(HttpRequest.request("/api/buildabet/events").withMethod("POST"))
        .respond(
            HttpResponse.response()
                .withHeader("Content-Type", "application/json")
                .withBody(fromFile("events.json")));
  }

  private void mockPrice() {
    mockServerClient
        .when(HttpRequest.request("/api/buildabet/price").withMethod("POST"))
        .respond(
            HttpResponse.response()
                .withHeader("Content-Type", "application/json")
                .withBody(fromFile("price.json")));
  }

  private void mockSelection() {
    mockServerClient
        .when(HttpRequest.request("/api/buildabet/selections").withMethod("POST"))
        .respond(
            HttpResponse.response()
                .withHeader("Content-Type", "application/json")
                .withBody(fromFile("selection.json")));
  }

  private void mockEventByLeagueId() {
    mockServerClient
        .when(HttpRequest.request("/api/buildabet/events").withMethod("POST"))
        .respond(
            HttpResponse.response()
                .withHeader("Content-Type", "application/json")
                .withBody(fromFile("eventsByLeagueId.json")));
  }

  @SneakyThrows
  private static JsonBody fromFile(String jsonFile) {
    return JsonBody.json(
        new String(
            Files.readAllBytes(
                Paths.get(ClassLoader.getSystemResource("__files/" + jsonFile).toURI()))));
  }

  private ResponseFieldsSnippet eventsResponse() {
    return responseFields()
        .andWithPrefix("data[].", Arrays.asList(obTypeId(), obSportId(), obEventId()))
        .andWithPrefix("data[].", eventFieldDescription());
  }

  private ResponseFieldsSnippet eventResponse() {
    return responseFields()
        .andWithPrefix("data.", eventFieldDescription())
        .andWithPrefix("data.", Arrays.asList(obTypeId(), obSportId(), obEventId()));
  }

  private FieldDescriptor[] eventFieldDescription() {
    return new FieldDescriptor[] {
      fieldWithPath("title").description("Event's name"),
      fieldWithPath("date").description("Event's start date"),
      fieldWithPath("homeTeam.abbreviation").description("abbr"),
      fieldWithPath("homeTeam.title").description("Home team name"),
      fieldWithPath("homeTeam.id").description("Home team id"),
      fieldWithPath("homeTeam").description("Home team"),
      statusField(),
      fieldWithPath("visitingTeam.abbreviation").description("abbr"),
      fieldWithPath("visitingTeam.title").description("Visiting team name"),
      fieldWithPath("visitingTeam.id").description("Visiting team id"),
      fieldWithPath("visitingTeam").description("Visiting team"),
      fieldWithPath("hasPlayerProps").description("Has Players' market")
    };
  }

  private FieldDescriptor[] marketFieldDescription() {
    return new FieldDescriptor[] {
      fieldWithPath("id").description("Market Id"),
      fieldWithPath("title").description("Market Title"),
      fieldWithPath("status").description("Status"),
      fieldWithPath("groupName").description("Market Group name")
    };
  }

  private FieldDescriptor[] teamFieldDescription() {
    return new FieldDescriptor[] {
      fieldWithPath("id").description("Team name"),
      fieldWithPath("title").description("Team id"),
      fieldWithPath("abbreviation").description("Team name abbreviation")
    };
  }

  private FieldDescriptor[] playerStatsByOpta() {
    return new FieldDescriptor[] {
      fieldWithPath("Booking").description("booking"),
      fieldWithPath("Score").description("score"),
      fieldWithPath("Passes").description("passes"),
      fieldWithPath("Tackles").description("tackles"),
      fieldWithPath("Shots").description("shots"),
      fieldWithPath("ShotsOnTarget").description("shotsOnTarget"),
      fieldWithPath("ShotsOutsideBox").description("shotsOutsideBox"),
      fieldWithPath("Assists").description("assists"),
      fieldWithPath("Offsides").description("offsides"),
      fieldWithPath("GoalsInsideBox").description("goalsInsideBox"),
      fieldWithPath("GoalsOutsideBox").description("goalsOutsideBox"),
      fieldWithPath("ShotsWoodwork").description("shotsWoodWork")
    };
  }

  private FieldDescriptor statusField() {
    return fieldWithPath("status").description("Status: 0 - inactive, 1 - active, 2 - inplay");
  }

  private FieldDescriptor obTypeId() {
    return fieldWithPath("obTypeId").description("OpenBet Type Id");
  }

  private FieldDescriptor obSportId() {
    return fieldWithPath("obSportId").description("OpenBet Sport Id");
  }

  private FieldDescriptor obEventId() {
    return fieldWithPath("obEventId").description("OpenBet Event Id");
  }
}
