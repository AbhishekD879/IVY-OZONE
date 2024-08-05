package com.egalacoral.spark.timeform.timer;

import etm.core.aggregation.ExecutionAggregate;
import etm.core.configuration.BasicEtmConfigurator;
import etm.core.configuration.EtmManager;
import etm.core.monitor.EtmMonitor;
import etm.core.monitor.EtmPoint;
import etm.core.renderer.MeasurementRenderer;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.metrics.GaugeService;
import org.springframework.stereotype.Service;

@Service
public class TimerService implements MeasurementRenderer, Runnable {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimerService.class);

  EtmMonitor monitor;

  @Autowired private GaugeService gaugeService;

  private List<TimerRenderer> timerRenderers = new ArrayList<>();

  private Executor executor = Executors.newCachedThreadPool();

  public TimerService() {
    super();
    BasicEtmConfigurator.configure();
    monitor = EtmManager.getEtmMonitor();
    monitor.start();
  }

  public EtmPoint createPoint(String simpleName) {
    return monitor.createPoint(simpleName);
  }

  public EtmPoint submit(EtmPoint point) {
    point.collect();
    executor.execute(this);
    return point;
  }

  @Override
  public void render(Map points) {
    Set<Object> set = points.keySet();
    for (Object object : set) {
      ExecutionAggregate aggregate = (ExecutionAggregate) points.get(object);
      String key = object + ".timer.ms";
      int value = (int) aggregate.getAverage();
      gaugeService.submit(key, value);
      processTimerRenderers(key, aggregate);
    }
  }

  private void processTimerRenderers(String key, ExecutionAggregate aggregate) {
    for (TimerRenderer timerRenderer : timerRenderers) {
      timerRenderer.timerRender(key, aggregate);
    }
    LOGGER.debug("{}={}", key, aggregate.getAverage());
  }

  public boolean addTimerRenderer(TimerRenderer e) {
    return timerRenderers.add(e);
  }

  @Override
  public void run() {
    monitor.render(this);
  }

  public EtmPoint createPoint(Object object, String string) {
    String name = MessageFormat.format("{0}.{1}", object.getClass().getName(), string);
    return createPoint(name);
  }
}
