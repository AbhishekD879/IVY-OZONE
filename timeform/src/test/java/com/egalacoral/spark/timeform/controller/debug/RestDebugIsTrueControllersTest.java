package com.egalacoral.spark.timeform.controller.debug;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {DebugControllersConfiguration.class}, //
    properties = { //
      "rest.debug=true" //
    })
@TestPropertySource(locations = "classpath:empty.properties")
public class RestDebugIsTrueControllersTest {

  @Autowired(required = false)
  HorseRaceController horseRaceController;

  @Autowired(required = false)
  QAController qaController;

  @Autowired(required = false)
  TimeformController timeformController;

  @Test
  public void test() {
    Assert.assertNotNull(horseRaceController);
    Assert.assertNotNull(qaController);
    Assert.assertNotNull(timeformController);
  }
}
