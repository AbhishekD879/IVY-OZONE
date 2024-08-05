package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class CompetitionModule extends AbstractEntity {

  @NotBlank private String name;
  private CompetitionModuleType type;
  private String path;
  @Valid private List<CompetitionMarket> markets = new ArrayList<>();
  private List<Integer> eventIds = new ArrayList<>();
  private int maxDisplay;
  private ViewType viewType = ViewType.CARD;
  private String promoTag;
  private boolean enabled;
  private Integer typeId;
  private String aemPageName;
  @Valid private CompetitionGroupModuleData groupModuleData;
  private CompetitionSpecialModuleData specialModuleData;
  private Integer resultModuleSeasonId;
  private List<String> surfaceBets = new ArrayList<>();
  private List<String> highlightCarousels = new ArrayList<>();

  @Valid
  private CompetitionKnockoutModuleData knockoutModuleData = new CompetitionKnockoutModuleData();

  public CompetitionModule setPathFromParentCompetitionTab(CompetitionTab parentCompetitionTab) {
    setPath(parentCompetitionTab.getPath() + "/" + this.getId());
    return this;
  }

  public CompetitionModule setPathFromParentCompetitionSubTab(
      CompetitionSubTab parentCompetitionSubTab) {
    setPath(parentCompetitionSubTab.getPath() + "/" + this.getId());
    return this;
  }
}
