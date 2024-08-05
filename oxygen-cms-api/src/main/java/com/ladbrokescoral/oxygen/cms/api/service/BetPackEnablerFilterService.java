package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.BPMDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackFilterDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerFilterRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.time.Instant;
import java.util.ArrayList;
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
public class BetPackEnablerFilterService extends SortableService<BetPackFilter> {

  @Value(value = "${bpmp.active-filter-limit}")
  private int activeFilterLimit;

  BetPackEnablerFilterRepository betPackEnablerFilterRepository;

  public BetPackEnablerFilterService(
      CustomMongoRepository<BetPackFilter> mongoRepository,
      BetPackEnablerFilterRepository betPackEnablerFilterRepository) {
    super(mongoRepository);
    this.betPackEnablerFilterRepository = betPackEnablerFilterRepository;
  }

  public List<BetPackFilter> findAllActiveBetPackFilter(String brand) {
    return betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(brand);
  }

  public Long deleteByFilterName(String filterName) {
    return betPackEnablerFilterRepository.deleteByFilterName(filterName);
  }

  public BetPackFilter checkActiveFilterLimit(String id, BetPackFilterDto filterDto) {
    if (filterDto.isFilterActive()) {
      Map<String, BetPackFilter> filterMap =
          betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(filterDto.getBrand())
              .stream()
              .collect(Collectors.toMap(BetPackFilter::getId, f -> f));
      if ((StringUtils.isBlank(id) || !isCurrentFilterActive(filterMap.get(id)))
          && (filterMap.size() >= activeFilterLimit)) {
        log.error(
            String.format(
                "Maximum limit for Active Filter(%s) already reached", activeFilterLimit));
        throw new BetPackMarketPlaceException(
            String.format(
                "Maximum limit for Active Filter(%s) already reached", activeFilterLimit));
      }
    }
    BetPackFilter filterEntity = new BetPackFilter();
    BeanUtils.copyProperties(filterDto, filterEntity);
    return filterEntity;
  }

  private static boolean isCurrentFilterActive(BetPackFilter currentFilter) {
    return currentFilter != null && currentFilter.isFilterActive();
  }

  public void validateSortOrder(BetPackFilterDto betPackFilterDto) {
    if (null == betPackFilterDto.getSortOrder()) {
      log.error("SortOrder should not be :{}", betPackFilterDto.getSortOrder());
      throw new BetPackMarketPlaceException(
          "Sort Order should not be : " + betPackFilterDto.getSortOrder());
    }
  }

  public BPMDto getFilterStatus(
      String filterName, BPMDto bpmDto, List<BetPackEntity> allBetPackEntities) {
    List<String> betpacks = new ArrayList<>();
    allBetPackEntities.forEach(
        entity ->
            entity
                .getFilterList()
                .forEach(
                    (String filter) -> {
                      if (filter.equalsIgnoreCase(filterName)
                          && Instant.now().isBefore(entity.getBetPackEndDate())) {
                        betpacks.add(entity.getBetPackTitle());
                        bpmDto.setFilterAssociated(true);
                      }
                      bpmDto.setBetpackNames(betpacks);
                    }));
    return bpmDto;
  }
}
