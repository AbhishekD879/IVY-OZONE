package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "bybMarkets")
@Data
@EqualsAndHashCode(callSuper = true)
public class BybMarket extends SortableEntity implements HasBrand {

  @NotBlank private String name;
  private String lang = "en";
  @NotBlank private String brand;
  @NotBlank private String bybMarket;
  private Integer incidentGrouping;
  private Integer marketGrouping;
  private String marketType;
  private Boolean popularMarket;
  private String marketDescription;
  private String stat = "N/A";
}
