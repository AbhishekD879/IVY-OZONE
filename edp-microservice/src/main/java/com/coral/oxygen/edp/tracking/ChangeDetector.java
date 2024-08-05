package com.coral.oxygen.edp.tracking;

/** Created by azayats on 28.12.17. */
public interface ChangeDetector<D> {

  boolean dataIsChanged(D newData, D oldData);
}
