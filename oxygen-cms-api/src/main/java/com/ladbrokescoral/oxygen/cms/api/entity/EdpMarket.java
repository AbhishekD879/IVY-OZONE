package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "edpmarkets")
@Data
@EqualsAndHashCode(callSuper = true)
public class EdpMarket extends SortableEntity implements HasBrand {
  @NotBlank private String name;
  private String lang = "en";
  @NotBlank private String brand;
  private boolean lastItem;
  private String marketId;
}
