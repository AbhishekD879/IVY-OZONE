package com.egalacoral.spark.timeform.configuration;

import com.egalacoral.spark.timeform.api.TimeFormAPI;
import com.egalacoral.spark.timeform.api.TimeFormAPIBuilder;
import com.egalacoral.spark.timeform.api.connectivity.RetryReloginFailOverStrategy;
import com.egalacoral.spark.timeform.api.connectivity.SystemTimeProvider;
import com.egalacoral.spark.timeform.api.multiplexer.TimeFormAPIMultiplexer;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Conditional;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TimeformApiConfiguration {

  @Value("${timeform.api.tokens.url}")
  private String tokenUrl;

  @Value("${timeform.api.data.url}")
  private String dataUrl;

  @Value("${timeform.api.image.url}")
  private String imageUrl;

  @Value("${timeform.api.url.greyhound}")
  private String grUrlSuffix;

  @Value("${timeform.api.url.horse}")
  private String hrUrlSuffix;

  @Value("${emulator.timeform.api.data.url:}")
  private Optional<String> dataUrlEmulator;

  @Conditional(TimeformRealCondition.class)
  @Bean
  public TimeFormAPI getTimeFormAPI() {
    return new TimeFormAPIBuilder(tokenUrl, dataUrl, grUrlSuffix, hrUrlSuffix, imageUrl) //
        .setTimeProvider(new SystemTimeProvider())
        .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
        .build();
  }

  @Conditional(TimeformEmulatorCondition.class)
  @Bean
  public TimeFormAPI getTimeFormEmulatorAPI() {
    TimeFormAPI realApi =
        new TimeFormAPIBuilder(tokenUrl, dataUrl, grUrlSuffix, hrUrlSuffix, imageUrl) //
            .setTimeProvider(new SystemTimeProvider())
            .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
            .build();
    TimeFormAPI emulatorApi =
        new TimeFormAPIBuilder(
                dataUrlEmulator.get(),
                dataUrlEmulator.get(),
                grUrlSuffix,
                hrUrlSuffix,
                dataUrlEmulator.get()) //
            .setTimeProvider(new SystemTimeProvider())
            .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
            .build();
    return new TimeFormAPIMultiplexer(realApi, emulatorApi);
  }
}
