package com.ladbrokescoral.oxygen.timeline.api.model.message;

import lombok.AccessLevel;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@Builder(access = AccessLevel.PUBLIC)
public class TimelineConfigMessage extends Message {
  private boolean enabled;
}
