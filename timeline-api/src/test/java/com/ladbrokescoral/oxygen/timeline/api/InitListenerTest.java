package com.ladbrokescoral.oxygen.timeline.api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.event.ContextRefreshedEvent;

@RunWith(MockitoJUnitRunner.class)
public class InitListenerTest {
  @InjectMocks private InitListener initListener;
  @Mock CampaignRepository campaignRepository;
  @Mock PostRepository postRepository;

  @Test
  public void applicationTest() {
    initListener.onApplicationEvent(mock(ContextRefreshedEvent.class));
    verify(campaignRepository, atLeastOnce()).deleteAll();
    assertEquals(0, campaignRepository.count());
    verify(postRepository, atLeastOnce()).deleteAll();
  }
}
