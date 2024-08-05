package com.egalacoral.spark.timeform.controller.debug;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {DebugControllersConfiguration.class}, //
    properties = {"spring.profiles.active=some_not_exists"})
@Configuration
@Import(value = {HorseRaceController.class, QAController.class, TimeformController.class})
@TestPropertySource(locations = "classpath:empty.properties")
public class RestDebugIsMissingControllersTest {

  @Autowired(required = false)
  HorseRaceController horseRaceController;

  @Autowired(required = false)
  QAController qaController;

  @Autowired(required = false)
  TimeformController timeformController;

  @Test
  public void test() {
    Assert.assertNull(horseRaceController);
    Assert.assertNull(qaController);
    Assert.assertNull(timeformController);
  }
}
