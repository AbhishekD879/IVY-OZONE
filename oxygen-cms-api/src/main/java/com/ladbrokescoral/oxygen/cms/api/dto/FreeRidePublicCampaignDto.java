package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.freeride.Questionnarie;
import java.time.Instant;
import lombok.Data;

@Data
public class FreeRidePublicCampaignDto {

  private String id;

  private String name;
  private String brand;

  private Instant displayFrom;
  private Instant displayTo;

  private Boolean isPotsCreated;
  private Questionnarie questionnarie;
}
