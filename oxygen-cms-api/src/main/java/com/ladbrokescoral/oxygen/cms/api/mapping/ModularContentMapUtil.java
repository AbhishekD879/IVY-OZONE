package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.entity.OSDevice;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import org.apache.commons.lang3.BooleanUtils;
import org.mapstruct.Qualifier;

@ModularContentMapUtil.ModularContentUtils
public class ModularContentMapUtil {

  @MapDevices
  public List<String> mapDevices(OSDevice osDevice) {
    List<String> devices = new ArrayList<>();
    if (Objects.isNull(osDevice)) {
      return null;
    }
    if (BooleanUtils.isTrue(osDevice.getAndroid())) {
      devices.add("android");
    }
    if (BooleanUtils.isTrue(osDevice.getIos())) {
      devices.add("ios");
    }
    if (BooleanUtils.isTrue(osDevice.getWp())) {
      devices.add("wp");
    }
    return devices;
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface ModularContentUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface MapDevices {}
}
