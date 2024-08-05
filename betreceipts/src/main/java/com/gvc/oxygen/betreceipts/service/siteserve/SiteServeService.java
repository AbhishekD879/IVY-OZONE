package com.gvc.oxygen.betreceipts.service.siteserve;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;

public interface SiteServeService {

  public List<String> getActiveClassesForCategoryId(int categoryId);

  public List<Event> doGetNextRacesEvents(NextEventsParameters params, List<String> classes);
}
