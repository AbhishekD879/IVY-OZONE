package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.Filters;
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "sporttabs")
@Data
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
// FIXME: uncomment after v108.
// make sure to remove {@link DatabaseChangeLog#removeDuplicateTabs} and dependecies
// @CompoundIndex(
//     name = "brand_sport_name_unique",
//     def = "{'brand' : 1, 'sportId': 1, 'name': 1}",
//     unique = true)
public class SportTab extends SortableEntity implements HasBrand {

  private String brand;
  private Integer sportId; // site serve category id
  private String name;
  private String displayName;
  private boolean enabled;
  private boolean checkEvents;
  private boolean hasEvents;
  private List<SportTabMarket> marketsNames = new ArrayList<>();
  private InitialBanner interstitialBanners;

  @DBRef private List<TrendingTab> trendingTabs = new ArrayList<>();
  private Boolean showNewFlag;

  @JsonInclude(Include.NON_NULL)
  private Filters filters;

  public boolean isHidden() {
    return !this.enabled || this.checkEvents && !this.hasEvents;
  }
}
