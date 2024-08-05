package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import java.util.List;

public interface SportQuickLinkExtendedRepository {

  List<SportQuickLink> findAll(String brand);

  List<SportQuickLink> findAll(String brand, Integer sport);
}
