package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TierCacheDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class TierCacheMapper {
  public List<TierCacheDto> toDto(
      Map<TierCategoriesCache.BrandedTierKey, List<SportCategory>> tierCategories) {
    if (tierCategories == null) {
      return Collections.emptyList();
    }
    return tierCategories.keySet().stream()
        .map(
            key ->
                TierCacheDto.builder()
                    .brand(key.getBrand())
                    .tier(key.getTier())
                    .sports(tierCategories.get(key))
                    .build())
        .sorted(Comparator.comparing(TierCacheDto::getBrand).thenComparing(TierCacheDto::getTier))
        .collect(Collectors.toList());
  }
}
