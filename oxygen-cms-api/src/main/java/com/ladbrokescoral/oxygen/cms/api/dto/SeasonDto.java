package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;

@Data
public class SeasonDto {
  private String id;
  private String brand;
  private String seasonName;
  private String seasonInfo;
  private Instant displayFrom;
  private Instant displayTo;
}
