package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink;
import java.util.List;

public interface QuickLinkExtendedRepository {
  List<QuickLink> findQuickLinks(String brand, String raceType);
}
