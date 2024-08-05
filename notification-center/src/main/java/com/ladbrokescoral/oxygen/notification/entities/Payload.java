package com.ladbrokescoral.oxygen.notification.entities;

import java.util.LinkedList;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.ToString;

@Data
@Builder
@ToString
public class Payload {
  private Long eventId;
  private String message;
  private String status;
  private String type;
  private String deepLink;
  @Builder.Default private List<Device> devices = new LinkedList<>();
}
