package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.dto.StatisticContentDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StatisticContentPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.bson.Document;
import org.bson.types.ObjectId;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class StatisticContentAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<StatisticContent> {

  @Mock StatisticContentPublicService service;

  @Getter @InjectMocks private StatisticContentAfterSaveListener listener;

  @Getter @Mock StatisticContent entity;

  @Getter List<StatisticContentDto> collection;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/statistic-content", "1122"}});
  }

  @Before
  public void init() {
    this.collection = Arrays.asList(new StatisticContentDto());
    given(getEntity().getEventId()).willReturn("1122");
    given(this.service.findAllByBrandAndEventId(anyString(), anyString()))
        .willReturn(this.getCollection());
  }

  @Test
  public void testShouldAfterDeleteEvent() {

    Document document = new Document().append("_id", new ObjectId("63fca96b6db928741f4432a9"));

    // given
    given(this.getEntity().getBrand()).willReturn(brand);
    given(this.getEntity().getId()).willReturn("63fca96b6db928741f4432a9");

    // when
    this.getListener()
        .onAfterDelete(
            new AfterDeleteEvent<>(document, StatisticContent.class, "12"),
            new AfterSaveEvent<>(getEntity(), null, "12"));

    // then
    if (null != this.getCollection()) {
      then(context).should().upload(brand, path, filename, this.getCollection());
    }
  }

  @Test
  public void testShouldAfterDeleteEventDoNothing() {
    Document document = new Document().append("_id", new ObjectId("63fca96b6db928741f4432a6"));

    // given
    given(this.getEntity().getBrand()).willReturn(brand);
    given(this.getEntity().getId()).willReturn("63fca96b6db928741f4432a9");

    // when
    this.getListener()
        .onAfterDelete(
            new AfterDeleteEvent<>(document, StatisticContent.class, "23"),
            new AfterSaveEvent<>(getEntity(), null, "23"));

    // then
    if (null != this.getCollection()) {
      then(context).shouldHaveNoInteractions();
    }
  }
}
