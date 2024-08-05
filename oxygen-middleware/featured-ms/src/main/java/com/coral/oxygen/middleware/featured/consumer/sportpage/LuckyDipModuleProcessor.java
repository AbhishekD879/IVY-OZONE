package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.featured.service.LuckyDipModuleService;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.LuckyDip;
import com.coral.oxygen.middleware.pojos.model.cms.featured.LuckyDipMapping;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.LuckyDipCategoryData;
import com.coral.oxygen.middleware.pojos.model.output.featured.LuckyDipModule;
import java.time.Duration;
import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class LuckyDipModuleProcessor implements ModuleConsumer<LuckyDipModule> {

  private final LuckyDipModuleService luckyDipModuleService;

  @Override
  public LuckyDipModule processModule(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    Instant start = Instant.now();
    LuckyDipModule ldModule = new LuckyDipModule(cmsModule.getSportModule());
    List<LuckyDipCategoryData> luckyDipData = processLuckyDipData(cmsModule);
    ldModule.setData(luckyDipData);
    Instant end = Instant.now();
    log.info(
        "duration time for processing LuckyDipModule {}", Duration.between(start, end).toMillis());
    return ldModule;
  }

  private List<LuckyDipCategoryData> processLuckyDipData(SportPageModule cmsModule) {

    Optional<LuckyDip> luckyDip =
        cmsModule.getPageData().stream().map(LuckyDip.class::cast).findFirst();
    if (luckyDip.isEmpty()) {
      log.info("CMS LuckyDip configuration is empty :{}", true);
      return Collections.emptyList();
    }
    LuckyDip luckyDipConfig = luckyDip.get();
    List<LuckyDipMapping> luckyDipMappings = luckyDipConfig.getLuckyDipMappings();
    if (luckyDipMappings == null || luckyDipMappings.isEmpty()) {
      log.info("CMS LuckyDip mappings are null or empty");
      return Collections.emptyList();
    }
    return luckyDipModuleService.processLuckyDipData(luckyDipMappings);
  }
}
