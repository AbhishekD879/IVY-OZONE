package com.ladbrokescoral.oxygen.cms.api.mapping;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.Arrays;
import java.util.List;
import org.mapstruct.Qualifier;

@FeatureMapUtil.FeatureMapUtils
public class FeatureMapUtil {

  @ShowToCustomer
  public List<String> showToCustomer(String entity) {
    return entity.equals("both") ? Arrays.asList("logged-in", "logged-out") : Arrays.asList(entity);
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface FeatureMapUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ShowToCustomer {}
}
