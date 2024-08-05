package com.egalacoral.spark.timeform.model;

import etm.core.aggregation.ExecutionAggregate;
import java.io.Serializable;

public class TimerExecution implements Serializable {

  private static final long serialVersionUID = 1L;
  private String name;
  private long measurements = 0;

  private double min = 0.0;
  private double max = 0.0;
  private double total = 0.0;

  public TimerExecution(String name) {
    super();
    this.name = name;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public long getMeasurements() {
    return measurements;
  }

  public void setMeasurements(long measurements) {
    this.measurements = measurements;
  }

  public double getMin() {
    return min;
  }

  public void setMin(double min) {
    this.min = min;
  }

  public double getMax() {
    return max;
  }

  public void setMax(double max) {
    this.max = max;
  }

  public double getTotal() {
    return total;
  }

  public void setTotal(double total) {
    this.total = total;
  }

  public double getAverage() {
    if (measurements != 0) {
      return total / (double) measurements;
    }
    return 0d;
  }

  public void update(ExecutionAggregate aggregate) {
    setTotal(aggregate.getTotal());
    setMeasurements(aggregate.getMeasurements());
    setMax(aggregate.getMax());
    setMin(aggregate.getMin());
  }
}
