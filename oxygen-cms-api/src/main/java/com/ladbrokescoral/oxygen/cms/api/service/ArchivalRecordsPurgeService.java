package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HighlightCarouselArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.ModuleRibbonTabArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportQuickLinkArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SurfaceBetArchivalRepository;
import java.time.Instant;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ArchivalRecordsPurgeService {

  private final SurfaceBetArchivalRepository surfaceBetArchivalRepository;
  private final HighlightCarouselArchiveRepository highlightCarouselArchiveRepository;
  private final HomeModuleArchivalRepository homeModuleArchivalRepository;
  private final FooterMenuArchivalRepository footerMenuArchivalRepository;
  private final NavigationPointArchivalRepository navigationPointArchivalRepository;
  private final SportQuickLinkArchivalRepository sportQuickLinkArchivalRepository;
  private final ModuleRibbonTabArchiveRepository moduleRibbonTabArchiveRepository;
  private final SegmentArchivalRepository segmentArchivalRepository;
  private final SportCategoryArchivalRepository sportCategoryArchivalRepository;
  private final SportModuleArchivalRepository sportModuleArchivalRepository;

  public void deleteByArchivalDateBefore(Instant purgeDate) {
    surfaceBetArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    highlightCarouselArchiveRepository.deleteByArchivalDateBefore(purgeDate);
    homeModuleArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    footerMenuArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    moduleRibbonTabArchiveRepository.deleteByArchivalDateBefore(purgeDate);
    sportQuickLinkArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    navigationPointArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    segmentArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    sportCategoryArchivalRepository.deleteByArchivalDateBefore(purgeDate);
    sportModuleArchivalRepository.deleteByArchivalDateBefore(purgeDate);
  }
}
