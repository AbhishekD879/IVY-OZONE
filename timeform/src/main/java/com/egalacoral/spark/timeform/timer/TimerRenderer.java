package com.egalacoral.spark.timeform.timer;

import etm.core.aggregation.ExecutionAggregate;

public interface TimerRenderer {

  void timerRender(String key, ExecutionAggregate aggregate);
}
