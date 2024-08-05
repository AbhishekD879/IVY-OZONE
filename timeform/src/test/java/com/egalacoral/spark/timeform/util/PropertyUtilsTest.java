package com.egalacoral.spark.timeform.util;

import com.egalacoral.spark.timeform.configuration.TimeformApiConfiguration;
import java.util.Properties;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.env.Environment;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {TimeformApiConfiguration.class},
    properties = { //
      "a=1", //
      "b=2"
    })
@TestPropertySource(locations = "classpath:PropertyUtilsTest.properties")
public class PropertyUtilsTest {

  @Autowired Environment environment;

  @Test
  public void test() {
    Properties properties = PropertyUtils.getProperties(environment);
    Assert.assertEquals("1", properties.getProperty("a"));
    Assert.assertEquals("2", properties.getProperty("b"));
    Assert.assertEquals("3", properties.getProperty("c"));
    Assert.assertEquals("4", properties.getProperty("d"));
  }
}
