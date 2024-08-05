package com.ladbrokescoral.oxygen.cms.util;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

public class TierCategoriesHelper extends TierCategoriesCache {
  private final Map<SportTier, Set<Integer>> categoriesByTier;

  public TierCategoriesHelper() {
    super(null);
    this.categoriesByTier = new HashMap<>();
    this.categoriesByTier.put(SportTier.TIER_1, new HashSet<>(Arrays.asList(16, 6, 34)));
    this.categoriesByTier.put(
        SportTier.TIER_2,
        new HashSet<>(
            Arrays.asList(2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 32, 52)));
    this.categoriesByTier.put(SportTier.UNTIED, new HashSet<>(Arrays.asList(0, 9999, 19)));
  }

  public Set<Integer> getCategoryIds(SportTier tier) {
    return categoriesByTier.get(tier);
  }

  @Override
  public List<SportCategory> getCategories(String brand, SportTier tier) {
    return categoriesByTier.get(tier).stream()
        .map(sportId -> buildSportCategory(brand, sportId, tier))
        .collect(Collectors.toList());
  }

  public static SportCategory buildSportCategory(String brand, Integer sportId, SportTier tier) {
    SportCategory sport = new SportCategory();
    sport.setBrand(brand);
    sport.setCategoryId(sportId);
    sport.setTier(tier);
    return sport;
  }

  public Optional<SportCategory> find(String brand, Integer sportId) {
    return categoriesByTier.entrySet().stream()
        .filter(entry -> entry.getValue().contains(sportId))
        .findFirst()
        .map(entry -> buildSportCategory(brand, sportId, entry.getKey()));
  }
}
