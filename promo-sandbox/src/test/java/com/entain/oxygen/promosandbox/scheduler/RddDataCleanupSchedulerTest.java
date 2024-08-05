package com.entain.oxygen.promosandbox.scheduler;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.anyBoolean;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.schedular.RddDataCleanupScheduler;
import com.entain.oxygen.promosandbox.service.CacheManagerService;
import com.entain.oxygen.promosandbox.service.HouseKeepingService;
import com.entain.oxygen.promosandbox.service.PromoConfigService;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.RequestUtilHelper;
import java.time.Instant;
import java.util.ArrayList;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
class RddDataCleanupSchedulerTest {

  private static PromoConfig promoConfig;

  @Mock private PromoConfigService promoConfigService;

  @Mock private CacheManagerService cacheManagerService;

  @Mock private HouseKeepingService houseKeepingService;

  @InjectMocks private RddDataCleanupScheduler promoDataCleanupScheduler;

  @BeforeEach
  void beforeEachSetup() {
    promoConfig = new PromoConfig();
    promoConfig.setStartDate(Instant.now());
    promoConfig.setPromotionId(IConstantsTest.PROMOTION_ID);
    ReflectionTestUtils.setField(
        promoDataCleanupScheduler, IConstantsTest.BRAND, IConstantsTest.LADBROKES);
  }

  @Test
  void dataCleanupJobPromoExpireTest() {
    promoConfig.setEndDate(Instant.now().plusSeconds(20));
    assertNotNull(promoConfigService);
    when(promoConfigService.findAllByBrandAndDataCleanupStatus(anyString(), anyBoolean()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig));
    promoDataCleanupScheduler.dataCleanupJob();
  }

  @Test
  void dataCleanupJobPromoNotExpireTest() {
    promoConfig.setEndDate(Instant.now().minusSeconds(20));
    assertNotNull(promoConfigService);
    when(promoConfigService.findAllByBrandAndDataCleanupStatus(anyString(), anyBoolean()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig));
    promoDataCleanupScheduler.dataCleanupJob();
  }

  @Test
  void dataCleanupJobEmptyConfigTest() {
    assertNotNull(promoConfigService);
    when(promoConfigService.findAllByBrandAndDataCleanupStatus(anyString(), anyBoolean()))
        .thenReturn(new ArrayList<>());
    promoDataCleanupScheduler.dataCleanupJob();
  }

  @Test
  void dataCleanupJobFailureTest() {
    assertNotNull(promoConfigService);
    when(promoConfigService.findAllByBrandAndDataCleanupStatus(anyString(), anyBoolean()))
        .thenThrow(NullPointerException.class);
    promoDataCleanupScheduler.dataCleanupJob();
  }
}
