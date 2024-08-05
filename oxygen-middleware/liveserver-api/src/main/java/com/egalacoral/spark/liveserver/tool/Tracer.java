package com.egalacoral.spark.liveserver.tool;

import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.egalacoral.spark.liveserver.Call;
import com.egalacoral.spark.liveserver.LiveServerClient;
import com.egalacoral.spark.liveserver.LiveServerListener;
import com.egalacoral.spark.liveserver.Message;
import com.egalacoral.spark.liveserver.configuration.LiveServerConfiguration;
import com.egalacoral.spark.liveserver.meta.EventMetaCachedRepoImpl;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import javax.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.context.annotation.Bean;

/**
 * This application traces all interaction with Live server to console. </br> Steps to trace simple
 * event : </br> 1. Go to https://invictus.coral.co.uk/#/?tab=InPlay </br> 2. Find {event id} </br>
 * 3. Run this application with parameter --event.ids={event id}</br> 4. Change event
 * https://ss-tst2.coral.co.uk/ti/hierarchy/event/{eventId}</br>
 *
 * @author Vitalij Havryk
 */
// @SpringBootApplication
@Slf4j
public class Tracer implements CommandLineRunner, LiveServerListener {

  private static final Long HOURS_5 = 5 * 60 * 60L;
  private static final int CONNECTION_TIMEOUT = 100;
  private static final int READ_TIMEOUT = 30;

  @Value("#{'${event.ids:}'.split(',')}")
  private List<String> eventIds;

  @Value("#{'${clock.ids:}'.split(',')}")
  private List<String> clockIds;

  @Value("#{'${score.ids:}'.split(',')}")
  private List<String> scoreIds;

  @Value("#{'${selection.ids:}'.split(',')}")
  private List<String> selectionIds;

  @Value("#{'${market.ids:}'.split(',')}")
  private List<String> marketIds;

  @Value("${http.proxyHost}")
  private String proxyHost;

  @Value("${http.proxyPort}")
  private String proxyPort;

  private Call call;

  @Bean
  public OkHttpClientCreator okHttpClientCreator() {
    return new OkHttpClientCreator();
  }

  @PostConstruct
  public void init() {
    LiveServerConfiguration conf = new LiveServerConfiguration();
    try {
      call =
          conf.callExecutor(
              conf.liveServeOkHttpClient(
                  CONNECTION_TIMEOUT,
                  READ_TIMEOUT,
                  "BODY",
                  okHttpClientCreator(),
                  proxyHost,
                  proxyPort));
    } catch (KeyManagementException | NoSuchAlgorithmException e) {
      log.error("Error occurred during initialization", e);
    }
  }

  public static void main(String[] args) {
    SpringApplication.run(Tracer.class, args);
  }

  @Override
  public void run(String... args) throws Exception {
    eventIds.add("8808157");
    log.info("Event ids : {}", eventIds);
    log.info("Score ids : {}", scoreIds);
    log.info("Clock ids : {}", clockIds);
    log.info("Selection ids : {}", selectionIds);
    log.info("Market ids : {}", marketIds);
    LiveServerClient client =
        new LiveServerClient(
            "https://push-tst2.coral.co.uk/push",
            call,
            HOURS_5,
            this,
            new EventMetaCachedRepoImpl(Caffeine.newBuilder().build()),
            "123");
    subscrube(client);
    client.connect();
    Thread.currentThread().join();
  }

  /**
   * @param client
   */
  private void subscrube(LiveServerClient client) {
    for (String id : eventIds) {
      if (!id.isEmpty()) {
        client.subscribeOnEvent(id);
      }
    }
    for (String id : scoreIds) {
      if (!id.isEmpty()) {
        client.subscribeOnScore(id);
      }
    }
    for (String id : clockIds) {
      if (!id.isEmpty()) {
        client.subscribeOnClock(id);
      }
    }
    for (String id : selectionIds) {
      if (!id.isEmpty()) {
        client.subscribeOnSelection(id);
      }
    }
    for (String id : marketIds) {
      if (!id.isEmpty()) {
        client.subscribeOnMarket(id);
      }
    }
  }

  @Override
  public void onMessage(Message message) {
    log.info("Got {}", message);
  }

  @Override
  public void onError(Throwable e) {
    // nothing
  }
}
