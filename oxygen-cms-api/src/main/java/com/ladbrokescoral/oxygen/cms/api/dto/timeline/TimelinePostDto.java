package com.ladbrokescoral.oxygen.cms.api.dto.timeline;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import lombok.experimental.Accessors;

@Data
@ToString(callSuper = true)
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
public class TimelinePostDto extends TimelineMessageDto {
  private TemplateDto template;
  private String campaignId;
  private String campaignName;
  private boolean pinned;
  private boolean isSpotlight;
  private boolean isVerdict;
}
