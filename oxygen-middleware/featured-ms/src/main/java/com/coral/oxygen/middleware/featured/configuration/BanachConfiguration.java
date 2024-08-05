package com.coral.oxygen.middleware.featured.configuration;

import com.ladbrokescoral.oxygen.byb.banach.client.BanachClients;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.LeaguesResponse;
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
  public BlockingBanachClient<GetLeaguesResponseDto, LeaguesResponse> getLeaguesClient(
      BanachClients banachClients) {
    return banachClients.blockingGetLeagues();
  }
}
