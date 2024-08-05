package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class FanzoneSycPageDto extends AbstractTimelineEntity<FanzoneSycPageDto>
    implements HasBrand {
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
  private String customTeamNameDescription;
  private String sycCancelCTA;
}
