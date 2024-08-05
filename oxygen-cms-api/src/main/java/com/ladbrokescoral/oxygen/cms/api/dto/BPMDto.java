package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.List;
import lombok.Data;

@Data
public class BPMDto {
  private List<String> betpackNames;
  @JsonIgnore private boolean isFilterAssociated;
}
