package com.egalacoral.spark.timeform.configuration;

import com.egalacoral.spark.timeform.api.TimeFormAPI;
import com.egalacoral.spark.timeform.api.multiplexer.TimeFormAPIMultiplexer;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {TimeformApiConfiguration.class},
    properties = { //
      "timeform.api.tokens.url=https://sso.timeform.com", //
      "timeform.api.data.url=https://api.timeform.com", //
      "emulator.timeform.api.data.url=http://127.0.0.1", //
      "timeform.api.url.greyhound=GreyhoundRacingApi/odata", //
      "timeform.api.url.horse=HorseRacingApi/odata", //
      "spring.profiles.active=junit" //
    })
public class TimeformLoginConfigurationRealPlusEmulatorApiTest {

  @Autowired TimeFormAPI timeFormAPI;

  /** We have configured property 'emulator.timeform.api.data.url' */
  @Test
  public void test() {
    Assert.assertTrue(
        "TimeFormAPI implementation should be TimeFormAPIMultiplexer",
        timeFormAPI instanceof TimeFormAPIMultiplexer);
  }
}
