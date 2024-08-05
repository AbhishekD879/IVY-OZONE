package com.coral.oxygen.middleware.in_play.service.model;

import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.Collection;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by Aliaksei Yarotski on 12/6/17. */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class SportCompetitionChanges {

  // the categoryId::topLevelType[::marketSelector]
  private String key;
  private String generationId;
  private Map<String, TypeSegment> added;
  private Collection<String> removed;
  private Collection<String> changed;

  public boolean isEmpty() {
    return added.isEmpty() && removed.isEmpty() && changed.isEmpty();
  }

  public boolean isNotEmpty() {
    return !isEmpty();
  }
}
