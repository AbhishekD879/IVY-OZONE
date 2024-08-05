package com.coral.oxygen.middleware.pojos.model.output.inplay;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import java.util.List;

/** Created by azayats on 20.01.17. */
public class SportsRibbon {

  private List<SportsRibbonItem> items;

  @ChangeDetect(compareList = true)
  public List<SportsRibbonItem> getItems() {
    return items;
  }

  public void setItems(List<SportsRibbonItem> items) {
    this.items = items;
  }
}
