package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import java.util.List;

public interface BankingMenuExtendedRepository {
  List<BankingMenu> findMenus(String brand);
}
