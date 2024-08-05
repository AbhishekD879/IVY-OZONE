package com.entain.oxygen.promosandbox.service;

import com.entain.oxygen.promosandbox.dto.LeaderboardConfigDto;
import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.dto.StatusDto;
import com.entain.oxygen.promosandbox.enums.FileProcessStatus;
import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.repository.PromoConfigRepository;
import com.entain.oxygen.promosandbox.utils.PromoLbUtil;
import java.time.Instant;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class PromoConfigService {

  private final PromoConfigRepository promoConfigRepository;

  @Autowired
  public PromoConfigService(PromoConfigRepository promoConfigRepository) {
    this.promoConfigRepository = promoConfigRepository;
  }

  public void savePromoConfig(
      PromoMessageDto promoMessageDto, LeaderboardConfigDto lbConfigDto, StatusDto statusDto) {
    PromoConfig promoConfig = new PromoConfig();
    promoConfig.setId(
        PromoLbUtil.computePrimaryKey(
            promoMessageDto.getPromotionId(), lbConfigDto.getLeaderboardId()));
    promoConfig.setPromotionId(promoMessageDto.getPromotionId());
    promoConfig.setBrand(promoMessageDto.getBrand());
    promoConfig.setFilePath(lbConfigDto.getFilePath());
    promoConfig.setLeaderboardId(lbConfigDto.getLeaderboardId());
    promoConfig.setStartDate(convertStringToInstant(promoMessageDto.getStartDate()));
    promoConfig.setEndDate(convertStringToInstant(promoMessageDto.getEndDate()));
    promoConfig.setLastFileModified(statusDto.getLastFileModified());
    promoConfig.setNoOfRecord(statusDto.getNoOfRecord());
    promoConfig.setCreatedAt(Instant.now());
    promoConfig.setUpdatedAt(Instant.now());
    promoConfig.setFileProcessStatus(evaluateStatus(statusDto.getStatus()));
    promoConfigRepository.save(promoConfig);
    log.info(
        "PromoConfig save successfully to mongoDB promotionId: {} ,leaderboardId : {} ",
        promoConfig.getPromotionId(),
        lbConfigDto.getLeaderboardId());
  }

  public void updatePromoConfig(
      PromoConfig promoConfig,
      PromoMessageDto promoMessageDto,
      LeaderboardConfigDto lbConfigDto,
      StatusDto statusDto) {
    promoConfig.setFilePath(lbConfigDto.getFilePath());
    promoConfig.setStartDate(convertStringToInstant(promoMessageDto.getStartDate()));
    promoConfig.setEndDate(convertStringToInstant(promoMessageDto.getEndDate()));
    promoConfig.setLastFileModified(statusDto.getLastFileModified());
    promoConfig.setFileProcessStatus(evaluateStatus(statusDto.getStatus()));
    promoConfig.setNoOfRecord(statusDto.getNoOfRecord());
    promoConfig.setUpdatedAt(Instant.now());
    promoConfigRepository.save(promoConfig);
    log.info(
        "PromoConfig updated successfully to mongoDB promotionId: {},leaderboardId: {} ",
        promoConfig.getPromotionId(),
        lbConfigDto.getLeaderboardId());
  }

  public void updatePromoStartEndDate(PromoMessageDto promoMessageDto) {
    promoConfigRepository
        .findAllByPromotionId(promoMessageDto.getPromotionId())
        .forEach(
            (PromoConfig promoConfig) -> {
              promoConfig.setStartDate(convertStringToInstant(promoMessageDto.getStartDate()));
              promoConfig.setEndDate(convertStringToInstant(promoMessageDto.getEndDate()));
              promoConfig.setUpdatedAt(Instant.now());
              promoConfigRepository.save(promoConfig);
              log.info(
                  "PromoConfig start/endDate updated successfully to mongoDB promotionId: {} ,leaderboardId : {} ",
                  promoConfig.getPromotionId(),
                  promoConfig.getLeaderboardId());
            });
  }

  public void updatePromoIsDataCleanupStatus(String primaryKey, boolean status) {
    promoConfigRepository
        .findById(primaryKey)
        .ifPresent(
            (PromoConfig promoConfig) -> {
              promoConfig.setDataCleaned(status);
              promoConfig.setUpdatedAt(Instant.now());
              promoConfigRepository.save(promoConfig);
              log.info(
                  "PromoConfig isDateCleanupStatus updated as {} to mongoDB promotionId: {} ,leaderboardId : {} ",
                  status,
                  promoConfig.getPromotionId(),
                  promoConfig.getLeaderboardId());
            });
  }

  public void updatePromoFileStatus(String primaryKey, StatusDto status) {
    promoConfigRepository
        .findById(primaryKey)
        .ifPresent(
            (PromoConfig promoConfig) -> {
              promoConfig.setFileProcessStatus(evaluateStatus(status.getStatus()));
              promoConfig.setUpdatedAt(Instant.now());
              promoConfig.setLastFileModified(status.getLastFileModified());
              promoConfigRepository.save(promoConfig);
              log.info(
                  "PromoConfig fileStatus updated as {} to mongoDB promotionId: {},leaderboardId : {} ",
                  promoConfig.getFileProcessStatus(),
                  promoConfig.getPromotionId(),
                  promoConfig.getLeaderboardId());
            });
  }

  public List<PromoConfig> findAllByBrandAndDataCleanupStatus(
      String brand, boolean dataCleanupStatus) {
    return promoConfigRepository.findAllByBrandAndIsDataCleaned(brand, dataCleanupStatus);
  }

  private Instant convertStringToInstant(String date) {
    return Instant.parse(date);
  }

  private String evaluateStatus(Boolean status) {
    return Boolean.TRUE.equals(status)
        ? FileProcessStatus.SUCCESS.getValue()
        : FileProcessStatus.FAILURE.getValue();
  }

  public Optional<Instant> getLastFileModified(String promotionId, String leaderboardId) {
    return promoConfigRepository
        .findById(PromoLbUtil.computePrimaryKey(promotionId, leaderboardId))
        .map(PromoConfig::getLastFileModified);
  }

  public Optional<PromoConfig> findById(String primaryKey) {
    return promoConfigRepository.findById(primaryKey);
  }
}
