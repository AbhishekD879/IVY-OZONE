package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "leagues")
@Data
@EqualsAndHashCode(callSuper = true)
public class League extends SortableEntity implements HasBrand {
  @NotBlank private String name;
  private String ssCategoryCode;
  private String betBuilderUrl;
  private String leagueUrl;
  private String lang = "en";
  private String brand = "bma";
  private String categoryId;
  private Integer typeId;
  private String banner;
  private String redirectionUrl;
  private String tabletBanner;
}
