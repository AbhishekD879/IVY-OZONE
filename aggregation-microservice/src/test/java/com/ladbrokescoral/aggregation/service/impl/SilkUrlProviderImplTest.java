package com.ladbrokescoral.aggregation.service.impl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.aggregation.configuration.ApiProperties;
import com.ladbrokescoral.aggregation.configuration.ApiProperties.DataFeed;
import com.ladbrokescoral.aggregation.exception.BadRequestException;
import com.ladbrokescoral.aggregation.model.Event;
import com.ladbrokescoral.aggregation.model.Horse;
import com.ladbrokescoral.aggregation.model.RaceInfo;
import com.ladbrokescoral.aggregation.model.SilkUrl;
import com.ladbrokescoral.aggregation.service.SilkUrlProviderService;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeoutException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.stubbing.Answer;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.ExchangeFunction;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClient.Builder;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
public class SilkUrlProviderImplTest {

  private SilkUrlProviderService silkUrlProvider;
  private ApiProperties properties;

  @BeforeEach
  public void setUp() throws Exception {
    properties = getProperties();
  }

  @Test
  public void getSilksUrlsByEventIds() {
    RaceInfo raceInfo = getRaceInfo();
    Builder builder = prepareMocks(raceInfo);

    silkUrlProvider = new SilkUrlProviderImpl(builder.build(), properties);

    Mono<List<SilkUrl>> coral =
        silkUrlProvider.getSilksUrlsByEventIds("coral", Arrays.asList("765894"));
    List<SilkUrl> silkUrls = coral.block();

    assertEquals(3, silkUrls.size());
    assertEquals("1", silkUrls.get(0).getSilkId());
    assertEquals("https://silkCoral1/1.gif", silkUrls.get(0).getEndpoint());
    assertEquals("3", silkUrls.get(1).getSilkId());
    assertEquals("https://silkCoral3/3.gif", silkUrls.get(1).getEndpoint());
    assertEquals("2", silkUrls.get(2).getSilkId());
    assertEquals("https://silkCoral2/2.gif", silkUrls.get(2).getEndpoint());
  }

  @Test
  public void getSilksUrlsByEventIdsLadbrokes() {
    RaceInfo raceInfo = getRaceInfo();
    Builder builder = prepareMocks(raceInfo);

    silkUrlProvider = new SilkUrlProviderImpl(builder.build(), properties);

    Mono<List<SilkUrl>> coral =
        silkUrlProvider.getSilksUrlsByEventIds("ladbrokes", Arrays.asList("765894"));
    List<SilkUrl> silkUrls = coral.block();

    assertEquals(3, silkUrls.size());
    assertEquals("1", silkUrls.get(0).getSilkId());
    assertEquals("https://silkLadbrokes1/1.gif", silkUrls.get(0).getEndpoint());
    assertEquals("3", silkUrls.get(1).getSilkId());
    assertEquals("https://silkLadbrokes3/3.gif", silkUrls.get(1).getEndpoint());
    assertEquals("2", silkUrls.get(2).getSilkId());
    assertEquals("https://silkLadbrokes2/2.gif", silkUrls.get(2).getEndpoint());
  }

  @Test
  public void getSilksUrlsByEventIdsError() {
    RaceInfo raceInfo = new RaceInfo();
    raceInfo.setError(true);
    raceInfo.setDocument(Collections.emptyMap());
    Builder builder = prepareMocks(raceInfo);

    silkUrlProvider = new SilkUrlProviderImpl(builder.build(), properties);

    Mono<List<SilkUrl>> coral =
        silkUrlProvider.getSilksUrlsByEventIds("coral", Arrays.asList("765894"));

    RuntimeException expectedException =
        assertThrows(
            RuntimeException.class,
            () -> {
              coral.block();
            });
    assertThat(expectedException).isNotNull();
  }

  @Test
  public void getSilksUrlsByEventIdsErrorTimeout() {
    ExchangeFunction exchangeFunction = mock(ExchangeFunction.class);
    when(exchangeFunction.exchange(any()))
        .thenAnswer((Answer<Mono<Long>>) invocation -> Mono.delay(Duration.ofSeconds(5)));

    WebClient builder = WebClient.builder().exchangeFunction(exchangeFunction).build();

    silkUrlProvider = new SilkUrlProviderImpl(builder, properties);

    Mono<List<SilkUrl>> coral =
        silkUrlProvider.getSilksUrlsByEventIds("coral", Arrays.asList("765894"));
    coral
        .onErrorResume(
            err -> {
              assertTrue(err instanceof TimeoutException);
              return Mono.empty();
            })
        .block();
  }

