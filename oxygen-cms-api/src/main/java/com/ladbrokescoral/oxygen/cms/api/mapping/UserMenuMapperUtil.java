package com.ladbrokescoral.oxygen.cms.api.mapping;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.mapstruct.Qualifier;
import org.springframework.util.StringUtils;

@UserMenuMapperUtil.UserMenuUtils
public class UserMenuMapperUtil {
  @TargetUri
  public String toDtoTargetUri(String entity) {
    return !StringUtils.isEmpty(entity) ? entity : "my-account";
  }

  @UriMedium
  public String toDtoUriMedium(String entity) {
    return !StringUtils.isEmpty(entity)
        ? removePublicPrefix(entity)
        : RightMenuMapUtil.URI_MEDIUM_DEFAULT;
  }

  @UriSmall
  public String toDtoUriSmall(String entity) {
    // expected input is something like
    // 'public/images/uploads/user_menu/medium/MYFREEBETSBONUSES.png'
    return !StringUtils.isEmpty(entity)
        ? removePublicPrefix(entity)
        : RightMenuMapUtil.URI_SMALL_DEFAULT;
  }

  private String removePublicPrefix(String entity) {
    return entity.startsWith("public") ? entity.substring(6) : entity;
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface UserMenuUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface TargetUri {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface UriMedium {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface UriSmall {}
}
