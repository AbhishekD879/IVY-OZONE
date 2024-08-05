package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.commons.lang.StringUtils;

@Data
@EqualsAndHashCode(callSuper = true)
public class VirtualEventModule extends EventsModule {
  private String svgId;
  private Integer limit;
  private Integer typeId;

  private String mobileImageId;
  private String desktopImageId;
  private boolean disabled;

  private String typeIds;
  private List<String> marketIds = new ArrayList<>();
  private List<Long> eventIds = new ArrayList<>();
  private String displayMarketType;
  private Boolean displayOnDesktop;

  private String buttonText;
  private String redirectionUrl;

  public VirtualEventModule() {
    this.showExpanded = true;
    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);

    setDataSelection(dataSelection);
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  @ChangeDetect
  public Integer getLimit() {
    return limit;
  }

  @ChangeDetect
  public Integer getTypeId() {
    return typeId;
  }
  // This property used to get TypeIds.
  @ChangeDetect
  public String getTypeIds() {
    return typeIds;
  }

  @ChangeDetect
  public List<Long> getEventIds() {
    return eventIds;
  }

  public List<String> getMarketIds() {
    return marketIds;
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.VIRTUAL_NEXT_EVENTS;
  }

  @ChangeDetect
  public String getDisplayMarketType() {
    return displayMarketType;
  }

  @ChangeDetect
  public Boolean isDisplayOnDesktop() {
    return displayOnDesktop;
  }

  @ChangeDetect
  public String getButtonText() {
    return buttonText;
  }

  @ChangeDetect
  public String getRedirectionUrl() {
    return redirectionUrl;
  }
}
