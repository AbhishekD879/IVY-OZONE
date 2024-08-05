package com.ladbrokescoral.oxygen.notification.entities;

import lombok.*;

@Data
@Setter
@EqualsAndHashCode
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class WinalertStatus {

  protected String userName;
  protected String token;
  protected String platform;
  protected String betId;
}
