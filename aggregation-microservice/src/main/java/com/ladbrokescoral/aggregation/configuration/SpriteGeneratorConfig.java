package com.ladbrokescoral.aggregation.configuration;

import com.ladbrokescoral.aggregation.utils.SpriteGenerator;
import com.ladbrokescoral.aggregation.utils.VerticalSpriteGenerator;
import java.awt.image.BufferedImage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class SpriteGeneratorConfig {

  @Bean
  public SpriteGenerator<BufferedImage> spriteGenerator(
      @Value("${silks.expected-width}") int expectedWidth,
      @Value("${silks.expected-height}") int expectedHeight) {
    log.info("{}x{}", expectedWidth, expectedHeight);
    return new VerticalSpriteGenerator(expectedWidth, expectedHeight);
  }

  @Bean
  BufferedImage defaultSilkImage() {
    return new BufferedImage(10, 10, 1);
  }
}
