package com.entain.oxygen.betbuilder_middleware.api;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

import com.entain.oxygen.betbuilder_middleware.BetbuilderMiddlewareApplication;
import com.entain.oxygen.betbuilder_middleware.api.request.CheckPriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.request.PriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.response.CheckPriceResponse;
import com.entain.oxygen.betbuilder_middleware.bpg.client.PricingGatewayClient;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceRequest;
import com.entain.oxygen.betbuilder_middleware.exception.PGConnectivityException;
import com.entain.oxygen.betbuilder_middleware.exception.PricingGatewayException;
import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.redis.dto.SelectionDto;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonCombinationRepository;
import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import com.entain.oxygen.betbuilder_middleware.service.PriceService;
import com.google.gson.*;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.*;
import java.util.function.Function;
import org.jboss.logging.MDC;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.client.RedisException;
import org.redisson.config.Config;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import redis.embedded.RedisServer;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class PriceApiTest {
  @Autowired private WebTestClient webTestClient;
  @Mock private PriceService priceService;
  @Mock private PricingGatewayClient pricingClient;
  @Mock private ServerHttpResponse response;

  @MockBean(name = "pricingGatewayWebClient")
  protected WebClient pricingGatewayWebClient;

  @MockBean RedissonCombinationRepository combinationRedisConfig;
  private static RedisServer redisServer;
  private static RedissonClient redissonClient;

  @Value("${local.server.port}")
  private int port;

  @BeforeAll
  public static void setUp() {
    redisServer = new RedisServer(6379);
    redisServer.start();

    Config config = new Config();
    config.useSingleServer().setAddress("redis://localhost:6379");
    redissonClient = Redisson.create(config);
  }

  @AfterAll
  public static void tearDown() {
    redisServer.stop();
    redissonClient.shutdown();
  }

  @Test
  void successfulTest() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();

    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/SuccessfulRequest.json"),
                priceRequestType);

    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json"),
        pricingGatewayWebClient);

    webTestClient
        .post()
        .uri("/price")
        .header("X-Correlation-Id", "correlation")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("$.prices[0].sgpId")
        .isEqualTo(
            "1|a3f7d05c209597170bd582c206c5ad469f9bf5095b1a5c3cf7e0384564483f03bcc73dad03482a4aacbb2e2b084102077f0557b427f8b7543cefbfbf10a69d21")
        .jsonPath("$.prices[0].status")
        .isEqualTo(1)
        .consumeWith(
            result -> {
              assertNull(MDC.get(BBUtil.CORRELATION_ID));
            });
  }

  @Test
  void successfulTestWithNullOeid() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();

    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/SuccessfulRequestNullOeId.json"),
                priceRequestType);

    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json"),
        pricingGatewayWebClient);

    webTestClient
        .post()
        .uri("/price")
        .header("X-Correlation-Id", "correlation")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void successfulTestWithDiffIds() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();

    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/SuccessfulRequest.json"),
                priceRequestType);

    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse(
            "pricingGateway/SuccessResponseWithNullCombinationId.json"),
        pricingGatewayWebClient);

    webTestClient
        .post()
        .uri("/price")
        .header("X-Correlation-Id", "correlation")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void testNullSuspFromPG() {
    Type checkPriceRequestType = new TypeToken<CheckPriceRequest>() {}.getType();

    Set<String> keys = new HashSet<>();
    keys.add("5385F5B955C591AEE6C78544188784F98BABAB9BC09D769AA94C6D6BC26F9F90");

    Mockito.when(combinationRedisConfig.getCombinations(keys))
        .thenReturn(Mono.just(NullSuspResponseFromRedis()));

    CheckPriceRequest checkPriceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/NullSuspFromPGRequest.json"),
                checkPriceRequestType);

    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/NullSuspFromPGResponse.json"),
        pricingGatewayWebClient);

    webTestClient
        .post()
        .uri("/checkPrice")
        .header("X-Correlation-Id", "correlation")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(checkPriceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void testNotNullSuspFromPG() {
    Type checkPriceRequestType = new TypeToken<CheckPriceRequest>() {}.getType();

    Set<String> keys = new HashSet<>();
    keys.add("5385F5B955C591AEE6C78544188784F98BABAB9BC09D769AA94C6D6BC26F9F90");

    Mockito.when(combinationRedisConfig.getCombinations(keys))
        .thenReturn(Mono.just(NullSuspResponseFromRedis()));

    CheckPriceRequest checkPriceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/NullSuspFromPGRequest.json"),
                checkPriceRequestType);

    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/NotNullSuspFromPGResponse.json"),
        pricingGatewayWebClient);

    webTestClient
        .post()
        .uri("/checkPrice")
        .header("X-Correlation-Id", "correlation")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(checkPriceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void testActuatorHealth() {
    webTestClient = WebTestClient.bindToServer().baseUrl("http://localhost:" + port).build();
    System.out.println("Port num is: " + port);
    webTestClient
        .get()
        .uri("/actuator/health")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody()
        .jsonPath("$.status")
        .isEqualTo("UP"); // Assuming UP status indicates a healthy state
  }

  private Map<String, CombinationCache> NullSuspResponseFromRedis() {
    Map<String, CombinationCache> map = new HashMap<>();

    SelectionDto sel = new SelectionDto();
    sel.setFixtureId("2:19511025");
    sel.setMarketId(43491639L);
    sel.setOptionId(292541083L);

    SelectionDto sel1 = new SelectionDto();
    sel1.setFixtureId("2:19511025");
    sel1.setMarketId(43536626L);
    sel1.setOptionId(292820673L);

    List<SelectionDto> selList = new ArrayList<>();

    CombinationCache combinationCache = new CombinationCache();
    combinationCache.setHash("5385F5B955C591AEE6C78544188784F98BABAB9BC09D769AA94C6D6BC26F9F90");
    combinationCache.setId("70e36e8e-dc81-59b2-a2d3-e5c2eca04baf----2:19511025");
    combinationCache.setSportId(4);
    combinationCache.setOEId("14815992");
    combinationCache.setSelections(selList);
    map.put("5385F5B955C591AEE6C78544188784F98BABAB9BC09D769AA94C6D6BC26F9F90", combinationCache);

    return map;
  }

  @Test
  void testGetPriceWithError() {
    WebClient.RequestHeadersSpec requestHeadersSpec =
        Mockito.mock(WebClient.RequestHeadersSpec.class);
    WebClient.RequestBodyUriSpec requestBodyUriSpec =
        Mockito.mock(WebClient.RequestBodyUriSpec.class);
    WebClient.RequestBodySpec requestBodySpec = Mockito.mock(WebClient.RequestBodySpec.class);

    Mockito.when(requestBodyUriSpec.contentType(MediaType.APPLICATION_JSON))
        .thenReturn(requestBodySpec);
    Mockito.when(requestBodySpec.accept(new MediaType[] {MediaType.APPLICATION_JSON}))
        .thenReturn(requestBodySpec);
    Mockito.when(pricingGatewayWebClient.post()).thenReturn(requestBodyUriSpec);
    Mockito.when(requestBodySpec.body(Mockito.any(), Mockito.any(Class.class)))
        .thenReturn(requestHeadersSpec);
    Mockito.when(requestHeadersSpec.header(Mockito.any(), Mockito.any()))
        .thenReturn(requestHeadersSpec);
    Mockito.when(requestBodySpec.body(Mockito.any())).thenReturn(requestHeadersSpec);
    Mockito.when(requestHeadersSpec.exchangeToMono(Mockito.any(Function.class)))
        .thenReturn(Mono.error(new RuntimeException("Simulated RuntimeException")));

    webTestClient
        .post()
        .uri("/price")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(new PriceRequest())
        .exchange()
        .expectStatus()
        .is5xxServerError();
  }

  @ParameterizedTest
  @CsvSource({
    "pricingGateway/CheckPriceSuccessRequest.json, pricingGateway/OddsNull.json, pricingGateway/Combination.json",
    "pricingGateway/CheckPriceSuccessRequest.json, pricingGateway/FractionalNull.json, pricingGateway/Combination.json",
    "pricingGateway/CheckPriceSuccessRequest.json, pricingGateway/SuccessfulResponse.json, pricingGateway/Combination.json",
    "pricingGateway/CheckPriceSuccessValidHashRequest.json, pricingGateway/SuccessfulResponse.json, pricingGateway/Combination.json",
    "pricingGateway/CheckPriceSuccessRequest.json, pricingGateway/SuccessfulWithNullSgpIdResponse.json, pricingGateway/Combination.json",
    "pricingGateway/CheckPriceSuccessRequest.json, pricingGateway/SuccessfulWithNullSgpIdResponse.json, pricingGateway/CombinationDifferentId.json",
    "pricingGateway/CheckPriceSuccessRequest.json, pricingGateway/SuccessfulResponseWithSuspendedState.json, pricingGateway/Combination.json"
  })
  void checkPriceSuccessTest(String req, String resp, String combination) {
    Type checkPriceType = new TypeToken<CheckPriceRequest>() {}.getType();
    CheckPriceRequest request =
        new Gson().fromJson(TestUtil.getResourceByPath(req), checkPriceType);
    Map<String, CombinationCache> combinationMap = getCombimap(combination);
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.just(combinationMap));
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse(resp), pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void successfulTestWithEmptySelections() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();
    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/SuccessfulRequest.json"),
                priceRequestType);
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json"),
        pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/price")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void onRedisExceptionTest() {
    Type priceRequestType = new TypeToken<CheckPriceRequest>() {}.getType();
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.error(new RedisException()));
    CheckPriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                priceRequestType);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody();
  }

  @Test
  void checkPriceExceptionTest() {
    Type priceRequestType = new TypeToken<CheckPriceRequest>() {}.getType();
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.error(new PGConnectivityException("Exception occured..")));
    CheckPriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                priceRequestType);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody();
  }

  @Test
  void checkPriceIllegalArgmentExceptionTest() {
    Type priceRequestType = new TypeToken<CheckPriceRequest>() {}.getType();
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.error(new IllegalArgumentException("Exception occured..")));
    CheckPriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                priceRequestType);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody();
  }

  @Test
  void checkPricingGatewayExceptionTest() {
    Type priceRequestType = new TypeToken<CheckPriceRequest>() {}.getType();
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.error(new PricingGatewayException("Exception occured..")));
    CheckPriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                priceRequestType);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody();
  }

  @Test
  void unknownAngstromTest() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();
    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/UnknownAngstromErrorRequest.json"),
                priceRequestType);
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse(
            "pricingGateway/UnknownAngstromErrorResponse.json"),
        pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/price")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void emptyEventIdTest() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();
    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/EmptyFixtureIdRequest.json"),
                priceRequestType);
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/EmptyFixtureIdResponse.json"),
        pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/price")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("$.prices[0].errorCode")
        .isEqualTo(2004)
        .jsonPath("$.prices[0].status")
        .isEqualTo(2)
        .jsonPath("$.prices[0].errorMessage")
        .isEqualTo(
            "FixtureId expects a specific format: x:nnn (where x is a single domain digit 1=TV1, 2=TV2 and nnn is a positive number) or nnn (where nnn is a number to be treated as TV1). Value passed for selection index 0 was : ");
  }

  @Test
  void checkPriceCombinationNull() {
    Type checkPriceType = new TypeToken<CheckPriceRequest>() {}.getType();
    CheckPriceRequest request =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                checkPriceType);
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any())).thenReturn(null);
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json"),
        pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody();
  }

  @Test
  void checkPriceNullCombinationTest() {
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any())).thenReturn(null);
    CheckPriceRequest request = new CheckPriceRequest();
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody();
  }

  @Test
  void checkPriceNotNullAndEmptyCombinationTest() {
    Type checkPriceType = new TypeToken<CheckPriceRequest>() {}.getType();
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.just(Collections.emptyMap()));
    CheckPriceRequest request =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                checkPriceType);
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json"),
        pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  @Test
  void checkPriceInvalidHashesTest() {
    Type checkPriceType = new TypeToken<CheckPriceRequest>() {}.getType();
    CheckPriceRequest request =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                checkPriceType);
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any())).thenReturn(null);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody();
  }

  @Test
  void checkPriceInvalidHashes2Test() {
    Type checkPriceType = new TypeToken<CheckPriceRequest>() {}.getType();
    Type checkPriceResponseType = new TypeToken<CheckPriceResponse>() {}.getType();
    CheckPriceRequest request =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/CheckPriceSuccessRequest.json"),
                checkPriceType);
    CheckPriceResponse checkPriceResponse =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath(
                    "pricingGateway/CheckPriceFilterUnmatchedHashResponse.json"),
                checkPriceResponseType);
    Map<String, CombinationCache> combinationMap = getCombimap("pricingGateway/Combination.json");
    Mockito.when(combinationRedisConfig.getCombinations(Mockito.any()))
        .thenReturn(Mono.just(combinationMap));
    Mockito.when(priceService.getLatestPrices(Mockito.any()))
        .thenReturn(Mono.just(checkPriceResponse));
    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json"),
        pricingGatewayWebClient);
    webTestClient
        .post()
        .uri("/checkPrice")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody();
  }

  public Map<String, CombinationCache> getCombimap(String filePath) {
    String jsonContent = TestUtil.getResourceByPath(filePath);
    JsonObject jsonObject = JsonParser.parseString(jsonContent).getAsJsonObject();
    JsonArray combinationsArray = jsonObject.getAsJsonArray("combinations");
    List<CombinationCache> combinationsCache = new ArrayList<>();
    for (JsonElement element : combinationsArray) {
      CombinationCache combinationCache = new Gson().fromJson(element, CombinationCache.class);
      combinationsCache.add(combinationCache);
    }
    Map<String, CombinationCache> combiMap = new HashMap<>();
    for (CombinationCache combinationCache : combinationsCache) {
      combiMap.put(combinationCache.getHash(), combinationCache);
    }
    return combiMap;
  }

  @Test
  void priceTest() {
    Type priceRequestType = new TypeToken<PriceRequest>() {}.getType();

    PriceRequest priceRequests =
        new Gson()
            .fromJson(
                TestUtil.getResourceByPath("pricingGateway/SuccessfulRequest.json"),
                priceRequestType);

    TestUtil.mockWebServer(
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse_sgpId.json"),
        pricingGatewayWebClient);

    webTestClient
        .post()
        .uri("/price")
        .header("X-Correlation-Id", "correlation")
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(priceRequests)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("$.prices[0].status")
        .isEqualTo(1)
        .consumeWith(
            result -> {
              assertNull(MDC.get(BBUtil.CORRELATION_ID));
            });
  }

  @Test
  void testBPGPriceRequest() {
    BPGPriceRequest bpgPriceRequest = new BPGPriceRequest();
    bpgPriceRequest.setBatchId("abc");
    bpgPriceRequest.setCombinations(new ArrayList<>());
    assertNotNull(bpgPriceRequest.getCombinations());
  }

  @Test
  void contextLoads() {
    BetbuilderMiddlewareApplication.main(new String[] {});
    Assertions.assertNotNull(BetbuilderMiddlewareApplication.class);
  }
}
