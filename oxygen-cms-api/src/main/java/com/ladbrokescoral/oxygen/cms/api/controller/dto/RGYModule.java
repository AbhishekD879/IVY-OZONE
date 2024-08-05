package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class RGYModule {
  private String id;
  private String brand;
  private String moduleName;
  private boolean subModuleEnabled;
  private String aliasModuleNames;
  private List<AliasModuleNamesDto> aliasModules = new ArrayList<>();

  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<String> subModuleIds;

  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<RGYModule> subModules;
}
