package com.ladbrokescoral.cashout;

import io.netty.channel.epoll.Epoll;
import java.util.Collections;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.env.EnvironmentPostProcessor;
import org.springframework.boot.logging.DeferredLog;
import org.springframework.context.ApplicationEvent;
import org.springframework.context.ApplicationListener;
import org.springframework.core.env.ConfigurableEnvironment;
import org.springframework.core.env.MapPropertySource;
import org.springframework.stereotype.Component;

/**
 * Allows to run the app with turned on socket.io native epoll on non-linux environemnts It checks
 * if epoll library is available and if not - disables socket.io native epoll to continue without
 * it.
 *
 * <p>This post-processor can be removed in case
 * https://github.com/hiwepy/socketio-spring-boot-starter/pull/2 is merged
 */
@Component
public class NativeEpollEnvPreProcessor
    implements EnvironmentPostProcessor, ApplicationListener<ApplicationEvent> {

  private static final String SPRING_SOCKETIO_SERVER_USE_LINUX_NATIVE_EPOLL =
      "spring.socketio.server.use-linux-native-epoll";
  private static final DeferredLog log = new DeferredLog();

  @Override
  public void postProcessEnvironment(
      ConfigurableEnvironment environment, SpringApplication application) {
    String nativeEpollProperty =
        environment.getProperty(SPRING_SOCKETIO_SERVER_USE_LINUX_NATIVE_EPOLL);
    boolean isSocketIoNativeEpollEnabled = Boolean.parseBoolean(nativeEpollProperty);
    if (isSocketIoNativeEpollEnabled && !Epoll.isAvailable()) {
      MapPropertySource mapPropertySource =
          new MapPropertySource(
              "disableNativeEpollPropSource",
              Collections.singletonMap(SPRING_SOCKETIO_SERVER_USE_LINUX_NATIVE_EPOLL, "false"));
      environment.getPropertySources().addFirst(mapPropertySource);
      log.warn("EPOLL library is not available, disabling native epoll for socket.io");
    }
  }

  /**
   * Because logging system is not initialized at env post-processor phase, we need to use deffered
   * logging once application is started
   *
   * @param event
   */
  @Override
  public void onApplicationEvent(ApplicationEvent event) {
    log.replayTo(NativeEpollEnvPreProcessor.class);
  }
}
