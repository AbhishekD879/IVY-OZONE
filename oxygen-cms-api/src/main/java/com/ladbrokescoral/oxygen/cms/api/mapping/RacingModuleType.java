package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.Getter;

@Getter
public enum RacingModuleType {
  UK_AND_IRISH_RACES("UK and Irish Races", "UIR", Arrays.asList(Brand.BMA, Brand.LADBROKES)),
  INTERNATIONAL_TOTE_CAROUSEL(
      "International Tote Carousel", "ITC", Arrays.asList(Brand.BMA, Brand.LADBROKES)),
  INTERNATIONAL_RACES("International Races", "IR", Arrays.asList(Brand.BMA, Brand.LADBROKES)),
  VIRTUAL_RACE_CAROUSEL("Virtual Race Carousel", "VRC", Arrays.asList(Brand.BMA, Brand.LADBROKES)),
  CORAL_LEGENDS("Coral Legends", "LVR", Collections.singletonList(Brand.BMA)),
  LADBROKES_LEGENDS("Ladbrokes Legends", "LVR", Collections.singletonList(Brand.LADBROKES));

  private String title;
  private String abbreviation;
  private List<String> brands;

  RacingModuleType(String title, String abbreviation, List<String> brands) {
    this.title = title;
    this.abbreviation = abbreviation;
    this.brands = brands;
  }

  public static List<RacingModuleType> getRacingTypes(String brand) {
    return Stream.of(values())
        .filter(val -> val.getBrands().contains(brand))
        .collect(Collectors.toList());
  }
}
