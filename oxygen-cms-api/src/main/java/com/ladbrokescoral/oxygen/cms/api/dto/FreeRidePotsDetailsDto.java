package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class FreeRidePotsDetailsDto {
  private String potId;
  private List<HorseDetails> horses;
}
