package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.anyBoolean;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.entain.oxygen.promosandbox.dto.LeaderboardConfigDto;
import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.dto.StatusDto;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.repository.PromoConfigRepository;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.RequestUtilHelper;
import com.entain.oxygen.promosandbox.utils.TestUtil;
import java.io.IOException;
import java.time.Instant;
import java.util.Optional;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
class PromoConfigServiceTest {

  private static PromoMessageDto promoMessageDto;

  private static LeaderboardConfigDto leaderboardConfigDto;

  private static PromoConfig promoConfig;

  @Mock private PromoConfigRepository promoConfigRepository;

  @InjectMocks private PromoConfigService promoConfigService;

  @BeforeAll
  static void setup() throws IOException {
    promoMessageDto = TestUtil.deserializeWithJackson("/promoConfig.json", PromoMessageDto.class);
    promoConfig = new PromoConfig();
    promoConfig.setPromotionId(promoMessageDto.getPromotionId());
    leaderboardConfigDto = new LeaderboardConfigDto();
    leaderboardConfigDto.setLeaderboardId(IConstantsTest.LEADERBOARD_ID);
  }

  @Test
  void savePromoConfigFileStatusFalseTest() {
    promoConfigService.savePromoConfig(
        promoMessageDto, leaderboardConfigDto, new StatusDto(false, Instant.now()));
    assertNotNull(promoMessageDto);
  }

  @Test
  void savePromoConfigFileStatusTrueTest() {
    promoConfigService.savePromoConfig(
        promoMessageDto, leaderboardConfigDto, new StatusDto(true, Instant.now()));
    assertNotNull(promoMessageDto);
  }

  @Test
  void updatePromoConfigFileStatusFalseTest() {
    promoConfigService.updatePromoConfig(
        promoConfig, promoMessageDto, leaderboardConfigDto, new StatusDto(false, Instant.now()));
    assertNotNull(promoMessageDto);
  }

  @Test
  void updatePromoConfigFileStatusTrueTest() {
    promoConfigService.updatePromoConfig(
        promoConfig, promoMessageDto, leaderboardConfigDto, new StatusDto(true, Instant.now()));
    assertNotNull(promoMessageDto);
  }

  @Test
  void updatePromoStartEndDateTest() {
    when(promoConfigRepository.findAllByPromotionId(anyString()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig));
    promoConfigService.updatePromoStartEndDate(promoMessageDto);
    assertNotNull(promoMessageDto);
  }

  @Test
  void updatePromoIsDataCleanupStatusTest() {
    when(promoConfigRepository.findById(anyString())).thenReturn(Optional.of(promoConfig));
    promoConfigService.updatePromoIsDataCleanupStatus(promoMessageDto.getPromotionId(), true);
    assertNotNull(promoMessageDto);
  }

  @Test
  void updatePromoFileStatusTrueTest() {
    when(promoConfigRepository.findById(anyString())).thenReturn(Optional.of(promoConfig));
    promoConfigService.updatePromoFileStatus(
        promoMessageDto.getPromotionId(), new StatusDto(true, Instant.now()));
    assertNotNull(promoMessageDto);
  }

  @Test
  void updatePromoFileStatusFalseTest() {
    when(promoConfigRepository.findById(anyString())).thenReturn(Optional.of(promoConfig));
    promoConfigService.updatePromoFileStatus(
        promoMessageDto.getPromotionId(), new StatusDto(false, Instant.now()));
    assertNotNull(promoMessageDto);
  }

  @Test
  void findByIdTest() {
    when(promoConfigRepository.findById(anyString())).thenReturn(Optional.of(promoConfig));
    assertNotNull(
        promoConfigService.findById(
            IConstantsTest.PROMOTION_ID + "_" + IConstantsTest.LEADERBOARD_ID));
  }

  @Test
  void getLastFileModifiedTest() {
    when(promoConfigRepository.findById(anyString())).thenReturn(Optional.of(promoConfig));
    assertNotNull(
        promoConfigService.getLastFileModified(
            IConstantsTest.PROMOTION_ID, IConstantsTest.LEADERBOARD_ID));
  }

  @Test
  void findAllByBrandAndDataCleanupStatusTest() {
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig));
    promoConfigService.findAllByBrandAndDataCleanupStatus(promoMessageDto.getBrand(), true);
    assertNotNull(promoMessageDto);
  }
}
