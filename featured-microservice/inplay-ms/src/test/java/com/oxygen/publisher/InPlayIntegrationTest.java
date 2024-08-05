package com.oxygen.publisher;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * A primitive integration test (as there is no other), checking if at least the app context is
 * successfully initialized, allowing to detect the problems such as context start-up failure after
 * updating dependencies/properties.
 *
 * <p>It can be also a starting point for the next IT tests.
 */
@RunWith(SpringRunner.class)
@SpringBootTest
@EmbeddedKafka(partitions = 1, bootstrapServersProperty = "spring.kafka.bootstrap-servers")
public class InPlayIntegrationTest {

  @Autowired private ApplicationContext applicationContext;

  @Test
  public void shouldApplicationContextBeInitialized() {
    assertThat(applicationContext).isNotNull();
  }
}
