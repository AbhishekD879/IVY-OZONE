package com.ladbrokescoral.oxygen.timeline.api.model.message;

import com.ladbrokescoral.oxygen.timeline.api.model.Template;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.TimelineSelectionEvent;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.index.Indexed;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@Builder(access = AccessLevel.PUBLIC)
@RedisHash("postMessages")
public class PostMessage extends Message {
  private Template template;
  @Indexed private String campaignId;
  private String campaignName;
  private boolean pinned;
  private String text;
  private String headerText;
  private boolean isSpotlight;
  private boolean isVerdict;
  private TimelineSelectionEvent selectionEvent;
}
