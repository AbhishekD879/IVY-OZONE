package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;

@Data
public class InplayDataSportItem {
  private int sportNumber;
  private int categoryId;
  private int eventCount;
  private List<String> segments;
  private List<SegmentReference> segmentReferences;
}