  @Test
  public void getSilksUrlsByEventIdsBRError() {
    RaceInfo raceInfo = new RaceInfo();
    raceInfo.setError(true);
    raceInfo.setErrorMessage("No such ID");
    raceInfo.setDocument(Collections.emptyMap());
    Builder builder = prepareMocks(raceInfo);

    silkUrlProvider = new SilkUrlProviderImpl(builder.build(), properties);

    Mono<List<SilkUrl>> coral =
        silkUrlProvider.getSilksUrlsByEventIds("coral", Arrays.asList("765894"));

    BadRequestException expectedException =
        assertThrows(
            BadRequestException.class,
            () -> {
              coral.block();
            });
    assertThat(expectedException).isNotNull();
  }

  @Test
  public void getSilksUrlsByMoreEventIds() {
    RaceInfo raceInfo = getRaceInfoWithTwoEvents();
    Builder builder = prepareMocks(raceInfo);

    silkUrlProvider = new SilkUrlProviderImpl(builder.build(), properties);

    Mono<List<SilkUrl>> coral =
        silkUrlProvider.getSilksUrlsByEventIds("coral", Arrays.asList("765894", "563628"));
    List<SilkUrl> silkUrls = coral.block();

    assertEquals(5, silkUrls.size());
    assertEquals("1", silkUrls.get(0).getSilkId());
    assertEquals("https://silkCoral1/1.gif", silkUrls.get(0).getEndpoint());
    assertEquals("3", silkUrls.get(1).getSilkId());
    assertEquals("https://silkCoral3/3.gif", silkUrls.get(1).getEndpoint());
    assertEquals("2", silkUrls.get(2).getSilkId());
    assertEquals("https://silkCoral2/2.gif", silkUrls.get(2).getEndpoint());
    assertEquals("5", silkUrls.get(3).getSilkId());
    assertEquals("https://silkCoral5/5.gif", silkUrls.get(3).getEndpoint());
    assertEquals("4", silkUrls.get(4).getSilkId());
    assertEquals("https://silkCoral4/4.gif", silkUrls.get(4).getEndpoint());
  }

  private Builder prepareMocks(RaceInfo raceInfo) {
    ClientResponse clientResponse = mock(ClientResponse.class);
    ExchangeFunction exchangeFunction = mock(ExchangeFunction.class);
    when(exchangeFunction.exchange(any())).thenReturn(Mono.just(clientResponse));
    when(clientResponse.bodyToMono(RaceInfo.class)).thenReturn(Mono.just(raceInfo));

    return WebClient.builder().exchangeFunction(exchangeFunction);
  }

  private RaceInfo getRaceInfo() {
    RaceInfo raceInfo = new RaceInfo();
    Event event = new Event();
    event.setHorses(getHorses());
    Map<String, Event> document = new HashMap<>();
    document.put("765894", event);
    raceInfo.setDocument(document);
    return raceInfo;
  }

  private RaceInfo getRaceInfoWithTwoEvents() {
    RaceInfo raceInfo = new RaceInfo();
    Event event = new Event();
    event.setHorses(getHorses());
    Event event2 = new Event();
    event2.setHorses(getHorsesSecond());
    Map<String, Event> document = new HashMap<>();
    document.put("765894", event);
    document.put("563628", event2);
    raceInfo.setDocument(document);
    return raceInfo;
  }

  private List<Horse> getHorses() {
    List<Horse> horses = new ArrayList<>();
    Horse horse = new Horse();
    horse.setRpHorseId(123L);
    horse.setSilkCoral("https://silkCoral1/1.gif");
    horse.setSilkLadbrokes("https://silkLadbrokes1/1.gif");
    Horse horse2 = new Horse();
    horse2.setRpHorseId(789L);
    horse2.setSilkCoral("https://silkCoral2/2.gif");
    horse2.setSilkLadbrokes("https://silkLadbrokes2/2.gif");
    Horse horse3 = new Horse();
    horse3.setRpHorseId(345L);
    horse3.setSilkCoral("https://silkCoral3/3.gif");
    horse3.setSilkLadbrokes("https://silkLadbrokes3/3.gif");
    horses.add(horse);
    horses.add(horse2);
    horses.add(horse3);
    return horses;
  }

  private List<Horse> getHorsesSecond() {
    List<Horse> horses = new ArrayList<>();
    Horse horse = new Horse();
    horse.setRpHorseId(885L);
    horse.setSilkCoral("https://silkCoral4/4.gif");
    horse.setSilkLadbrokes("https://silkLadbrokes4/4.gif");
    Horse horse2 = new Horse();
    horse2.setRpHorseId(128L);
    horse2.setSilkCoral("https://silkCoral5/5.gif");
    horse2.setSilkLadbrokes("https://silkLadbrokes5/5.gif");
    horses.add(horse);
    horses.add(horse2);
    return horses;
  }

  private ApiProperties getProperties() {
    ApiProperties properties = new ApiProperties();
    DataFeed dataFeed = new DataFeed();
    dataFeed.setEndpoint("https://test");
    dataFeed.setTimeout(Duration.ofSeconds(3));
    properties.setDf(dataFeed);
    return properties;
  }
}
