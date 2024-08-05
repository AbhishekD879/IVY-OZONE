package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.*;
import lombok.Data;

@Data
@JsonIgnoreProperties(
    value = {
      "moduleName",
      "moduleDiscription",
      "id",
      "createdBy",
      "createdByUserName",
      "updatedAt",
      "updatedBy",
      "updatedByUserName",
      "createdAt"
    })
public class FirstBetPlaceCFDto extends FirstBetPlaceTutorialDto {}
