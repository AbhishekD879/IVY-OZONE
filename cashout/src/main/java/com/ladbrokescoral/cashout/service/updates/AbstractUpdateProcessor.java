package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.safbaf.HasStatus;

public abstract class AbstractUpdateProcessor<T extends HasStatus> {

  protected final SelectionDataAwareUpdateProcessor<T> selectionDataAwareUpdateProcessor;

  public AbstractUpdateProcessor(
      SelectionDataAwareUpdateProcessor<T> selectionDataAwareUpdateProcessor) {
    this.selectionDataAwareUpdateProcessor = selectionDataAwareUpdateProcessor;
  }
}
