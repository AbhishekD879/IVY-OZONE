package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class CreatePotsRequestDto {

  private Integer categoryId;
  private List<String> eventIds;

  private CreatePotsCampaignDto campaign;
}
