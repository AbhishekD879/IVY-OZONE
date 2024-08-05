package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import lombok.Data;

@Data
public class CreatePotsCampaignDto {

  private String id;

  private String name;

  private Instant displayFrom;

  private Instant displayTo;

  private List<CreatePotsQuestionDto> questions;
}
