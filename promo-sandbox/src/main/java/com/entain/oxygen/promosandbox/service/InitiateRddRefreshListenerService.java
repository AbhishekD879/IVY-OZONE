package com.entain.oxygen.promosandbox.service;

import com.entain.oxygen.promosandbox.dto.StatusDto;
import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.repository.PromoConfigRepository;
import com.entain.oxygen.promosandbox.utils.PromoLbUtil;
import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class InitiateRddRefreshListenerService implements ApplicationRunner {

  private final PromoConfigRepository promoConfigRepository;

  private final RddCreationService rddCreationService;

  private final PromoConfigService promoConfigService;

  private final AmazonS3Service amazonS3Service;

  @Value("${cms.brand}")
  private String brand;

  @Autowired
  public InitiateRddRefreshListenerService(
      PromoConfigRepository promoConfigRepository,
      RddCreationService rddCreationService,
      PromoConfigService promoConfigService,
      AmazonS3Service amazonS3Service) {
    this.promoConfigRepository = promoConfigRepository;
    this.rddCreationService = rddCreationService;
    this.promoConfigService = promoConfigService;
    this.amazonS3Service = amazonS3Service;
  }

  @Override
  public void run(ApplicationArguments args) {
    try {
      List<PromoConfig> currentFuturePromotions =
          promoConfigRepository.findAllByBrandAndIsDataCleaned(brand, false).stream()
              .filter(
                  promoConfig ->
                      promoConfig.getEndDate().getEpochSecond() >= Instant.now().getEpochSecond())
              .collect(Collectors.toList());
      log.info(
          "Eligible promoId for reload data to spark from amazonS3 on application startup.PromotionsCount : {} ",
          currentFuturePromotions.size());
      if (!currentFuturePromotions.isEmpty()) {
        currentFuturePromotions.forEach(
            (PromoConfig promoConfig) -> {
              UserRankInfoDto userRankDetails =
                  amazonS3Service.fetchAmazonS3CsvData(
                      promoConfig.getPromotionId(), promoConfig.getFilePath());
              boolean status = false;
              if (PromoLbUtil.isDataExist(userRankDetails)) {
                status =
                    rddCreationService.createPromoUserRDD(
                        userRankDetails,
                        promoConfig.getPromotionId(),
                        promoConfig.getLeaderboardId());
              }
              promoConfigService.updatePromoFileStatus(
                  PromoLbUtil.computePrimaryKey(
                      promoConfig.getPromotionId(), promoConfig.getLeaderboardId()),
                  new StatusDto(status, userRankDetails.getLastFileModified()));
            });
      }
    } catch (Exception ex) {
      log.error("Error while recreating rdd on application startup : {} ", ex.getMessage());
    }
  }
}
