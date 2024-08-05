package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.commons.lang.StringUtils;

@Data
@EqualsAndHashCode(callSuper = true)
public class PopularBetModule extends EventsModule {

  private boolean disabled;

  private String displayName;

  private String redirectionUrl;

  private String mostBackedIn;

  private String eventStartsIn;

  private String priceRange;

  private String backedInTimes;

  private boolean enableBackedInTimes;

  private String lastMsgUpdatedAt;

  private String updatedAt;

  public PopularBetModule() {
    this.showExpanded = true;
    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);

    setDataSelection(dataSelection);
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.POPULAR_BETS;
  }

  @ChangeDetect
  public boolean isDisabled() {
    return disabled;
  }

  @ChangeDetect(minor = true)
  public String getDisplayName() {
    return displayName;
  }

  @ChangeDetect(minor = true)
  public String getRedirectionUrl() {
    return redirectionUrl;
  }

  @ChangeDetect(minor = true)
  public String getMostBackedIn() {
    return mostBackedIn;
  }

  @ChangeDetect(minor = true)
  public String getEventStartsIn() {
    return eventStartsIn;
  }

  @ChangeDetect(minor = true)
  public String getPriceRange() {
    return priceRange;
  }

  @ChangeDetect
  public String getBackedInTimes() {
    return backedInTimes;
  }

  @ChangeDetect(minor = true)
  public boolean isEnableBackedInTimes() {
    return enableBackedInTimes;
  }

  @ChangeDetect(minor = true)
  public String getLastMsgUpdatedAt() {
    return lastMsgUpdatedAt;
  }

  @ChangeDetect(minor = true)
  public String getUpdatedAt() {
    return updatedAt;
  }
}
