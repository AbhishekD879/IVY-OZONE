package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
@SuppressWarnings("java:S1820")
public class MyStableDto {

  private String id;
  private String brand;
  private String entryPointIcon;
  private String entryPointLabel;
  private String editLabel;
  private String saveLabel;
  private String editIcon;
  private String saveIcon;
  private String bookmarkIcon;
  private String unbookmarkIcon;
  private String noHorsesIcon;
  private String noHorsesCtaButton;
  private String signpostingIcon;
  private String emptyStableLabel1;
  private String emptyStableLabel2;
  private String notesSignPostingIcon;
  private boolean active;
  private boolean horsesRunningToday;
  private String todayRunningHorsesText;
  private String todayRunningHorsesSvg;
  private String createdByUserName;
  private String updatedByUserName;
  private String editNoteIcon;
  private String horseCountExceededMsg;
  private String inProgressIcon;
  private boolean antePost;
  private String createdBy;
  private String updatedBy;
  private Instant createdAt;
  private Instant updatedAt;
  private boolean isMybets;
  private String stableTooltipText;
  private boolean isSettledBets;
  private String crcLogo;
  private String crcLabel;
  private String crcSignPostingIcon;
  private Boolean crcActive;
  private String crcSaveAllText;
  private String crcWhiteBookmarkIcon;
  private String crcBlackBookmarkIcon;
  private String crcGotoRacingClubText;
  private String crcGotoRacingClubUrl;
}
