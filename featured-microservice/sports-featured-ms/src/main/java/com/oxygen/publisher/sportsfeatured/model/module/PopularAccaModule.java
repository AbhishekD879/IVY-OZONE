package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.PopularAccaModuleData;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class PopularAccaModule extends AbstractFeaturedModule<PopularAccaModuleData> {

  private String type = "PopularAccaModule";
  private String cardCta;
  private String cardCtaAfterAdd;

  @JsonIgnore
  @Override
  public ModuleType getModuleType() {
    return ModuleType.POPULAR_ACCA;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
  }
}
