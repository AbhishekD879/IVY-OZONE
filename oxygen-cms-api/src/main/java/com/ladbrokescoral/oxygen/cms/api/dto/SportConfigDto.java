package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.util.Map;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;

@Data
@NoArgsConstructor
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SportConfigDto {
  private String title;
  private String name;
  private String path;
  private Integer tier;
  private String categoryType;

  @JsonProperty("isOutrightSport")
  private boolean outrightSport;

  @JsonProperty("isMultiTemplateSport")
  private boolean multiTemplateSport;

  private String oddsCardHeaderType;

  @JsonProperty("request")
  private SSRequestFilters requestFilters;

  @JsonProperty("tabs")
  private Map<String, SSTabRequestFilters> tabRequestsFilters;

  // FIXME: need rework. use lombok
  public static Builder builder() {
    return new Builder();
  }

  // FIXME: need rework. use lombok
  public static class Builder {
    private String title;
    private String name;
    private String path;
    private Integer tier;
    private String categoryType;
    private boolean outrightSport;
    private boolean multiTemplateSport;
    private String oddsCardHeaderType;
    private SSRequestFilters requestFilters;
    private TabFiltersBuilder tabFiltersBuilder;

    public Builder config(SportCategory sportCategory) {
      this.title = sportCategory.getImageTitle();
      this.path = pathFromUri(sportCategory.getTargetUri());
      this.name = this.path.replaceAll("\\W", "");
      this.tier = sportCategory.getTier() != null ? sportCategory.getTier().value : null;
      this.categoryType = "gaming";
      this.oddsCardHeaderType = "";
      if (sportCategory.getOddsCardHeaderType() != null) {
        this.oddsCardHeaderType = sportCategory.getOddsCardHeaderType().value;
      }
      this.multiTemplateSport = sportCategory.isMultiTemplateSport();
      this.outrightSport = sportCategory.isOutrightSport();
      this.requestFilters = new SSRequestFilters(sportCategory);
      this.tabFiltersBuilder = new TabFiltersBuilder(sportCategory);
      tabFiltersBuilder.build();
      return this;
    }

    /**
     * @param uri "/sport/ice-hockey"
     * @return "ice-hockey"
     */
    private String pathFromUri(String uri) {
      if (uri == null) {
        return "";
      }
      return StringUtils.substringAfterLast(uri, "/");
    }

    public SportConfigDto build() {
      return new SportConfigDto(
          title,
          name,
          path,
          tier,
          categoryType,
          outrightSport,
          multiTemplateSport,
          oddsCardHeaderType,
          requestFilters,
          tabFiltersBuilder.getTabRequestsFilters());
    }
  }

  @Getter
  @AllArgsConstructor
  @EqualsAndHashCode
  @JsonInclude(JsonInclude.Include.NON_NULL)
  private static class SSRequestFilters {
    private String categoryId;
    private String siteChannels = "M";
    private Boolean marketsCount;

    @JsonProperty("isActive")
    private Boolean active;

    private String[] dispSortName;
    private String[] dispSortNameIncludeOnly;
    private String typeIds;

    @JsonProperty("marketTemplateMarketNameIntersects")
    private String primaryMarkets;

    SSRequestFilters(SportCategory sportCategory) {
      this.categoryId = String.valueOf(sportCategory.getCategoryId());
      this.marketsCount = !sportCategory.isOutrightSport();
      this.active = sportCategory.isOutrightSport();
      if (!sportCategory.isOutrightSport()) {
        if (sportCategory.getDispSortNames() != null) {
          String[] dispSortNameFilters = sportCategory.getDispSortNames().split("\\W+");
          this.dispSortName = dispSortNameFilters;
          this.dispSortNameIncludeOnly = dispSortNameFilters;
        }
        this.primaryMarkets = sportCategory.getPrimaryMarkets();
      }
      this.typeIds = sportCategory.getTypeIds();
    }
  }
}
