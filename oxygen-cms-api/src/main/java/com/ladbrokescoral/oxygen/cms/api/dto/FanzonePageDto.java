package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class FanzonePageDto extends AbstractTimelineEntity<FanzonePageDto> implements HasBrand {
  @NotNull private String pageName;
  @NotNull private String brand;
}
