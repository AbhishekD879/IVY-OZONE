package com.coral.oxygen.edp.tracking.firstmarkets;

import com.coral.oxygen.edp.tracking.AbstractChangeDetector;
import com.coral.oxygen.edp.tracking.ChangeDetector;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;

/** Created by azayats on 28.12.17. */
public class FirstMarketsChangeDetector extends AbstractChangeDetector
    implements ChangeDetector<FirstMarketsData> {

  @Override
  public boolean dataIsChanged(FirstMarketsData newData, FirstMarketsData oldData) {
    return isChanged(newData, oldData);
  }
}
