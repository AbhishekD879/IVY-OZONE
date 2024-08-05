package com.egalacoral.spark.siteserver.api;

import static org.mockserver.integration.ClientAndServer.startClientAndServer;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.stream.Collectors;
import org.junit.After;
import org.junit.Before;
import org.mockserver.client.MockServerClient;
import org.mockserver.integration.ClientAndServer;

public abstract class BasicIntegrationMock {
  protected ClientAndServer server;
  protected MockServerClient mock;
  public static Integer MOCK_SERVER_PORT = 8443;
  public static String MOCK_SERVER_HOST = "127.0.0.1";

  @Before
  public void before() {
    server = startClientAndServer(BasicIntegrationMock.MOCK_SERVER_PORT);
    mock =
        new MockServerClient(
            BasicIntegrationMock.MOCK_SERVER_HOST, BasicIntegrationMock.MOCK_SERVER_PORT);
  }

  @After
  public void after() {
    server.stop();
  }

  protected String getResourceFileAsString(String resourceFileName) {
    InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
    return reader.lines().collect(Collectors.joining("\n"));
  }
}
