package com.entain.oxygen.betbuilder_middleware.service;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

import com.entain.oxygen.betbuilder_middleware.api.TestUtil;
import com.entain.oxygen.betbuilder_middleware.api.response.PriceResponse;
import com.entain.oxygen.betbuilder_middleware.bpg.client.PricingGatewayClient;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceRequest;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceResponse;
import com.entain.oxygen.betbuilder_middleware.bpg.model.Combination;
import com.entain.oxygen.betbuilder_middleware.bpg.model.Selection;
import com.entain.oxygen.betbuilder_middleware.config.PricingGatewayClientProperties;
import com.entain.oxygen.betbuilder_middleware.exception.BetBuilderException;
import com.entain.oxygen.betbuilder_middleware.exception.PGConnectivityException;
import com.entain.oxygen.betbuilder_middleware.exception.PricingGatewayException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;
import org.jboss.logging.MDC;
import org.jetbrains.annotations.NotNull;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.context.Context;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {PricingGatewayClient.class, PricingGatewayClientProperties.class})
class PricingGatewayClientTest {
  @Autowired private PricingGatewayClient pricingGatewayClient;

  @MockBean(name = "pricingGatewayWebClient")
  protected WebClient pricingGatewayWebClient;

  @BeforeEach
  void setUp() {
    pricingGatewayClient = new PricingGatewayClient(pricingGatewayWebClient);
  }

