package com.ladbrokescoral.oxygen.cms.api.entity.menu;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;

public interface IconAbstractMenu extends HasBrand {
  void setIcon(Filename icon);

  Filename getIcon();

  void setUriSmallIcon(String uriSmallIcon);

  String getUriSmallIcon();

  void setHeightSmallIcon(Integer heightSmallIcon);

  void setWidthSmallIcon(Integer widthSmallIcon);

  void setUriMediumIcon(String uriMediumIcon);

  String getUriMediumIcon();

  void setHeightMediumIcon(Integer heightMediumIcon);

  void setWidthMediumIcon(Integer widthMediumIcon);

  void setUriLargeIcon(String uriLargeIcon);

  String getUriLargeIcon();

  void setHeightLargeIcon(Integer heightLargeIcon);

  void setWidthLargeIcon(Integer widthLargeIcon);
}
