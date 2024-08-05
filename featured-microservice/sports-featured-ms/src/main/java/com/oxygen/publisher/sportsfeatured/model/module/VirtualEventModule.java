package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.ModuleDataSelection;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
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
  private Boolean inPlay = false;
  private Integer typeId;

  private String typeIds;
  private List<String> marketIds = new ArrayList<>();
  private List<Long> eventIds = new ArrayList<>();
  private String displayMarketType;
  private Boolean displayOnDesktop;
  private String mobileImageId;
  private String desktopImageId;
  private boolean disabled;
  private String buttonText;
  private String redirectionUrl;

  public VirtualEventModule() {

    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);
    this.setType("VirtualEventModule");
    setDataSelection(dataSelection);
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.VIRTUAL_NEXT_EVENTS;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
