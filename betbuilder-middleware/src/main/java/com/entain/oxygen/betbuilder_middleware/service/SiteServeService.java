package com.entain.oxygen.betbuilder_middleware.service;

import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class SiteServeService {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger();
  private static final String EVENT_IS_FINISHED = "event.isFinished";

  private static final String EVENT_CATEGORY_ID = "event.categoryId";

  @Value("${event.categoryId}")
  private String categoryId;

  private SiteServerApiAsync siteServerAsync;

  @Autowired
  public SiteServeService(SiteServerApiAsync siteServerApiAsync) {
    this.siteServerAsync = siteServerApiAsync;
  }

  public Mono<List<Event>> getFinishedEvents() {
    SimpleFilter activeClassesFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId)
                .addBinaryOperation(EVENT_IS_FINISHED, BinaryOperation.equals, "true")
                .build();
    return siteServerAsync
        .getEvents(activeClassesFilter)
        .doOnNext(
            events -> ASYNC_LOGGER.info("Finished events from siteServe size: {}", events.size()));
  }
}
