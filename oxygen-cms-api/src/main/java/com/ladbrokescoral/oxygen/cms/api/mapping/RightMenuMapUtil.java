package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import org.mapstruct.Qualifier;
import org.springframework.util.StringUtils;

@RightMenuMapUtil.RightMenuUtils
public class RightMenuMapUtil {

  public static final String URI_LARGE_DEFAULT =
      "/images/uploads/right_menu/default/default-156x156.png";
  public static final String URI_MEDIUM_DEFAULT =
      "/images/uploads/right_menu/default/default-156x156.png";
  public static final String URI_SMALL_DEFAULT =
      "/images/uploads/right_menu/default/default-104x104.png";

  private static final String REDUNDANT_PREFIX = "public";

  @LinkTitle
  public String toDtoLinkTitle(RightMenu entity) {
    return (Objects.isNull(entity.getMenuItemView()) || !entity.getMenuItemView().equals("icon"))
            && Objects.nonNull(entity.getLinkTitle())
        ? entity.getLinkTitle()
        : "";
  }

  @UriLarge
  public String toDtoUriLarge(RightMenu entity) {
    return getUri(entity.getMenuItemView(), entity.getUriLarge(), URI_LARGE_DEFAULT);
  }

  @UriMedium
  public String toDtoUriMedium(RightMenu entity) {
    return getUri(entity.getMenuItemView(), entity.getUriMedium(), URI_MEDIUM_DEFAULT);
  }

  @UriSmall
  public String toDtoUriSmall(RightMenu entity) {
    return getUri(entity.getMenuItemView(), entity.getUriSmall(), URI_SMALL_DEFAULT);
  }

  private String getUri(String menuItemView, String uri, String defaultUri) {
    if (Objects.isNull(menuItemView) || menuItemView.equals("description")) {
      return "";
    }
    return !StringUtils.isEmpty(uri) ? uri.replace(REDUNDANT_PREFIX, "") : defaultUri;
  }

  @ShowOnlyOnOS
  public List<String> toShowOnlyOnOS(RightMenu entity) {
    List<String> showOnlyOnOS = new ArrayList<>();
    if (Objects.isNull(entity)) {
      return showOnlyOnOS;
    }
    if (entity.isShowOnlyOnIOS()) {
      showOnlyOnOS.add("ios");
    }
    if (entity.isShowOnlyOnAndroid()) {
      showOnlyOnOS.add("android");
    }
    return showOnlyOnOS;
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface RightMenuUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface LinkTitle {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface UriLarge {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface UriMedium {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface UriSmall {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ShowOnlyOnOS {}
}
