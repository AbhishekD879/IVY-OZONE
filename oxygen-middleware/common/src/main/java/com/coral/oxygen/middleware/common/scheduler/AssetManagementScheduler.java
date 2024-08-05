package com.coral.oxygen.middleware.common.scheduler;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class AssetManagementScheduler {

  private final CmsService cmsService;

  private final AssetManagementService assetManagementService;

  @Scheduled(cron = "${app.featured.cron.expression}", zone = "${time.zone}")
  public void doJob() {
    try {
      assetManagementService.saveAll(
          (List<AssetManagement>) cmsService.getAssetManagementInfoByBrand());
    } catch (Exception ex) {
      log.error("Error while posting data from Cms ", ex);
    }
  }
}
