package com.coral.oxygen.edp.model.mapping.config;

import com.coral.oxygen.edp.exceptions.InitializationException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes = SportsConfigTest.class)
@TestPropertySource(
    properties = {
      "improper.sports.config.json=classpath:improperSportsConfig.txt",
      "sports.config.json=classpath:SportsConfig.json",
    })
public class SportsConfigTest {

  @Value("${improper.sports.config.json}")
  Resource improperSportsConfigJson;

  private ObjectMapper mapper = new ObjectMapper();

  @Test(expected = InitializationException.class)
  public void testIoException() {
    new SportsConfig(improperSportsConfigJson, mapper);
  }
}
