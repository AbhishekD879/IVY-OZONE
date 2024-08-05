package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.repository.PromoConfigRepository;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.RequestUtilHelper;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.boot.ApplicationArguments;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
class InitiateRddRefreshListenerServiceTest {
  private static final List<PromoConfig> promoConfigs = new ArrayList<>();
  @Mock private PromoConfigRepository promoConfigRepository;
  @Mock private RddCreationService RDDCreationService;
  @Mock private PromoConfigService promoConfigService;
  @Mock private AmazonS3Service amazonS3Service;

  @InjectMocks private InitiateRddRefreshListenerService initiateRddRefreshListenerService;

  @BeforeAll
  static void setup() {
    PromoConfig promoConfig = new PromoConfig();
    promoConfig.setStartDate(Instant.now());
    promoConfig.setEndDate(Instant.now().plusSeconds(20));
    promoConfig.setPromotionId(IConstantsTest.PROMOTION_ID);
    promoConfigs.add(promoConfig);
  }

  @BeforeEach
  void beforeEachSetup() {
    ReflectionTestUtils.setField(
        initiateRddRefreshListenerService, IConstantsTest.BRAND, IConstantsTest.LADBROKES);
  }

  @Test
  void runSuccessTest() {
    ApplicationArguments applicationArguments = Mockito.mock(ApplicationArguments.class);
    assertNotNull(promoConfigRepository);
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenReturn(promoConfigs);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any()))
        .thenReturn(RequestUtilHelper.prepareUserRankInfo());
    initiateRddRefreshListenerService.run(applicationArguments);
  }

  @Test
  void runSuccessPromoExpiredTest() {
    ApplicationArguments applicationArguments = Mockito.mock(ApplicationArguments.class);
    assertNotNull(promoConfigRepository);
    List<PromoConfig> promoConfigList = new ArrayList<>();
    PromoConfig promoConfig = new PromoConfig();
    promoConfig.setStartDate(Instant.now());
    promoConfig.setEndDate(Instant.now().minusSeconds(20));
    promoConfig.setPromotionId(IConstantsTest.PROMOTION_ID);
    promoConfigList.add(promoConfig);
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenReturn(promoConfigList);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any()))
        .thenReturn(RequestUtilHelper.prepareUserRankInfo());
    initiateRddRefreshListenerService.run(applicationArguments);
  }

  @Test
  void runSuccessEmptyResponseTest() {
    ApplicationArguments applicationArguments = Mockito.mock(ApplicationArguments.class);
    assertNotNull(promoConfigRepository);
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenReturn(promoConfigs);
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setRowList(new ArrayList<>());
    userRankInfoDto.setStructType(null);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any())).thenReturn(userRankInfoDto);
    initiateRddRefreshListenerService.run(applicationArguments);
  }

  @Test
  void runSuccessInvalidResponseTest() {
    ApplicationArguments applicationArguments = Mockito.mock(ApplicationArguments.class);
    assertNotNull(promoConfigRepository);
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenReturn(promoConfigs);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any())).thenReturn(new UserRankInfoDto());
    initiateRddRefreshListenerService.run(applicationArguments);
  }

  @Test
  void runSuccessEmptyResponse2Test() {
    ApplicationArguments applicationArguments = Mockito.mock(ApplicationArguments.class);
    assertNotNull(promoConfigRepository);
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenReturn(promoConfigs);
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setRowList(RequestUtilHelper.prepareUserRankInfo().getRowList());
    userRankInfoDto.setStructType(null);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any())).thenReturn(userRankInfoDto);
    initiateRddRefreshListenerService.run(applicationArguments);
  }

  @Test
  void runSuccessFailureTest() {
    ApplicationArguments applicationArguments = Mockito.mock(ApplicationArguments.class);
    when(promoConfigRepository.findAllByBrandAndIsDataCleaned(anyString(), anyBoolean()))
        .thenThrow(NullPointerException.class);
    initiateRddRefreshListenerService.run(applicationArguments);
    assertNotNull(promoConfigRepository);
  }
}
