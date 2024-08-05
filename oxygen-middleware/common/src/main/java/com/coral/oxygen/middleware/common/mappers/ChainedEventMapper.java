package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public abstract class ChainedEventMapper implements EventMapper {

  private final EventMapper chain;

  public ChainedEventMapper(EventMapper chain) {
    this.chain = chain;
  }

  @Override
  public EventsModuleData map(EventsModuleData resultEvent, Event event) {
    EventsModuleData result = chain.map(resultEvent, event);
    try {
      populate(result, event);
    } catch (Exception e) {
      log.error(
          "Suppressed error during event mapping in class " + this.getClass().getCanonicalName(),
          e);
    }
    return result;
  }

  protected abstract void populate(EventsModuleData result, Event event);
}
