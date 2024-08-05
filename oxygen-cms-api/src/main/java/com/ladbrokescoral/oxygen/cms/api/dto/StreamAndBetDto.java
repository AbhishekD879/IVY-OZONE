package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class StreamAndBetDto {
  private List<SABChildElementDto> children;

  // StreamAndBet Child Element, basically a Node in categories tree
  @Data
  @NoArgsConstructor
  public static class SABChildElementDto {
    private Integer id;
    private String name;
    private Boolean androidActive;
    private Boolean iosActive;
    private List<SABChildElementDto> children;
  }
}
