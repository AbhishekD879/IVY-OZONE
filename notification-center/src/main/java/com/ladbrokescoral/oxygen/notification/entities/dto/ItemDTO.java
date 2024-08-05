package com.ladbrokescoral.oxygen.notification.entities.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@ToString
@EqualsAndHashCode
@NoArgsConstructor
public class ItemDTO {
  private String id;
  private Long eventId;
  private String token;
  private String type;
  private String platform;
  private String ownerId;
  private Integer appVersionInt;
}
