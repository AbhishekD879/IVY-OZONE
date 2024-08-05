package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "rgy-configurations")
@Data
@EqualsAndHashCode(callSuper = false)
public class RGYConfigurationEntity extends SortableEntity implements HasBrand {
  @Indexed private String brand;
  @Indexed private int reasonCode;
  @Indexed private int riskLevelCode;
  private String riskLevelDesc;
  private String reasonDesc;

  @JsonProperty("enabled")
  @Indexed
  private boolean bonusSuppression;

  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<String> moduleIds;

  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<RGYModule> modules;
}
