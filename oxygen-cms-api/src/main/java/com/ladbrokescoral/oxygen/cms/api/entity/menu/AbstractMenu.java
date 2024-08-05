package com.ladbrokescoral.oxygen.cms.api.entity.menu;

/** This class helps to simplify retrieving child menu sections for various *Menu classes. */
public interface AbstractMenu {

  String getId();

  String getParent();

  String getTargetUri();

  String getLinkTitle();

  Boolean getDisabled();

  Boolean getInApp();
}
