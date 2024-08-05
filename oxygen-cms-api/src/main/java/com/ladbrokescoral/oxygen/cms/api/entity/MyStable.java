package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Auditable;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "my-stable")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
@JsonIgnoreProperties(ignoreUnknown = true)
@SuppressWarnings("java:S1820")
public class MyStable extends SortableEntity implements HasBrand, Auditable<MyStable> {
  @NotBlank
  @Indexed(unique = true)
  private String brand;

  private String entryPointIcon;

  @Size(max = 15, message = "message should be max of 15 chars")
  private String entryPointLabel;

  @Size(max = 25, message = "message should be max of 25 chars")
  private String editLabel;

  @Size(max = 25, message = "message should be max of 25 chars")
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
  private String createdByUserName;
  private String updatedByUserName;
  private String editNoteIcon;
  private String inProgressIcon;
  private boolean antePost;
  private String todayRunningHorsesText;
  private String todayRunningHorsesSvg;
  private String horseCountExceededMsg;
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

  @Override
  public MyStable content() {
    return this;
  }
}
