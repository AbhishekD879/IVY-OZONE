package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import java.util.List;
import java.util.Optional;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class OrderDto {
  private String id;
  private List<String> order;
  @SegmentNamePattern private String segmentName;
  private String pageId;
  private String pageType;
  @Builder.Default private Optional<Integer> indexId = Optional.empty();
}
