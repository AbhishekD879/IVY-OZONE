package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;

@Data
public class BetSharingDto {
  private String id;
  @NotNull private String brand;

  private String horseRacingUrl;
  private String footBallUrl;
  private String url5ASide;
  @NotNull private String brandLogoUrl;
  @NotNull private String settledBetsGenericUrl;
  @NotNull private String openBetsGenericUrl;
  @NotNull private String extensionUrl;
  @NotNull private String beGambleAwareLogoUrl;
  @NotNull private String popUpDesc;

  @NotNull private String genericSharingLink;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String lostBetsShareCardMessage;

  @NotNull private List<ShareCardDetailsDto> lostBetControl;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String openBetShareCardMessage;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String openBetShareCardSecondMessage;

  private Boolean openBetShareCardStatus;
  @NotNull private List<ShareCardDetailsDto> openBetControl;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String wonBetShareCardMessage;

  private Boolean wonBetShareCardStatus;
  @NotNull private List<ShareCardDetailsDto> wonBetControl;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String cashedOutBetsShareCardMessage;

  @NotNull private List<ShareCardDetailsDto> cashedOutBetControl;

  private FTPBetSharingDto ftpBetSharingConfigs;

  private LuckyDipBetSharingDto luckyDipBetSharingConfigs;

  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;
  private Instant createdAt;
  private Instant updatedAt;
}
