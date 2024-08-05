package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import reactor.core.publisher.Mono;

public interface SiteServerApiAsync {
  Mono<List<Event>> getEvents(SimpleFilter filter);
}
