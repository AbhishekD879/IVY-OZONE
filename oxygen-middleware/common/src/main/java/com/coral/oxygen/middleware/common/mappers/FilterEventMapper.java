package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.Objects;

public class FilterEventMapper extends ChainedEventMapper {

  public FilterEventMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  public EventsModuleData map(EventsModuleData resultEvent, Event event) {
    // Commented because we should display inactive suspended events. which are inactive and not
    // available
    if (Objects.nonNull(event)) {
      // start chain
      return super.map(resultEvent, event);
    } else {
      // skip chain and return not populated result
      return resultEvent;
    }
  }

  @Override
  protected void populate(EventsModuleData result, Event event) {
    // should be empty
  }
}
