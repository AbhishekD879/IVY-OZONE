package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.EqualsAndHashCode;
import lombok.Setter;
import lombok.ToString;

@Setter
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class PopularAccaModule extends AbstractFeaturedModule<PopularAccaModuleData> {

  private String cardCta;
  private String cardCtaAfterAdd;

  @ChangeDetect
  public String getCardCta() {
    return cardCta;
  }

  @ChangeDetect
  public String getCardCtaAfterAdd() {
    return cardCtaAfterAdd;
  }

  public PopularAccaModule() {
    this.showExpanded = true;
  }

  @JsonIgnore
  @Override
  public ModuleType getModuleType() {
    return ModuleType.POPULAR_ACCA;
  }
}
