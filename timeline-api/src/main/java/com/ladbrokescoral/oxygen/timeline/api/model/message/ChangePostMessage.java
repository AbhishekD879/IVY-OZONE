package com.ladbrokescoral.oxygen.timeline.api.model.message;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
public class ChangePostMessage extends ActionMessage {
  private PostMessage data;

  @Override
  public TimeBasedId timeBasedId() {
    return new TimeBasedId(getAffectedMessageId(), getAffectedMessageCreatedDate());
  }
}
