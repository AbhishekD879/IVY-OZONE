package com.oxygen.publisher.model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by Aliaksei Yarotski on 12/6/17. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SportCompetitionChanges {

  // the categoryId::topLevelType[::marketSelector]
  private String key;
  private String generationId;
  // list initialization is required here because of business requirements
  private Map<String, TypeSegment> added = new HashMap();
  private Set<String> changed = new HashSet();
  private Set<String> removed = new HashSet();

  public SportCompetitionChanges key(String key) {
    this.key = key;
    return this;
  }
}
