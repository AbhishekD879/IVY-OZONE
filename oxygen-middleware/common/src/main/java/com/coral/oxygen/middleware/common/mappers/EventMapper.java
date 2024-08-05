package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

public interface EventMapper {
  EventsModuleData map(EventsModuleData result, Event event);
}
