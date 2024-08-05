package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzonesyc")
public class FanzoneSycPage extends AbstractTimelineEntity<FanzoneSycPage> implements HasBrand {
  @NotNull private String pageName;
  @NotNull private String brand;
  private String sycLoginCTA;
  private String sycConfirmTitle;
  private String sycThankYouTitle;
  private String sycPreLoginTeamSelectionMsg;
  private String sycPreLoginNoTeamSelectionMsg;
  private String sycConfirmMsgMobile;
  private String sycConfirmMsgDesktop;
  private String sycNoTeamSelectionTitle;
  private String relegatedSycTitle;
  private String relegatedSycDescription;
  private String customTeamNameDescription;
  private String sycCancelCTA;
}
