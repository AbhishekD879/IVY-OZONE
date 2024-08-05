package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestPrizeRepository;
import com.ladbrokescoral.oxygen.cms.kafka.ContestPublisher;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.bson.Document;
import org.junit.After;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class ContestAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Contest> {

  @Getter @Mock private ContestPublisher contestPublisher;

  @Getter @InjectMocks private ContestAfterSaveListener listener;

  @Getter @Mock private ContestPrizeRepository contestPrizeRepository;

  @Getter @Mock private Contest entity;

  @Getter @Mock private final List<Contest> collection = Arrays.asList(new Contest());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "contests"}});
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {
    Contest contest = new Contest();
    contest.setBrand("bma");
    this.getListener().onAfterSave(new AfterSaveEvent<Contest>(contest, null, "11"));
    verify(contestPublisher, times(1)).publish(any(), any(), any());
  }

  @Test
  public void shouldAfterDeleteEvent() throws Exception {
    Contest contest = new Contest();
    contest.setBrand("bma");
    contest.setId("VmM2b0k1R3NUS0lmemNOSHNvdUphQT09");
    Document document = new Document();
    document.put("_id", contest.getId());
    this.getListener()
        .onAfterDelete(new AfterDeleteEvent<Contest>(document, Contest.class, contest.getId()));
    verify(contestPublisher, times(1)).publish(any(), any(), any());
  }

  @After
  public void should() throws Exception {
    verify(contestPublisher, times(1)).publish(any(), any(), any());
  }
}
