package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InitialSportConfigDto {

  private String title;
  private String name;
  private String path;
  private Integer tier;

  @JsonProperty("isOutrightSport")
  private boolean outrightSport;

  @JsonProperty("isMultiTemplateSport")
  private boolean multiTemplateSport;

  private String oddsCardHeaderType;
  private SSRequestFilters request;

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class SSRequestFilters {
    private String categoryId;
    private String siteChannels = "M";
    private Boolean marketsCount;
    private String[] dispSortName;
    private String[] dispSortNameIncludeOnly;
    private String marketTemplateMarketNameIntersects;
    private List<Map<String, String>> aggregatedMarkets;
  }
}
