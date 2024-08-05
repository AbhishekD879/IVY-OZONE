package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.QuickLinkExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuickLinkRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class QuickLinkService extends SortableService<QuickLink> {

  private final QuickLinkExtendedRepository extendedRepository;

  @Autowired
  public QuickLinkService(
      QuickLinkRepository quickLinkRepository, QuickLinkExtendedRepository extendedRepository) {
    super(quickLinkRepository);
    this.extendedRepository = extendedRepository;
  }

  public List<QuickLink> findAllByBrand(String brand, String raceType) {
    return extendedRepository.findQuickLinks(brand, raceType);
  }
}
