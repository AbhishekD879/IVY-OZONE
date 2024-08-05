package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.ModuleDataSelection;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.commons.lang3.StringUtils;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class HighlightCarouselModule extends EventsModule {
  private String svgId;
  private Integer limit;
  private Boolean inPlay;
  private Integer typeId;
  // BMA-62182: This property helps to holds the multiple TypeIds.
  private List<String> typeIds;
  private List<Long> eventIds;
  private Boolean displayOnDesktop;

  public HighlightCarouselModule() {
    ModuleDataSelection dataSelection = new ModuleDataSelection();
    dataSelection.setSelectionId(StringUtils.EMPTY);
    dataSelection.setSelectionType(StringUtils.EMPTY);
    this.setType("HighlightCarouselModule");

    setDataSelection(dataSelection);
  }

  @Override
  public ModuleType getModuleType() {
    return ModuleType.HIGHLIGHTS_CAROUSEL;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
