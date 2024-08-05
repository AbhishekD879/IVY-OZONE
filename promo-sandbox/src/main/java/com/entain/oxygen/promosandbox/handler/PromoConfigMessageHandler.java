package com.entain.oxygen.promosandbox.handler;

import com.entain.oxygen.promosandbox.dto.LeaderboardConfigDto;
import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.dto.StatusDto;
import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.enums.KafkaAction;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.service.*;
import com.entain.oxygen.promosandbox.utils.PromoLbUtil;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class PromoConfigMessageHandler {

  private final HouseKeepingService houseKeepingService;

  private final PromoConfigService promoConfigService;

  private final RddCreationService rddCreationService;

  private final AmazonS3Service amazonS3Service;

  private final CacheManagerService cacheManagerService;

  @Autowired
  public PromoConfigMessageHandler(
      HouseKeepingService houseKeepingService,
      PromoConfigService promoConfigService,
      RddCreationService rddCreationService,
      AmazonS3Service amazonS3Service,
      CacheManagerService cacheManagerService) {
    this.houseKeepingService = houseKeepingService;
    this.promoConfigService = promoConfigService;
    this.rddCreationService = rddCreationService;
    this.amazonS3Service = amazonS3Service;
    this.cacheManagerService = cacheManagerService;
  }

  public void handleKafkaMessage(PromoMessageDto promoMsgDto) {
    List<LeaderboardConfigDto> lbConfigs = promoMsgDto.getPromoLbConfigs();
    if (KafkaAction.CREATE.getValue().equals(promoMsgDto.getAction())) {
      lbConfigs.forEach(
          (LeaderboardConfigDto lbConfig) -> {
            StatusDto status =
                fetchAmazonS3CsvDataAndCreateRdd(
                    promoMsgDto.getPromotionId(),
                    lbConfig.getFilePath(),
                    lbConfig.getLeaderboardId());
            promoConfigService.savePromoConfig(promoMsgDto, lbConfig, status);
          });
    } else if (KafkaAction.UPDATE.getValue().equals(promoMsgDto.getAction())) {
      lbConfigs.forEach(
          (LeaderboardConfigDto lbConfig) ->
              promoConfigService
                  .findById(
                      PromoLbUtil.computePrimaryKey(
                          promoMsgDto.getPromotionId(), lbConfig.getLeaderboardId()))
                  .ifPresent(
                      (PromoConfig promoConfig) -> {
                        StatusDto status =
                            fetchAmazonS3CsvDataAndCreateRdd(
                                promoMsgDto.getPromotionId(),
                                lbConfig.getFilePath(),
                                lbConfig.getLeaderboardId());
                        promoConfigService.updatePromoConfig(
                            promoConfig, promoMsgDto, lbConfig, status);
                      }));
      cacheManagerService.clearCache();
    } else if (KafkaAction.DELETE.getValue().equals(promoMsgDto.getAction())) {
      lbConfigs.forEach(
          (LeaderboardConfigDto lbConfig) -> {
            boolean status =
                houseKeepingService.dropSparkTempTable(
                    promoMsgDto.getPromotionId(), lbConfig.getLeaderboardId());
            promoConfigService.updatePromoIsDataCleanupStatus(
                PromoLbUtil.computePrimaryKey(
                    promoMsgDto.getPromotionId(), lbConfig.getLeaderboardId()),
                status);
          });
    } else if (KafkaAction.PROMO_DATE_CHANGE.getValue().equals(promoMsgDto.getAction())) {
      promoConfigService.updatePromoStartEndDate(promoMsgDto);
    }
  }

  private StatusDto fetchAmazonS3CsvDataAndCreateRdd(
      String promotionId, String filePath, String leaderboardId) {
    boolean status = false;
    UserRankInfoDto userRankDetails = amazonS3Service.fetchAmazonS3CsvData(promotionId, filePath);
    int noOfRecord = 0;
    if (PromoLbUtil.isDataExist(userRankDetails)) {
      status = rddCreationService.createPromoUserRDD(userRankDetails, promotionId, leaderboardId);
      noOfRecord = userRankDetails.getRowList().size();
    }
    return new StatusDto(status, userRankDetails.getLastFileModified(), noOfRecord);
  }
}
