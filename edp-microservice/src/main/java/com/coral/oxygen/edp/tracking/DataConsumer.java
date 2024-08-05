package com.coral.oxygen.edp.tracking;

import java.util.Set;

/** Created by azayats on 19.12.17. */
public interface DataConsumer<T, D> {

  void consume(Set<T> consumingTask);

  void setListener(ConsumingListener<T, D> listener);
}
