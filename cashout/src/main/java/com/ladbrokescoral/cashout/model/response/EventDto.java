package com.ladbrokescoral.cashout.model.response;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class EventDto {

  private String eventId;
  private boolean vod;
}
