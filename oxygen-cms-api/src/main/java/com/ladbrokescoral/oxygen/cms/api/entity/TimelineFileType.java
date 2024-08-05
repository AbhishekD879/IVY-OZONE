package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.Arrays;
import lombok.Getter;

/**
 * enum that contains possible types of images. It`s purpose is to serve as request parameter
 * selector for upload/remove image methods in various menu controllers.
 */
public enum TimelineFileType {
  TOP_RIGHT_CORNER("TOP_RIGHT_CORNER"),
  HEADER_ICON("HEADER_ICON");

  @Getter private String value;

  TimelineFileType(String value) {
    this.value = value;
  }

  public static TimelineFileType fromValue(String value) {
    for (TimelineFileType fileType : TimelineFileType.values()) {
      if (fileType.value.equalsIgnoreCase(value)) {
        return fileType;
      }
    }
    throw new IllegalArgumentException(
        String.format(
            "Unknown file type: %s, accepted types are: %s", value, Arrays.toString(values())));
  }
}
