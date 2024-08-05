package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "oddsBoostMessages")
public class OddsBoostMessage extends AbstractEntity implements HasBrand {
  @NotNull private String brand;
  private Boolean oddsBoostMsgEnabled;
  private String svgId;
  private String bsHeader;
  private String bsDesc;
  private Boolean infoIcon;
  private String brsp;
  private Boolean brspEnabled;
  private Boolean brDispBoostedPrice;
  private String mbsp;
  private Boolean mbspEnabled;
  private Boolean mbDispBoostedPrice;
  private String profitIndicator;
  private PopUpDetails popUpDetails;
}
