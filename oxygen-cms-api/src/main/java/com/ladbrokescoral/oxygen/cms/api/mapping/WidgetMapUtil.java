package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ShowOnDto;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.mapstruct.Qualifier;

@WidgetMapUtil.WidgetUtils
public class WidgetMapUtil {

  @ShowOn
  public ShowOnDto toShowOnDto(com.ladbrokescoral.oxygen.cms.api.entity.ShowOn showOn) {
    if (showOn != null && showOn.getRoutes() != null) {
      return new ShowOnDto().routes(showOn.getRoutes());
    }
    return null;
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface WidgetUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ShowOn {}
}
