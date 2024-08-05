package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.ModuleDataSelection;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
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
    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);
    this.setType("PopularBetModule");
    setDataSelection(dataSelection);
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.POPULAR_BETS;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
