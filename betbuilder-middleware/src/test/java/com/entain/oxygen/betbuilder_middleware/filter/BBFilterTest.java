package com.entain.oxygen.betbuilder_middleware.filter;

import static org.mockito.Mockito.*;

import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import org.jboss.logging.MDC;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpHeaders;
import org.springframework.http.server.RequestPath;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class BBFilterTest {
  @InjectMocks private BBFilter bbFilter;

  @Mock private ServerWebExchange exchange;

  @Mock private WebFilterChain webFilterChain;

  @Mock private ServerHttpRequest request;

  @Mock private ServerHttpResponse response;

  private HttpHeaders requestHeaders;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.openMocks(this);

    request = mock(ServerHttpRequest.class);

    String path = "/price";
    RequestPath requestPath = mock(RequestPath.class);
    when(requestPath.value()).thenReturn(path);
    when(request.getPath()).thenReturn(requestPath);

    requestHeaders = new HttpHeaders();
    requestHeaders.add(BBUtil.X_CORRELATION_ID, "test-correlation-id");
    when(request.getHeaders()).thenReturn(requestHeaders);
    when(exchange.getRequest()).thenReturn(request);
    when(exchange.getResponse()).thenReturn(response);
    when(response.getHeaders()).thenReturn(new HttpHeaders());
    when(webFilterChain.filter(any())).thenReturn(Mono.empty());
  }

  @Test
  void filterTest() {
    Mono<Void> result = bbFilter.filter(exchange, webFilterChain);

    StepVerifier.create(result).expectComplete().verify();

    MDC.put(BBUtil.CORRELATION_ID, "test-correlation-id");

    Assertions.assertNotNull(result);

    MDC.clear();
  }
}
