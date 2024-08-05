package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import java.util.List;

public interface RightMenuExtendedRepository {
  List<RightMenu> findRightMenus(String brand);
}
