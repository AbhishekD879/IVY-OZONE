package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.ModuleDataSelection;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import org.apache.commons.lang3.StringUtils;

@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class SurfaceBetModule extends EventsModule {

  public SurfaceBetModule() {
    this.setType("SurfaceBetModule");
    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);
    setDataSelection(dataSelection);
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.SURFACE_BET;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor, String segment) {
    visitor.visit(this, segment);
  }
}
