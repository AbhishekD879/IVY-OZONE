package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.Optional;

public enum DeviceType {
  MOBILE("mobile"),
  TABLET("tablet"),
  DESKTOP("desktop");

  private String value;

  DeviceType(String value) {
    this.value = value;
  }

  public String getValue() {
    return this.value;
  }

  public static Optional<DeviceType> fromString(String value) {
    for (DeviceType fileType : DeviceType.values()) {
      if (fileType.value.equalsIgnoreCase(value)) {
        return Optional.of(fileType);
      }
    }
    return Optional.empty();
  }
}
