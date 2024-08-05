package com.ladbrokescoral.oxygen.timeline.api.model.message;

import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
public abstract class ActionMessage extends Message {
  private String affectedMessageId;
  private Instant affectedMessageCreatedDate;

  @Override
  public TimeBasedId timeBasedId() {
    return new TimeBasedId(affectedMessageId, getTimePart());
  }

  private Instant getTimePart() {
    if (affectedMessageCreatedDate != null) {
      return affectedMessageCreatedDate;
    } // looks like this is a workaround for some bug, for some reason affectedMessageCreatedDate is
    // null for delete actions
    if (super.getCreatedDate() != null) {
      return super.getCreatedDate();
    } else {
      throw new IllegalStateException("Can not generate time based id as no date/time data");
    }
  }
}
