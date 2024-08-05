package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public abstract class ChainedEventMapper implements EventMapper {

  private final EventMapper chain;

  public ChainedEventMapper(EventMapper chain) {
    this.chain = chain;
  }

  @Override
  public OutputEvent map(OutputEvent resultEvent, Event event) {
    OutputEvent result = chain.map(resultEvent, event);
    populate(result, event);
    return result;
  }

  protected abstract void populate(OutputEvent result, Event event);
}
