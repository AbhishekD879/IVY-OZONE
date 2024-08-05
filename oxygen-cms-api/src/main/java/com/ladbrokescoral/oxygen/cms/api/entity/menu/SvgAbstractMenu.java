package com.ladbrokescoral.oxygen.cms.api.entity.menu;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;

/** This class has svg related methods */
public interface SvgAbstractMenu extends HasBrand {

  void setSvgFilename(SvgFilename svfFilename);

  SvgFilename getSvgFilename();

  void setSvg(String svg);

  void setSvgId(String svgId);
}
