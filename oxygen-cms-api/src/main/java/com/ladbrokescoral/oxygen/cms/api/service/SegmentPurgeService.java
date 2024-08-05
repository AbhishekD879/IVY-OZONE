package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class SegmentPurgeService {

  private final SurfaceBetService surfaceBetService;
  private final HighlightCarouselService highlightCarouselService;
  private final HomeModuleServiceImpl homeModuleService;
  private final FooterMenuService footerMenuService;
  private final NavigationPointService navigationPointService;
  private final SportQuickLinkService sportQuickLinkService;
  private final ModuleRibbonTabService moduleRibbonTabService;
  private final SportCategoryService sportCategoryService;
  private final HomeInplaySportService homeInplaySportService;

  public void deleteSegmentsInModules(List<String> segments, String brand) {

    CompletableFuture<Void> surfaceModule =
        CompletableFuture.runAsync(() -> surfaceBetService.deleteSegments(segments, brand));

    CompletableFuture<Void> highlightCarouselModule =
        CompletableFuture.runAsync(() -> highlightCarouselService.deleteSegments(segments, brand));

    CompletableFuture<Void> homeModule =
        CompletableFuture.runAsync(() -> homeModuleService.deleteSegments(segments, brand));

    CompletableFuture<Void> footerMenuModule =
        CompletableFuture.runAsync(() -> footerMenuService.deleteSegments(segments, brand));

    CompletableFuture<Void> navigationPointModule =
        CompletableFuture.runAsync(() -> navigationPointService.deleteSegments(segments, brand));

    CompletableFuture<Void> sportQuickLinksModule =
        CompletableFuture.runAsync(() -> sportQuickLinkService.deleteSegments(segments, brand));

    CompletableFuture<Void> moduleRibbonTabModule =
        CompletableFuture.runAsync(() -> moduleRibbonTabService.deleteSegments(segments, brand));

    CompletableFuture<Void> homeInplaySportModule =
        CompletableFuture.runAsync(() -> homeInplaySportService.deleteSegments(segments, brand));

    CompletableFuture<Void> sportCategoryModule =
        CompletableFuture.runAsync(() -> sportCategoryService.deleteSegments(segments, brand));

    CompletableFuture.allOf(
            surfaceModule,
            highlightCarouselModule,
            homeModule,
            footerMenuModule,
            navigationPointModule,
            sportQuickLinksModule,
            moduleRibbonTabModule,
            homeInplaySportModule,
            sportCategoryModule)
        .join();
  }
}
