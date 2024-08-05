package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class PopularAccaWidgetDataDto extends AbstractDto {

  private String id;
  private String title;
  private String subTitle;
  private String svgId;
  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;
  private Double sortOrder;

  private List<String> locations;

  private String numberOfTimeBackedLabel;
  private Integer numberOfTimeBackedThreshold;

  private String accaIdsType;
  private List<String> listOfIds;
  private List<String> marketTemplateIds;
  private Integer accaRangeMin;
  private Integer accaRangeMax;
}
