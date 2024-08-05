package com.ladbrokescoral.oxygen.notification.entities;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Data
@Setter
@EqualsAndHashCode
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class BaseSubscription {

  @NotEmpty(message = "notification.exception.message.token")
  @Size(max = 1024)
  protected String token;

  @NotEmpty(message = "notification.exception.message.platform")
  protected String platform;

  // expiration period for subscription
  protected long hoursToExpire = 0L;
}
