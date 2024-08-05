package com.ladbrokescoral.oxygen.cms.api.dto.timeline;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import lombok.experimental.Accessors;

@Data
@ToString(callSuper = true)
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
public class RemoveCampaignTimelineMessageDto extends ActionTimelineMessageDto {}
