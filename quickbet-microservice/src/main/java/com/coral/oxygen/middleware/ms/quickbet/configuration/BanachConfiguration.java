package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.ladbrokescoral.oxygen.byb.banach.client.BanachClients;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachOptions;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PriceResponse;
import java.time.Duration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BanachConfiguration {

  @Bean
  public BanachClients banachClients(@Value("${banach.url}") String banachUrl) {
    return BanachClients.builder().baseUrl(banachUrl).build();
  }

  @Bean
  public BanachClients.BanachClientsBuilder banachClientBuilder(
      @Value("${banach.url}") String banachUrl) {
    return BanachClients.builder().baseUrl(banachUrl);
  }

  @Bean
  public BlockingBanachClient<GetPriceRequestDto, PriceResponse> priceClient(
      BanachClients.BanachClientsBuilder banachBuilder,
      @Value("${banach.price.timeout}") long priceTimeoutMillis) {

    return banachBuilder
        .defaultOptions(
            BanachOptions.builder().timeoutDuration(Duration.ofMillis(priceTimeoutMillis)).build())
        .build()
        .blockingPrice();
  }

  @Bean
  public BlockingBanachClient<PlaceBetRequestDto, PlaceBetResponse> placeBetClient(
      BanachClients.BanachClientsBuilder banachBuilder,
      @Value("${banach.place-bet.timeout}") long placeBetTimeoutMillis) {
    return banachBuilder
        .defaultOptions(
            BanachOptions.builder()
                .timeoutDuration(Duration.ofMillis(placeBetTimeoutMillis))
                .build())
        .build()
        .blockingPlaceBet();
  }
}
