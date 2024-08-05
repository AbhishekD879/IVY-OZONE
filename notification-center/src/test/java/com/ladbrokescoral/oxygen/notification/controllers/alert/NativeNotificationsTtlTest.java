package com.ladbrokescoral.oxygen.notification.controllers.alert;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.notification.controllers.NativeNotifications;
import com.ladbrokescoral.oxygen.notification.services.NotificationSubscriptionService;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {NativeNotifications.class})
@AutoConfigureMockMvc(addFilters = false)
public class NativeNotificationsTtlTest {

  @MockBean private NotificationSubscriptionService service;

  @Qualifier("StringRedisTemplate")
  @MockBean
  private StringRedisTemplate redisTemplate;

  @Autowired protected MockMvc mockMvc;
  @MockBean Events events;
  @MockBean Subscriptions subscriptions;

  @Test
  public void getNonExpiredSubTest() throws Exception {
    mockMvc
        .perform(
            MockMvcRequestBuilders.get("/noExpirySubscriptions/0/10")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
