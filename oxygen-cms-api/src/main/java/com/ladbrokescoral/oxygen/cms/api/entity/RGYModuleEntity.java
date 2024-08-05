package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "rgy-modules")
public class RGYModuleEntity extends SortableEntity implements HasBrand {
  @Indexed private String brand;
  private String moduleName;
  @Indexed private boolean subModuleEnabled;
  private String aliasModuleNames;
  private List<AliasModuleNamesDto> aliasModules = new ArrayList<>();

  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<String> subModuleIds;

  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<RGYModule> subModules;
}
