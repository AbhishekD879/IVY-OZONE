package com.ladbrokescoral.oxygen.timeline.api;

import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationListener;
import org.springframework.context.annotation.Profile;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
@Profile("!test")
public class InitListener implements ApplicationListener<ContextRefreshedEvent> {

  private final PostRepository postRepository;

  private final CampaignRepository campaignRepository;

  @Override
  public void onApplicationEvent(ContextRefreshedEvent event) {
    postRepository.deleteAll();
    campaignRepository.deleteAll();
  }
}
