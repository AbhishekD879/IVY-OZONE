package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.BetPackDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class BetPackMarketPlaceService extends SortableService<BetPackEntity> {

  @Value(value = "${bpmp.active-betpack-limit}")
  private int activeBetPackLimit;

  private final BetPackEnablerRepository betPackEnablerRepository;

  public BetPackMarketPlaceService(
      CustomMongoRepository<BetPackEntity> mongoRepository,
      BetPackEnablerRepository betPackEnablerRepository) {
    super(mongoRepository);
    this.betPackEnablerRepository = betPackEnablerRepository;
  }

  public List<BetPackEntity> findAllBetPackEntities() {

    return betPackEnablerRepository.findAll();
  }

  public List<String> getActiveBetPackId(String brand) {
    List<BetPackEntity> betPackEntities =
        betPackEnablerRepository.findByBrandAndBetPackActiveTrue(brand);
    return betPackEntities.stream().map(BetPackEntity::getBetPackId).collect(Collectors.toList());
  }

  public List<BetPackEntity> findAllActiveBetPackEntities(String brand) {
    return betPackEnablerRepository.findByBrandAndBetPackActiveTrue(brand);
  }

  public List<BetPackEntity> findAllBetPacksBetweenDate(String brand) {
    return betPackEnablerRepository
        .findByBrandAndBetPackEndDateIsAfterOrMaxTokenExpirationDateIsAfter(
            brand, Instant.now(), Instant.now());
  }

  public BetPackEntity checkActiveBetPackLimit(String id, BetPackDto betPackDto) {
    if (betPackDto.isBetPackActive()) {
      Map<String, BetPackEntity> betPackMap =
          betPackEnablerRepository.findByBrandAndBetPackActiveTrue(betPackDto.getBrand()).stream()
              .collect(Collectors.toMap(BetPackEntity::getId, b -> b));
      if ((StringUtils.isBlank(id) || !isCurrentBetPackActive(betPackMap.get(id)))
          && (betPackMap.size() >= activeBetPackLimit)) {
        log.error(
            String.format(
                "Maximum limit for Active BetPack(%s) already reached", activeBetPackLimit));
        throw new BetPackMarketPlaceException(
            String.format(
                "Maximum limit for Active BetPack(%s) already reached", activeBetPackLimit));
      }
    }
    BetPackEntity betPackEntity = new BetPackEntity();
    BeanUtils.copyProperties(betPackDto, betPackEntity);
    return betPackEntity;
  }

  public BetPackEntity checkDateValidation(String id, BetPackDto betPackDto) {
    BetPackEntity entity =
        betPackEnablerRepository.findById(id).orElseThrow(NotFoundException::new);
    if (Instant.now().isAfter(betPackDto.getBetPackStartDate())) {
      betPackDto.setBetPackStartDate(entity.getBetPackStartDate());
    }
    BeanUtils.copyProperties(betPackDto, entity);
    return entity;
  }

  private static boolean isCurrentBetPackActive(BetPackEntity currentBetPack) {
    return currentBetPack != null && currentBetPack.isBetPackActive();
  }

  public void validateSortOrder(BetPackDto betPackDto) {
    if (null == betPackDto.getSortOrder()) {
      log.error("SortOrder should not be :{}", betPackDto.getSortOrder());
      throw new BetPackMarketPlaceException(
          "Sort Order should not be : " + betPackDto.getSortOrder());
    }
  }
}
