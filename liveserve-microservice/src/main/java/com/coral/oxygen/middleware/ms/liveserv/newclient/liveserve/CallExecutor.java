package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.coral.siteserver.api.SiteServerException;
import com.google.common.util.concurrent.ThreadFactoryBuilder;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.io.IOException;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.extern.slf4j.Slf4j;
import okhttp3.Request;
import okhttp3.Response;

/**
 * This class executes calls to Live Server
 *
 * @author Vitalij Havryk
 */
@Slf4j
public class CallExecutor {

  private static final int TIME_SLEEP = 5000;
  private final String id;
  private final Call call;
  private String endPoint;
  private Payload payload;
  private LiveServerListener listener;
  private ExecutorService executorService;
  private AtomicBoolean working;

  public CallExecutor(
      String endPoint, Payload payload, LiveServerListener listeners, String id, Call call) {
    this.endPoint = endPoint;
    this.payload = payload;
    this.listener = listeners;
    this.id = id;
    this.call = call;
  }

  public void execute() {
    final ThreadFactory threadFactory =
        new ThreadFactoryBuilder()
            .setNameFormat("call-executor-%d-".concat(id))
            .setDaemon(true)
            .build();
    executorService = Executors.newSingleThreadExecutor(threadFactory);
    working = new AtomicBoolean(true);
    executorService.execute(this::infinityExecute);
  }

  private void infinityExecute() {
    do {
      try {
        doExecute();
      } catch (Exception e) {
        NewRelic.noticeError(e);
        log.error("Error while requesting {}", endPoint, e);
        listener.onError(e);
        sleep();
      }
    } while (working.get());
  }

  private void sleep() {
    try {
      log.debug("Sleeping {} milliseconds...", TIME_SLEEP);
      Thread.sleep(TIME_SLEEP);
    } catch (InterruptedException e) {
      NewRelic.noticeError(e);
      log.error("Error while sleeping", e);
      Thread.currentThread().interrupt();
    }
  }

  private void doExecute() throws IOException {
    if (payload.getPayloadItems().size() == 0) {
      log.info("There are no items to subscribe");
      sleep();
    } else {
      executeCall();
    }
  }

  private void executeCall() throws IOException {
    RequestBuilder builder = new RequestBuilder();
    Request request = builder.build(endPoint, payload);
    Response response = doExecute(request);
    ResponseConverter converter = new ResponseConverter();
    List<Message> messages = converter.convert(response.body().string());
    payload.update(messages);
    messages.stream().forEachOrdered(this::notify);
  }

  @Trace(metricName = "CallExecutor/Notify", dispatcher = true)
  private void notify(Message message) {
    try {
      listener.onMessage(Collections.singletonList(message));
    } catch (IllegalArgumentException | SiteServerException e) {
      log.error("Exception while message processing.", e);
      NewRelic.noticeError(e);
      listener.onError(e);
    }
  }

  @Trace(metricName = "CallExecutor/doExecute", dispatcher = true)
  private Response doExecute(Request request) throws IOException {
    return call.execute(request);
  }

  ExecutorService getExecutorService() {
    return executorService;
  }

  void setExecutorService(ExecutorService executorService) {
    this.executorService = executorService;
  }

  public void shutdown() {
    working.set(false);
    executorService.shutdownNow();
  }

  public String getEndPoint() {
    return endPoint;
  }

  public LiveServerListener getListener() {
    return listener;
  }
}
