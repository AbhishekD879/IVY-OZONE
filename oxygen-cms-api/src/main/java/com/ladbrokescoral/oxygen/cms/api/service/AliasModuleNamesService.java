package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.mapping.AliasModuleNamesMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.ExtraNavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkRepository;
import java.time.Instant;
import java.util.Arrays;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class AliasModuleNamesService {

  private final SportQuickLinkRepository sportQuickLinkRepository;

  private final NavigationPointRepository superButtonRepository;

  private final ExtraNavigationPointRepository specialSuperButtonRepository;

  public Map<AliasModuleTypes, List<AliasModuleNamesDto>> readQLAndSB(String brand) {
    List<AliasModuleNamesDto> quickLinks;
    List<AliasModuleNamesDto> superButtons;
    Map<AliasModuleTypes, List<AliasModuleNamesDto>> result = new EnumMap<>(AliasModuleTypes.class);

    Predicate<SportQuickLink> sportQuickLinkPredicate =
        sportQuickLink ->
            (!sportQuickLink.isDisabled())
                && (Instant.now().isBefore(sportQuickLink.getValidityPeriodEnd()));
    Predicate<NavigationPoint> superButtonPredicate =
        navigationPoint ->
            (navigationPoint.isEnabled())
                && (Instant.now().isBefore(navigationPoint.getValidityPeriodEnd()));
    Predicate<ExtraNavigationPoint> specialSuperButtonPredicate =
        extraNavigationPoint ->
            (extraNavigationPoint.isEnabled())
                && (Instant.now().isBefore(extraNavigationPoint.getValidityPeriodEnd()));
    quickLinks =
        this.sportQuickLinkRepository
            .findAllByBrandAndPageTypeIn(brand, Arrays.asList(PageType.sport, PageType.eventhub))
            .stream()
            .filter(sportQuickLinkPredicate)
            .map(AliasModuleNamesMapper.MAPPER::toQLDto)
            .collect(Collectors.toList());

    superButtons =
        this.superButtonRepository.findByBrand(brand).stream()
            .filter(superButtonPredicate)
            .map(AliasModuleNamesMapper.MAPPER::toSBDto)
            .collect(Collectors.toList());

    if (Brand.LADBROKES.equalsIgnoreCase(brand)) {
      superButtons =
          Stream.concat(
                  this.superButtonRepository.findByBrand(brand).stream()
                      .filter(superButtonPredicate)
                      .map(AliasModuleNamesMapper.MAPPER::toSBDto),
                  this.specialSuperButtonRepository.findByBrand(brand).stream()
                      .filter(specialSuperButtonPredicate)
                      .map(AliasModuleNamesMapper.MAPPER::toSSBDto))
              .collect(Collectors.toList());
    }

    result.put(AliasModuleTypes.QL, quickLinks);
    result.put(AliasModuleTypes.SB, superButtons);

    return result;
  }
}
