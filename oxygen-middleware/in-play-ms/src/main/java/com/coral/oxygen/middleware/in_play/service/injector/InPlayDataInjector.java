package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import java.util.function.Supplier;

public interface InPlayDataInjector<T> {

  default void injectData(InPlayData inPlayData) {
    throw new UnsupportedOperationException("Not implemented");
  }

  default void injectData(InPlayData inPlayData, Supplier<T> injectorData) {
    injectData(inPlayData);
  }
}
