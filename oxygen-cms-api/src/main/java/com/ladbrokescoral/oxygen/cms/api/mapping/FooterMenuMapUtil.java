package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import org.mapstruct.Qualifier;

@FooterMenuMapUtil.FooterMenuMapUtils
public class FooterMenuMapUtil {

  @ToTarget
  public String toTarget(FooterMenu entity) {
    return Objects.nonNull(entity.getItemType())
            && entity.getItemType().equals("link")
            && Objects.nonNull(entity.getTargetUri())
        ? entity.getTargetUri()
        : "";
  }

  @ToInApp
  public Boolean toInApp(FooterMenu entity) {
    return Objects.nonNull(entity.getItemType()) && entity.getItemType().equals("link")
        ? entity.isInApp()
        : null;
  }

  @ToWidget
  public String toWidget(FooterMenu entity) {

    return Objects.nonNull(entity.getItemType()) && entity.getItemType().equals("widget")
        ? entity.getWidgetName()
        : null;
  }

  @ToDevice
  public List<String> toDevice(FooterMenu entity) {
    List<String> device = new ArrayList<>();
    if (entity.isMobile()) device.add("m");
    if (entity.isTablet()) device.add("t");
    if (entity.isDesktop()) device.add("d");
    return device;
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface FooterMenuMapUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ToTarget {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ToInApp {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ToWidget {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ToDevice {}
}
