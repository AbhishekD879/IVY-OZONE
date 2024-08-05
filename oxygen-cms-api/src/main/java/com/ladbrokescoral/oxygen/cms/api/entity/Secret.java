package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "secrets")
@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true, callSuper = false)
@CompoundIndex(name = "brand_uri", def = "{'brand' : 1, 'uri': 1}", unique = true)
public class Secret extends AbstractEntity implements HasBrand {

  @EqualsAndHashCode.Include @NotBlank private String brand;
  @EqualsAndHashCode.Include @NotBlank private String uri;
  private String name;
  private boolean enabled;
  private List<SecretItem> items;
}
