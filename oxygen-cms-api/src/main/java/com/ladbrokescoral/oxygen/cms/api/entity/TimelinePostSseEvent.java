package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import lombok.Data;

@Data
public class TimelinePostSseEvent {
  private TimelineChangelogOperation operation;
  private String campaignId;
  private TimelinePost content;
  private String contentId;
}
