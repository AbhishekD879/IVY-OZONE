package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AbstractHomeModuleSegmentDto {

  private List<SegmentReference> segmentReferences = new ArrayList<>();
  private List<String> exclusionList = new ArrayList<>();
  private List<String> inclusionList = new ArrayList<>();
  private String archivalId;
  private boolean universalSegment = Boolean.TRUE;
}