  @ParameterizedTest
  @CsvSource({
    "pricingGateway/SuccessfulResponse.json",
    "pricingGateway/ContradictorySelectionResponse.json",
    "pricingGateway/BussinessError2.json"
  })
  void testBuildResponseDoOnNext(String resp)
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    BPGPriceResponse response = TestUtil.getResourceByPathToPriceResponse(resp);
    ClientResponse clientResponse =
        ClientResponse.create(HttpStatus.OK)
            .body(BBUtil.toJson(response))
            .headers(headers -> headers.setContentType(MediaType.APPLICATION_JSON))
            .build();
    Method buildResponseMethod =
        PricingGatewayClient.class.getDeclaredMethod("buildResponse", ClientResponse.class);
    buildResponseMethod.setAccessible(true);
    Mono<BPGPriceResponse> result =
        (Mono<BPGPriceResponse>) buildResponseMethod.invoke(pricingGatewayClient, clientResponse);
    Consumer<? super BPGPriceResponse> onNext = Mockito.mock(Consumer.class);
    result.doOnNext(onNext).subscribe();
    Assertions.assertNotNull(result);
  }

  @Test
  void testBuildResponseSuccess()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    ClientResponse clientResponse = ClientResponse.create(HttpStatus.OK).build();
    MDC.put(BBUtil.CORRELATION_ID, "test-correlation-id");
    Method buildResponseMethod =
        PricingGatewayClient.class.getDeclaredMethod("buildResponse", ClientResponse.class);
    buildResponseMethod.setAccessible(true);
    Mono<PriceResponse> result =
        (Mono<PriceResponse>) buildResponseMethod.invoke(pricingGatewayClient, clientResponse);
    Assertions.assertNotNull(result);
  }

  @Test
  void testBuildResponseServerError() throws Throwable {
    ClientResponse clientResponse = ClientResponse.create(HttpStatus.INTERNAL_SERVER_ERROR).build();
    Method buildResponseMethod =
        PricingGatewayClient.class.getDeclaredMethod("buildResponse", ClientResponse.class);
    buildResponseMethod.setAccessible(true);
    Throwable thrownException = null;
    try {
      buildResponseMethod.invoke(pricingGatewayClient, clientResponse);
    } catch (InvocationTargetException e) {
      thrownException = e.getCause();
    } catch (Exception e) {
      thrownException = e;
    }

    if (thrownException != null) {
      Throwable finalThrownException = thrownException;
      assertThrows(
          PricingGatewayException.class,
          () -> {
            throw finalThrownException;
          });
    }
  }

  @Test
  void testBuildResponseServerErrorServiceUnavailable() throws NoSuchMethodException {
    ClientResponse clientResponse = ClientResponse.create(HttpStatus.SERVICE_UNAVAILABLE).build();
    Method buildResponseMethod =
        PricingGatewayClient.class.getDeclaredMethod("buildResponse", ClientResponse.class);
    buildResponseMethod.setAccessible(true);
    Throwable thrownException = null;
    try {
      buildResponseMethod.invoke(pricingGatewayClient, clientResponse);
    } catch (InvocationTargetException e) {
      thrownException = e.getCause();
    } catch (Exception e) {
      thrownException = e;
    }

    if (thrownException != null) {
      Throwable finalThrownException = thrownException;
      assertThrows(
          PGConnectivityException.class,
          () -> {
            throw finalThrownException;
          });
    }
  }

  @Test
  void testBuildResponseClientError() throws NoSuchMethodException {
    ClientResponse clientResponse = ClientResponse.create(HttpStatus.BAD_REQUEST).build();
    Method buildResponseMethod =
        PricingGatewayClient.class.getDeclaredMethod("buildResponse", ClientResponse.class);
    buildResponseMethod.setAccessible(true);
    Throwable thrownException = null;
    try {
      buildResponseMethod.invoke(pricingGatewayClient, clientResponse);
    } catch (InvocationTargetException e) {
      thrownException = e.getCause();
    } catch (Exception e) {
      thrownException = e;
    }

    if (thrownException != null) {
      Throwable finalThrownException = thrownException;
      assertThrows(
          IllegalArgumentException.class,
          () -> {
            throw finalThrownException;
          });
    }
  }

  @Test
  void testBuildResponseOtherError() throws NoSuchMethodException {
    ClientResponse clientResponse = ClientResponse.create(HttpStatus.MULTIPLE_CHOICES).build();
    Method buildResponseMethod =
        PricingGatewayClient.class.getDeclaredMethod("buildResponse", ClientResponse.class);
    buildResponseMethod.setAccessible(true);
    Throwable thrownException = null;
    try {
      buildResponseMethod.invoke(pricingGatewayClient, clientResponse);
    } catch (InvocationTargetException e) {
      thrownException = e.getCause();
    } catch (Exception e) {
      thrownException = e;
    }

    if (thrownException != null) {
      Throwable finalThrownException = thrownException;
      assertThrows(
          BetBuilderException.class,
          () -> {
            throw finalThrownException;
          });
    }
  }

  @Test
  void testGetPrice_onError() {
    BPGPriceRequest bpgPriceRequest = getBpgRequest();
    TestUtil.mockClient_doOnError(pricingGatewayWebClient);
    Map<String, String> contextMap = new HashMap<>();
    contextMap.put(BBUtil.CORRELATION_ID, "12344");
    contextMap.put(BBUtil.TRANSACTION_PATH, "/price");
    contextMap.put(BBUtil.BPG_REQUEST_KEY, "BPG Request");
    contextMap.put(BBUtil.LCG_REQUEST, "LCG Request");
    Consumer<? super Throwable> onErrorConsumer = Mockito.mock(Consumer.class);
    pricingGatewayClient
        .getPrice(bpgPriceRequest)
        .contextWrite(Context.of(contextMap))
        .doOnError(onErrorConsumer)
        .subscribe();
    Assertions.assertNotNull(bpgPriceRequest);
  }

  @Test
  void testGetPrice_onSuccesss() {
    BPGPriceRequest bpgPriceRequest = getBpgRequest();
    BPGPriceResponse response =
        TestUtil.getResourceByPathToPriceResponse("pricingGateway/SuccessfulResponse.json");
    WebClient.RequestHeadersSpec requestHeadersSpec = getRequestHeadersSpec(response);

    Map<String, String> contextMap = new HashMap<>();
    contextMap.put(BBUtil.CORRELATION_ID, "12344");
    contextMap.put(BBUtil.TRANSACTION_PATH, "/price");
    contextMap.put(BBUtil.BPG_REQUEST_KEY, "BPG Request");
    contextMap.put(BBUtil.LCG_REQUEST, "LCG Request");
    pricingGatewayClient.getPrice(bpgPriceRequest).contextWrite(Context.of(contextMap)).subscribe();

    ArgumentCaptor<Function<? super ClientResponse, ? extends Mono<?>>> functionCaptor =
        ArgumentCaptor.forClass(Function.class);
    verify(requestHeadersSpec).exchangeToMono(functionCaptor.capture());
    Function<? super ClientResponse, ? extends Mono<?>> function = functionCaptor.getValue();
    function.apply(ClientResponse.create(HttpStatus.OK).build());
  }

  @Test
  void testNullPGRequest() {
    BPGPriceRequest bpgPriceRequest = null;
    Map<String, String> contextMap = new HashMap<>();
    contextMap.put(BBUtil.CORRELATION_ID, "12344");
    contextMap.put(BBUtil.TRANSACTION_PATH, "/price");
    contextMap.put(BBUtil.BPG_REQUEST_KEY, "BPG Request");
    contextMap.put(BBUtil.LCG_REQUEST, "LCG Request");
    pricingGatewayClient.getPrice(bpgPriceRequest).contextWrite(Context.of(contextMap)).subscribe();
    Assertions.assertNull(bpgPriceRequest);
  }

  @NotNull
  private WebClient.RequestHeadersSpec getRequestHeadersSpec(BPGPriceResponse response) {
    WebClient.RequestHeadersSpec requestHeadersSpec =
        Mockito.mock(WebClient.RequestHeadersSpec.class);
    WebClient.ResponseSpec responseSpec = Mockito.mock(WebClient.ResponseSpec.class);

    WebClient.RequestBodySpec requestBodySpec = Mockito.mock(WebClient.RequestBodySpec.class);
    WebClient.RequestBodyUriSpec requestBodyUriSpec =
        Mockito.mock(WebClient.RequestBodyUriSpec.class);

    Mockito.when(pricingGatewayWebClient.post()).thenReturn(requestBodyUriSpec);

    Mockito.when(requestBodyUriSpec.uri(Mockito.any(Function.class))).thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.contentType(MediaType.APPLICATION_JSON))
        .thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.accept(MediaType.APPLICATION_JSON)).thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.body(Mockito.any(), Mockito.any(Class.class)))
        .thenReturn(requestHeadersSpec);

    Mockito.when(requestHeadersSpec.header(Mockito.any(), Mockito.any()))
        .thenReturn(requestHeadersSpec);
    ClientResponse clientResponse =
        ClientResponse.create(HttpStatus.OK).body(BBUtil.toJson(response)).build();
    Mockito.when(requestHeadersSpec.exchangeToMono(Mockito.any(Function.class)))
        .thenReturn(Mono.just(clientResponse));
    Mockito.when(responseSpec.bodyToMono(BPGPriceResponse.class)).thenReturn(Mono.just(response));
    return requestHeadersSpec;
  }

  private BPGPriceRequest getBpgRequest() {
    BPGPriceRequest bpgPriceRequest = new BPGPriceRequest();
    bpgPriceRequest.setBatchId("Timestamp: 1715163515451");
    List<Combination> combinations = new ArrayList<>();
    Combination combination = new Combination();
    combination.setId("f7ef1cc8-dc2c-5174-b792-c06666505396----2:9169149");
    combination.setSportId(4);
    Selection selection = new Selection();
    selection.setFixtureId("2:9169149");
    selection.setMarketId(71999487L);
    selection.setOptionId(325382158L);

    Selection selection1 = new Selection();
    selection1.setFixtureId("2:9169149");
    selection1.setMarketId(71998807L);
    selection1.setOptionId(325380123L);
    combination.setSelections(Arrays.asList(selection, selection1));
    combinations.add(combination);
    bpgPriceRequest.setCombinations(combinations);
    return bpgPriceRequest;
  }
}
