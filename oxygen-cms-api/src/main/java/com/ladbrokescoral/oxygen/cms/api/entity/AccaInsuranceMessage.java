package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "accaInsuranceMessages")
public class AccaInsuranceMessage extends AbstractEntity implements HasBrand {
  @NotNull private String brand;
  private Boolean accInsMsgEnabled;
  private Boolean enabled;
  private String svgId;
  private String bsAddToQualifyMsg;
  private String bsQualifiedMsg;
  private Boolean bsqInfoIcon;
  private String avlblInscCountIndi;
  private Integer obAccaCount;
  private BetslipSp betslipSp;
  private AccabarSp accabarSp;
  private BetreceiptSp betreceiptSp;
  private MybetsSp mybetsSp;
  private String profitIndi;
  private String profitIndiUrl;
  private PopUpDetails popUpDetails;
}
