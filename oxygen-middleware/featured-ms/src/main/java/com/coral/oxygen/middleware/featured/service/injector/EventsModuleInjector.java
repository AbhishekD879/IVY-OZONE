package com.coral.oxygen.middleware.featured.service.injector;

import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import java.util.List;

@FunctionalInterface
public interface EventsModuleInjector {

  void injectData(List<? extends EventsModuleData> eventsData, IdsCollector idsCollector);
}
