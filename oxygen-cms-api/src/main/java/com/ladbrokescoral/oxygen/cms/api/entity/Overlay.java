package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class Overlay extends SortableEntity implements HasBrand {

  private String brand;
  private String headerTitle;
  private String sectionTitle;
  private String previewTitle;
  private String videoURL;
  private String plWelcomeTitle;
  private String plWelcomeContent;
  private String plWelcomeFooter;
  private String plPrizePoolInfo;
  private String plRulesEntryInfo;
  private String plBuildTeamInfo;
  private String plBuildAnotherTeamInfo;
  private String plBuildAnotherTeamHeader;
  private String plBuildAnotherTeamContent;
  private String plBulesButtonInfo;
  private String lobbyWelcomeHeader;
  private String lobbyWelcome1;
  private String lobbyWelcome2;
  private String lobbyWelcome3;
  private String lobbySignPostingsInfo;
  private String lobbyEntryInfo;
  private String lobbyShowdownCardInfo;
  private String liveHeaderTitle;
  private String liveSectionTitle;
  private String liveFooterTitle;
  private String liveMainPageHeaderTitle;
  private String liveMainPageSectionTitle;
  private String liveEntryTitle;
  private String liveStatTitle;
  private String liveProgressHeaderTitle;
  private String liveProgressFooterTitle;
  private String liveLeaderBoardEntriesTitle;
  private boolean overlayEnabled = true;
}
