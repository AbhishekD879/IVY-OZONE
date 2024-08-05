package com.ladbrokescoral.oxygen.cms.api.mapping;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.mapstruct.Qualifier;

@StreamAndBetMapUtil.StreamAndBetUtils
public class StreamAndBetMapUtil {

  @AndroidActive
  public Boolean isAndroidActive(String showItemFor) {
    return isDeviceActive("android", showItemFor);
  }

  @IOSActive
  public Boolean isIosActive(String showItemFor) {
    return isDeviceActive("ios", showItemFor);
  }

  private Boolean isDeviceActive(String device, String showItemFor) {
    return device.equalsIgnoreCase(showItemFor) || "both".equalsIgnoreCase(showItemFor);
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface StreamAndBetUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface AndroidActive {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface IOSActive {}
}
