package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzonesyc")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class FanzoneSyc extends FanzoneSycPage {
  private String sycTitle;
  private String sycPopUpTitle;
  private String sycDescription;
  private String sycPopUpDescription;
  private String sycImage;
  private String okCTA;
  private String remindLater;
  private String remindLaterHideDays;
  private String dontShowAgain;
  @NotNull private Instant seasonStartDate;
  @NotNull private Instant seasonEndDate;
  private String customTeamNameText;
  private String sycConfirmCTA;
  private String sycChangeCTA;
  private String sycExitCTA;
  private String thankYouMsg;
  private String changeTeamTimePeriodMsg;
  private Integer daysToChangeTeam;
  private String updatedByUserName;
  private String createdByUserName;
}
