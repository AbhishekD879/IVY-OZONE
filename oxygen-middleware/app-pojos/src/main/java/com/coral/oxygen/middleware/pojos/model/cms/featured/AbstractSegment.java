package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
public class AbstractSegment implements Serializable {

  private List<String> segments;
  private List<SegmentReference> segmentReferences;
}
