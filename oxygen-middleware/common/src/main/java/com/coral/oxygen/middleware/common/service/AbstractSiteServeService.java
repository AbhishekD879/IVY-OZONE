package com.coral.oxygen.middleware.common.service;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public abstract class AbstractSiteServeService {

  protected final SiteServerApi siteServerApi;
  protected final MarketTemplateNameService marketTemplateNameService;

  public Map<String, Event> getCommentaryForEvent(List<String> eventIds) {
    List<Event> commentary =
        siteServerApi.getCommentaryForEvent(eventIds).orElse(Collections.emptyList());
    return commentary.stream().collect(Collectors.toMap(Event::getId, Function.identity()));
  }
}
