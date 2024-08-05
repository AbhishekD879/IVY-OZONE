package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.connector.SocketIOConnector;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.test.context.TestContext;
import org.springframework.test.context.TestExecutionListener;

public class WebSocketCleanUpListener implements TestExecutionListener {

  @Autowired protected SocketIOConnector socketIOConnector;

  @Autowired protected WebSocketTestClient webSocketTestClient;

  @Value("${remote-betslip.websocket.port}")
  int websocketPort;

  @Override
  public void afterTestExecution(TestContext testContext) {
    webSocketTestClient.clearReceivedData();
  }

  @Override
  public void beforeTestClass(TestContext testContext) {
    testContext.getApplicationContext().getAutowireCapableBeanFactory().autowireBean(this);
    socketIOConnector.start();
    webSocketTestClient.start(websocketPort);
  }

  @Override
  public void afterTestClass(TestContext testContext) {
    webSocketTestClient.stop();
    socketIOConnector.stop();
  }
}
