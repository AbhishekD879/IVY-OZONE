package com.coral.oxygen.middleware.pojos.model.cms;

import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@Accessors(chain = true)
public class VirtualSportDto {
  private String id;
  private String title;
  private List<VirtualSportTrackDto> tracks;
  private String svgId;
  private String svg;
  private String ctaButtonUrl;
  private String ctaButtonText;
}
