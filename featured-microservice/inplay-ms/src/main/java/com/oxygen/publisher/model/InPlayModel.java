package com.oxygen.publisher.model;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import lombok.Data;

@Data
public class InPlayModel {

  private Collection<Long> eventsIds = new ArrayList<>();
  private List<SportSegment> eventsBySports = new ArrayList<>();
  private int eventCount;
}
