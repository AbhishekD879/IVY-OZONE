package com.ladbrokescoral.oxygen.timeline.api.model.message;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import com.ladbrokescoral.oxygen.timeline.api.model.OutputChannel;
import com.ladbrokescoral.oxygen.timeline.api.model.OutputEvent;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OutputMessage {
  private EnvelopeType type;
  private OutputEvent event;
  private OutputChannel channel;
  private OutputChannel subChannel;
  private Object message;
}
