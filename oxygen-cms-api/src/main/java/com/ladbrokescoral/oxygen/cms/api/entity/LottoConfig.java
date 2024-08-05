package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(value = "lottoconfig")
@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class LottoConfig extends SortableEntity implements HasBrand {

  @Brand private String brand;
  private String ssMappingId;
  @NotNull private String label;
  private String infoMessage;
  private String nextLink;
  private String bannerLink;
  private String svgId;
  private String bannerText;
  private boolean isEnabled;
  private Integer dayCount;
  private Double maxPayOut;
}
