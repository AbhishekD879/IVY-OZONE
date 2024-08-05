package com.ladbrokescoral.oxygen.notification.entities;

import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(exclude = {"platform"})
@Data
@AllArgsConstructor
public class Device {
  private final String token;
  private final Platform platform;
  private final Integer appVersionInt;
}
