package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.YourCallLeagueRepository;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class YourCallLeagueService extends SortableService<YourCallLeague> {

  private final YourCallLeagueRepository yourCallLeagueRepository;

  @Autowired
  public YourCallLeagueService(YourCallLeagueRepository yourCallLeagueRepository) {
    super(yourCallLeagueRepository);
    this.yourCallLeagueRepository = yourCallLeagueRepository;
  }

  @Override
  public YourCallLeague prepareModelBeforeSave(YourCallLeague entity) {
    validateTypeId(entity);
    return entity;
  }

  private void validateTypeId(YourCallLeague entity) {
    yourCallLeagueRepository.findAllByBrandAndTypeId(entity.getBrand(), entity.getTypeId()).stream()
        .filter(league -> !league.getId().equals(entity.getId()))
        .findAny()
        .ifPresent(
            league -> {
              throw new ValidationException(
                  String.format("League with type id: %s is already present", league.getTypeId()));
            });
  }

  public List<YourCallLeague> findAllByBrandSorted(String brand) {
    return yourCallLeagueRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }

  public Set<Long> findDisabledBuildYourBetLeaguesIds(String brand) {
    Collection<YourCallLeague> disabledLeagues =
        yourCallLeagueRepository.findAllByBrandAndEnabledFalse(brand);
    if (disabledLeagues == null || disabledLeagues.isEmpty()) {
      return Collections.emptySet();
    } else {
      return disabledLeagues.stream()
          .map(YourCallLeague::getTypeId)
          .map(Long::valueOf)
          .collect(Collectors.toSet());
    }
  }
}
