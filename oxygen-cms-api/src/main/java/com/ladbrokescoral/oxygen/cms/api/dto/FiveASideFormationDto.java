package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.BanachMarket;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class FiveASideFormationDto {
  @Id private String id;
  private String title;
  private String actualFormation;
  private String position1;
  private BanachMarket stat1;
  private String position2;
  private BanachMarket stat2;
  private String position3;
  private BanachMarket stat3;
  private String position4;
  private BanachMarket stat4;
  private String position5;
  private BanachMarket stat5;
}
