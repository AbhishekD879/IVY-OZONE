package com.ladbrokescoral.oxygen.cms.api.service;

import static java.util.stream.Collectors.toList;

import com.ladbrokescoral.oxygen.cms.Application;
import com.ladbrokescoral.oxygen.cms.api.dto.TierCacheDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.mapping.TierCacheMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;
import javax.annotation.PostConstruct;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Component;

@Component
@DependsOn(Application.MONGOCK)
public class TierCategoriesCache {

  private final SportCategoryRepository repository;
  private final TierCacheMapper mapper;
  private final ConcurrentHashMap<BrandedTierKey, List<SportCategory>> categoriesByTier;

  @Autowired
  public TierCategoriesCache(SportCategoryRepository repository) {
    this.repository = repository;
    this.categoriesByTier = new ConcurrentHashMap<>();
    this.mapper = new TierCacheMapper();
  }

  // FIXME: rework: use Mongo events on chnage to avoid overkill / AfterSaveEvent ??
  @PostConstruct
  public void refreshCategoryIdsCache() {
    categoriesByTier.clear();
    categoriesByTier.putAll(
        repository.findAll().stream()
            .filter(category -> category.getBrand() != null)
            .filter(category -> category.getTier() != null)
            .collect(
                Collectors.groupingBy(
                    category -> new BrandedTierKey(category.getBrand(), category.getTier()),
                    Collectors.collectingAndThen(toList(), Collections::unmodifiableList))));
  }

  public Set<Integer> getCategoryIds(String brand, SportTier tier) {
    return getCategories(brand, tier).stream()
        .map(SportCategory::getCategoryId)
        .collect(Collectors.toSet());
  }

  public List<SportCategory> getCategories(String brand, SportTier tier) {
    return categoriesByTier.getOrDefault(new BrandedTierKey(brand, tier), Collections.emptyList());
  }

  public List<TierCacheDto> getCacheView() {
    return mapper.toDto(categoriesByTier);
  }

  // FIXME: hash of hash ? why ? overkill here
  @ToString(of = {"brand", "tier"})
  @Getter
  @EqualsAndHashCode(of = {"hash"})
  public static class BrandedTierKey {
    private int hash;
    private String brand;
    private SportTier tier;

    BrandedTierKey(String brand, SportTier tier) {
      this.brand = brand;
      this.tier = tier;
      this.hash = Objects.hash(brand, tier);
    }
  }
}
