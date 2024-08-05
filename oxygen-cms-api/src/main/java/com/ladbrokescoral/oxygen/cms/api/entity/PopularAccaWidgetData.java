package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "popularAccaWidgetData")
@EqualsAndHashCode(callSuper = true)
public class PopularAccaWidgetData extends SortableEntity implements HasBrand {

  @Brand public String brand;

  private String title;
  private String subTitle;
  private String svgId;
  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;

  private List<String> locations;

  private String numberOfTimeBackedLabel;
  private Integer numberOfTimeBackedThreshold;

  private String accaIdsType;
  private List<String> listOfIds;
  private List<String> marketTemplateIds;
  private Integer accaRangeMin;
  private Integer accaRangeMax;
}
