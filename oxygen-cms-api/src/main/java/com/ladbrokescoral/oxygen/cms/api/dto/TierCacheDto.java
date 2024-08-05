package com.ladbrokescoral.oxygen.cms.api.dto;

import static java.util.stream.Collectors.toList;

import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
@JsonPropertyOrder({"brand", "tier", "sportIds", "sport"})
public class TierCacheDto {
  private String brand;
  private SportTier tier;
  private List<SportCategory> sports;

  public List<Integer> getSportIds() {
    return sports.stream().map(SportCategory::getCategoryId).sorted().collect(toList());
  }
}
