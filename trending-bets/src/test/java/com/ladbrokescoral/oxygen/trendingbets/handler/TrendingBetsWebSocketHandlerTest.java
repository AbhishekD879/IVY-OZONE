package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingBetsDto;
import java.net.URI;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.Assert;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.client.ReactorNettyWebSocketClient;
import org.springframework.web.reactive.socket.client.WebSocketClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RunWith(SpringRunner.class)
@DirtiesContext
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.DEFINED_PORT)
@ActiveProfiles("TEST")
public class TrendingBetsWebSocketHandlerTest {

  private static final Duration TIMEOUT = Duration.ofMillis(10000);
  WebSocketClient client = new ReactorNettyWebSocketClient();
  URI uri = URI.create("ws://localhost:8099/trendingbets");

  @BeforeAll
  public static void setup() {
    TrendingBetsContext.getTrendingBets()
        .put("football_tb_12h_1h", TrendingBetsDto.builder().build());
  }

  private List<String> webSocketRequest(String... payload) {
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    Flux<String> input = Flux.fromArray(payload);
    client
        .execute(
            uri,
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(session.receive().take(1).map(WebSocketMessage::getPayloadAsText))
                    .collectList()
                    .doOnNext(actualRef::set)
                    .doOnNext(System.out::println)
                    .then())
        .block(TIMEOUT);

    return actualRef.get();
  }

  public void testWithArguments(String... args) {
    List<String> actualRef = webSocketRequest(args);
    Assert.assertNotNull(actualRef);
    Assert.assertEquals(1, actualRef.size());
  }

  @ParameterizedTest
  @ValueSource(
      strings = {
        "2",
        "41",
        "[\"subscribe\", \"football_tb_12h_1h\"]",
        "[\"subscribe\", \"football_tb_48h_48h\"]",
        "[\"subscribe\"]",
        "[\"invalid\", null]",
        "subscribe"
      })
  void testWithRequest(String args) {
    testWithArguments(args);
  }

  @Test
  void testTimeout() throws InterruptedException {
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    CountDownLatch latch = new CountDownLatch(1);
    Flux<String> input = Flux.interval(Duration.ofSeconds(62)).map(index -> "41");
    client
        .execute(
            uri,
            session ->
                session
                    .send(input.map(session::textMessage))
                    .timeout(Duration.ofSeconds(61), Mono.empty())
                    .thenMany(session.receive().take(1).map(WebSocketMessage::getPayloadAsText))
                    .collectList()
                    .doOnNext(actualRef::set)
                    .doOnNext(System.out::println)
                    .then())
        .subscribe();
    latch.await(62, TimeUnit.SECONDS);
    Assert.assertNotNull(actualRef.get());
  }
}
