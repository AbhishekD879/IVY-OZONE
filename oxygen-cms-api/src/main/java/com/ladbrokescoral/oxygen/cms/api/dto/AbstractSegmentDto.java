package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public abstract class AbstractSegmentDto {
  private List<String> segments = new ArrayList<>();
  private List<SegmentReferenceDto> segmentReferences = new ArrayList<>();
  private List<String> fanzoneSegments = new ArrayList<>();
  private boolean universalSegment = true;
}
