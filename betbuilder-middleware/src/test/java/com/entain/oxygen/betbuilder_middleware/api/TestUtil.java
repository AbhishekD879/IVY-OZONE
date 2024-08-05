package com.entain.oxygen.betbuilder_middleware.api;

import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.SneakyThrows;
import org.mockito.Mockito;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

public class TestUtil {
  @SneakyThrows(Exception.class)
  public static String getResourceByPath(String filePath) {
    return Files.lines(Paths.get(ClassLoader.getSystemResource(filePath).toURI()))
        .collect(Collectors.joining(" "));
  }

  public static BPGPriceResponse getResourceByPathToPriceResponse(String filePath) {
    try {
      ObjectMapper objectMapper = new ObjectMapper();
      String fileContent =
          Files.lines(Paths.get(ClassLoader.getSystemResource(filePath).toURI()))
              .collect(Collectors.joining(" "));
      return objectMapper.readValue(fileContent, BPGPriceResponse.class);
    } catch (IOException | URISyntaxException e) {
      throw new RuntimeException("Error reading resource file ", e);
    }
  }

  protected static void mockWebServer(BPGPriceResponse response, WebClient webClient) {

    WebClient.RequestHeadersSpec requestHeadersSpec =
        Mockito.mock(WebClient.RequestHeadersSpec.class);

    WebClient.RequestBodySpec requestBodySpec = Mockito.mock(WebClient.RequestBodySpec.class);
    WebClient.RequestBodyUriSpec requestBodyUriSpec =
        Mockito.mock(WebClient.RequestBodyUriSpec.class);

    WebClient.ResponseSpec responseMock = Mockito.mock(WebClient.ResponseSpec.class);

    Mockito.when(webClient.post()).thenReturn(requestBodyUriSpec);

    Mockito.when(requestBodyUriSpec.uri(Mockito.any(Function.class))).thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.contentType(MediaType.APPLICATION_JSON))
        .thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.accept(MediaType.APPLICATION_JSON)).thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.body(Mockito.any(), Mockito.any(Class.class)))
        .thenReturn(requestHeadersSpec);

    Mockito.when(requestHeadersSpec.header(Mockito.any(), Mockito.any()))
        .thenReturn(requestHeadersSpec);

    Mockito.when(requestHeadersSpec.exchangeToMono(Mockito.any(Function.class)))
        .thenReturn(Mono.just(response));
    Mockito.when(responseMock.bodyToMono(BPGPriceResponse.class)).thenReturn(Mono.just(response));
  }

  public static void mockClient_doOnError(WebClient webClient) {
    WebClient.RequestHeadersSpec requestHeadersSpec =
        Mockito.mock(WebClient.RequestHeadersSpec.class);

    WebClient.RequestBodySpec requestBodySpec = Mockito.mock(WebClient.RequestBodySpec.class);
    WebClient.RequestBodyUriSpec requestBodyUriSpec =
        Mockito.mock(WebClient.RequestBodyUriSpec.class);
    Mockito.when(webClient.post()).thenReturn(requestBodyUriSpec);

    Mockito.when(requestBodyUriSpec.uri(Mockito.any(Function.class))).thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.contentType(MediaType.APPLICATION_JSON))
        .thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.accept(MediaType.APPLICATION_JSON)).thenReturn(requestBodySpec);

    Mockito.when(requestBodySpec.body(Mockito.any(), Mockito.any(Class.class)))
        .thenReturn(requestHeadersSpec);

    Mockito.when(requestHeadersSpec.header(Mockito.any(), Mockito.any()))
        .thenReturn(requestHeadersSpec);
    Mockito.when(requestHeadersSpec.exchangeToMono(Mockito.any()))
        .thenReturn(Mono.error(new RuntimeException("Simulated error")));
  }
}
