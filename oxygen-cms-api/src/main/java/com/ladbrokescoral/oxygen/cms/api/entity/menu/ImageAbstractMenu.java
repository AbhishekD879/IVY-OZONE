package com.ladbrokescoral.oxygen.cms.api.entity.menu;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;

/** interface that collect setters for small, medium & large images */
public interface ImageAbstractMenu
    extends SmallImageAbstractMenu, MediumImageAbstractMenu, LargeImageAbstractMenu, HasBrand {

  void setFilename(Filename filename);

  Filename getFilename();
}
