package com.ladbrokescoral.oxygen;

import com.ladbrokescoral.oxygen.service.Listener;
import com.ladbrokescoral.oxygen.service.SocketIOListener;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableEurekaClient
@EnableScheduling
@SpringBootApplication
public class Application {

  public static void main(String[] args) {
    ConfigurableApplicationContext context = SpringApplication.run(Application.class, args);
    Listener listener = context.getBean(SocketIOListener.class);

    try {
      listener.start();
    } catch (Exception e) {
      listener.stop();
      context.close();
      throw e;
    }
  }
}
