package com.coral.oxygen.middleware.pojos.model.cms;

import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toSet;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;
import lombok.Getter;

public class CmsSportData {

  @Getter private final List<SportItem> activeInplaySports;
  private final Set<String> enabledSportsIds;
  private final Set<String> disabledCategoryIds;

  private CmsSportData(List<SportItem> activeInplaySports, Set<String> disabledCategoryIds) {
    this.activeInplaySports = activeInplaySports;
    this.disabledCategoryIds = disabledCategoryIds;
    enabledSportsIds = activeInplaySports.stream().map(SportItem::getCategoryId).collect(toSet());
  }

  public static CmsSportData createFrom(
      List<SportItem> sportCategories, List<SportItem> olympicSports) {
    Map<Boolean, List<SportItem>> isSportCategoryEnabled =
        sportCategories.stream()
            .collect(groupingBy(category -> !category.isDisabled() && category.isShowInPlay()));
    List<SportItem> enabledSportCategories =
        isSportCategoryEnabled.getOrDefault(Boolean.TRUE, Collections.emptyList());

    Set<String> enabledCategoryIds =
        enabledSportCategories.stream().map(SportItem::getCategoryId).collect(toSet());

    Set<String> disabledCategoryIds =
        isSportCategoryEnabled.getOrDefault(Boolean.FALSE, Collections.emptyList()).stream()
            .map(SportItem::getCategoryId)
            .collect(toSet());

    List<SportItem> activeInplaySports =
        Stream.concat(
                enabledSportCategories.stream(),
                olympicSports.stream()
                    .filter(item -> !item.isDisabled())
                    .filter(SportItem::isShowInPlay)
                    .filter(item -> !disabledCategoryIds.contains(item.getCategoryId()))
                    .filter(item -> !enabledCategoryIds.contains(item.getCategoryId())))
            .collect(toList());

    return new CmsSportData(activeInplaySports, disabledCategoryIds);
  }

  // take ids from static list in case it`s not in disabled & enabled catIds lists -> at the end add
  // to enabled sportId lists
  public Set<String> getUniqueCategoryIdsIncluding(String[] categoriesIds) {
    return Stream.concat(
            Stream.of(categoriesIds)
                .filter(c -> !disabledCategoryIds.contains(c) && !enabledSportsIds.contains(c)),
            enabledSportsIds.stream())
        .collect(toSet());
  }
}
