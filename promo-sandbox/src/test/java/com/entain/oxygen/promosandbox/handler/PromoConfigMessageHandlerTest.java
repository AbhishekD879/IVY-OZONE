package com.entain.oxygen.promosandbox.handler;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.when;

import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.service.*;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.RequestUtilHelper;
import com.entain.oxygen.promosandbox.utils.TestUtil;
import java.io.IOException;
import java.util.ArrayList;
import org.apache.spark.sql.types.StructType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
class PromoConfigMessageHandlerTest {
  private static PromoMessageDto promoMessageDto;
  @Mock private HouseKeepingService houseKeepingService;
  @Mock private PromoConfigService promoConfigService;
  @Mock private AmazonS3Service amazonS3Service;
  @Mock private CacheManagerService cacheManagerService;
  @Mock private RddCreationService RDDCreationService;
  @InjectMocks private PromoConfigMessageHandler promoConfigMessageHandler;

  @BeforeAll
  static void setUp() throws IOException {
    promoMessageDto = TestUtil.deserializeWithJackson("/promoMessage.json", PromoMessageDto.class);
  }

  @Test
  void handleCreateKafkaMessageEmptyResponseTest() {
    promoMessageDto.setAction("Create");
    assertNotNull(promoConfigMessageHandler);
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setRowList(new ArrayList<>());
    userRankInfoDto.setStructType(new StructType());
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any())).thenReturn(userRankInfoDto);
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }

  @Test
  void handleCreateKafkaMessageFailureTestTest() {
    promoMessageDto.setAction("Create");
    assertNotNull(promoConfigMessageHandler);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any())).thenReturn(new UserRankInfoDto());
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }

  @Test
  void handleCreateKafkaMessageTest() {
    promoMessageDto.setAction("Create");
    assertNotNull(promoConfigMessageHandler);
    when(amazonS3Service.fetchAmazonS3CsvData(any(), any()))
        .thenReturn(RequestUtilHelper.prepareUserRankInfo());
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }

  @Test
  void handleUpdateKafkaMessageTest() {
    promoMessageDto.setAction("Update");
    assertNotNull(promoConfigMessageHandler);
    PromoConfig promoConfig = new PromoConfig();
    promoConfig.setPromotionId(IConstantsTest.PROMOTION_ID);
    promoConfig.setLeaderboardId(promoMessageDto.getPromoLbConfigs().get(0).getLeaderboardId());
    when(promoConfigService.findById(any()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig).stream().findFirst());
    doReturn(RequestUtilHelper.prepareUserRankInfo())
        .when(amazonS3Service)
        .fetchAmazonS3CsvData(anyString(), anyString());
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }

  @Test
  void handleUpdateKafkaMessageColumnNullResponseTest() {
    promoMessageDto.setAction("Update");
    assertNotNull(promoConfigMessageHandler);
    PromoConfig promoConfig = new PromoConfig();
    promoConfig.setPromotionId(IConstantsTest.PROMOTION_ID);
    promoConfig.setLeaderboardId(promoMessageDto.getPromoLbConfigs().get(0).getLeaderboardId());
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setRowList(new ArrayList<>());
    userRankInfoDto.setStructType(null);
    doReturn(userRankInfoDto).when(amazonS3Service).fetchAmazonS3CsvData(anyString(), anyString());
    when(promoConfigService.findById(any()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig).stream().findFirst());
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }

  @Test
  void handleUpdateKafkaMessageDataSetNullResponseTest() {
    promoMessageDto.setAction("Update");
    assertNotNull(promoConfigMessageHandler);
    PromoConfig promoConfig = new PromoConfig();
    promoConfig.setPromotionId(IConstantsTest.PROMOTION_ID);
    promoConfig.setLeaderboardId(promoMessageDto.getPromoLbConfigs().get(0).getLeaderboardId());
    UserRankInfoDto userRankInfoDto = new UserRankInfoDto();
    userRankInfoDto.setRowList(RequestUtilHelper.prepareUserRankInfo().getRowList());
    userRankInfoDto.setStructType(null);
    when(promoConfigService.findById(any()))
        .thenReturn(RequestUtilHelper.getPromoConfigs(promoConfig).stream().findFirst());
    doReturn(userRankInfoDto).when(amazonS3Service).fetchAmazonS3CsvData(anyString(), anyString());
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }

  @ParameterizedTest
  @ValueSource(strings = {"Delete", "dateChange", "OtherAction"})
  void handleDeleteKafkaMessageTest(String input) {
    promoMessageDto.setAction(input);
    assertNotNull(promoConfigMessageHandler);
    promoConfigMessageHandler.handleKafkaMessage(promoMessageDto);
  }
}
