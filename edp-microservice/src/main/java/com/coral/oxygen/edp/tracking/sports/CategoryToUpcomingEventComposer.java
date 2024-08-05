package com.coral.oxygen.edp.tracking.sports;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent;
import com.egalacoral.spark.siteserver.model.Category;
import java.util.Collection;
import java.util.List;

public interface CategoryToUpcomingEventComposer {

  List<CategoryToUpcomingEvent> composeCategoriesToEvents(
      Collection<? extends Category> categories, Collection<? extends OutputEvent> events);
}
