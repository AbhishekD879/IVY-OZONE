package com.entain.oxygen.betbuilder_middleware.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.model.Event;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class SiteServeServiceTest {
  @Mock private SiteServerApiAsync siteServerApiAsync;
  @InjectMocks private SiteServeService siteServeService;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testGetFinishedEvents() {
    List<Event> mockEvents = new ArrayList<>();
    Event event1 = new Event();
    event1.setId("1");
    mockEvents.add(event1);

    when(siteServerApiAsync.getEvents(any())).thenReturn(Mono.just(mockEvents));

    Mono<List<Event>> resultMono = siteServeService.getFinishedEvents();

    StepVerifier.create(resultMono)
        .expectSubscription()
        .expectNext(mockEvents)
        .expectComplete()
        .verify(Duration.ofSeconds(5));
  }
}
