package com.ladbrokescoral.oxygen.timeline.api.ws.model;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class IncomingRequest {
  private ClientAction clientAction;
  private Object input;
}
