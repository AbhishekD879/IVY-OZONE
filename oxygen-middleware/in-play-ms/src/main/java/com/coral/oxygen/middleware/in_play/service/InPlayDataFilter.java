package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import java.util.Collection;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

/** Created by azayats on 26.01.17. */
@Component
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
public class InPlayDataFilter {

  public InPlayDataFilter() {
    super();
  }

  public void removeEmptyNodes(InPlayData inPlayData) {
    removeEmptyNodes(inPlayData.getLivenow());
    removeEmptyNodes(inPlayData.getUpcoming());
    removeEmptyNodes(inPlayData.getLiveStream());
  }

  private void removeEmptyNodes(InPlayModel model) {
    model
        .getSportEvents()
        .forEach(
            sport ->
                sport
                    .getEventsByTypeName()
                    .removeIf(type -> isCollectionNullOrEmpty(type.getEvents())));
    model.getSportEvents().removeIf(sport -> isCollectionNullOrEmpty(sport.getEventsByTypeName()));
  }

  private boolean isCollectionNullOrEmpty(Collection<?> collection) {
    return collection == null || collection.isEmpty();
  }
}
