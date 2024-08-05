package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Scorecast;
import io.vavr.collection.List;
import java.util.Arrays;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class SiteServerServiceTest {

  @Mock private SiteServerApi siteServerApi;

  private SiteServerService siteServerService;

  @BeforeEach
  void setUp() {
    siteServerService = new SiteServerService(siteServerApi, 1);
  }

  @Test
  void getEventsForOutcomeIdsTest() {
    // given
    List<String> outcomeIds = List.of("1", "2");

    // when
    siteServerService.getEventsForOutcomeIds(outcomeIds);

    // then
    verify(siteServerApi)
        .getEventToOutcomeForOutcome(eq(Arrays.asList("1", "2")), any(), isNull(), eq(false));
  }

  @Test
  void getEventToOutcomeForOutcomeTest() {
    // given
    java.util.List<Long> outcomeIds = Arrays.asList(1L, 2L);

    // when
    siteServerService.getEventToOutcomeForOutcome(outcomeIds);

    // then
    verify(siteServerApi)
        .getEventToOutcomeForOutcome(eq(Arrays.asList("1", "2")), any(), isNull(), eq(false));
  }

  @Test
  void getEventsForTest() {
    // given
    java.util.List<String> outcomeIds = Arrays.asList("1", "2");

    // when
    siteServerService.getEventsFor(outcomeIds);

    // then
    verify(siteServerApi)
        .getEventToOutcomeForOutcome(eq(Arrays.asList("1", "2")), any(), isNull(), eq(false));
  }

  @Test
  void shouldGetScorecastData() {
    // GIVEN
    String marketId = "MarketId";
    String scorerOutcomeId = "OutcomeId";
    Scorecast scorecast = mock(Scorecast.class);
    Optional<Scorecast> expectedResponse = Optional.of(scorecast);
    when(siteServerApi.getScorecast(marketId, scorerOutcomeId)).thenReturn(expectedResponse);

    // WHEN
    Optional<Scorecast> response = siteServerService.getScorecast(marketId, scorerOutcomeId);

    // THEN
    assertThat(response).contains(scorecast);
  }

  @Test
  void getEventToOutcomeForMarketForLuckyDipTest() {
    // GIVEN
    when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any(), any()))
        .thenReturn(Optional.of(Arrays.asList(new Event())));
    // WHEN
    Optional<java.util.List<Event>> response =
        siteServerService.getEventToOutcomeForMarketForLuckyDip("1");
    // THEN
    assertThat(response).isPresent();
  }
}
