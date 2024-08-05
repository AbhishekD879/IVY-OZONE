package com.oxygen.publisher;

import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.handler.ClientHead;
import com.corundumstudio.socketio.protocol.Packet;
import com.corundumstudio.socketio.transport.NamespaceClient;
import com.newrelic.api.agent.NewRelic;
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.translator.DiagnosticService;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;

@EnableEurekaClient
@SpringBootApplication
@EnableScheduling
@ComponentScan(
    basePackages = {
      "com.oxygen.publisher.sportsfeatured.configuration",
      "com.oxygen.publisher.service",
      "com.oxygen.publisher.sportsfeatured.service",
      "com.oxygen.publisher.configuration",
      "com.oxygen.health.api"
    })
@Slf4j
public class SportsFeaturedApplication {

  public static void main(String[] args) {
    ConfigurableApplicationContext context =
        SpringApplication.run(SportsFeaturedApplication.class, args);
    startSportFeaturedApplication(context);
  }

  public static void startSportFeaturedApplication(ConfigurableApplicationContext context) {
    SportsServiceRegistry featuredServiceRegistry = context.getBean(SportsServiceRegistry.class);
    try {
      DiagnosticService diagnosticService = context.getBean(DiagnosticService.class);
      if (diagnosticService != null) {
        diagnosticService.start();
      }
      featuredServiceRegistry.load();
      featuredServiceRegistry.getSocketIOServer().start();
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("FeaturedApplication startup failed.", e);
      featuredServiceRegistry.stop();
      context.close();
      throw e;
    }
  }

  @Autowired SocketIOServer server;

  @Scheduled(fixedDelay = 10_000)
  public void trackPacketsQueues() {
    Map<String, Integer> clientsWithQueueSizes = new HashMap<>();
    server
        .getAllClients()
        .forEach(
            client -> {
              ClientHead baseClient = ((NamespaceClient) client).getBaseClient();
              Queue<Packet> packetsQueue = baseClient.getPacketsQueue(client.getTransport());

              int queueSize = packetsQueue.size();
              if (queueSize >= 10) {
                clientsWithQueueSizes.put(baseClient.getSessionId().toString(), queueSize);
              }
            });

    if (!clientsWithQueueSizes.isEmpty()) {
      log.warn("Packets queues (10+): {}", clientsWithQueueSizes);
    }
  }
}
