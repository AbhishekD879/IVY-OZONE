package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.AccaInsuranceMessage;
import com.ladbrokescoral.oxygen.cms.api.repository.AccaInsuranceMessageRepository;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class AccaInsuranceMessagesAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<AccaInsuranceMessage> {

  @Getter @InjectMocks private AccaInsuranceMessagesAfterSaveListener listener;

  @Getter @Mock private AccaInsuranceMessage entity;

  @Mock private AccaInsuranceMessageRepository accaInsuranceMessageRepository;

  @Getter @Mock
  private final List<AccaInsuranceMessage> collection = Arrays.asList(new AccaInsuranceMessage());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "acca-insurance"}});
  }

  @Before
  public void init() {
    given(accaInsuranceMessageRepository.findOneByBrand(Mockito.any()))
        .willReturn(Optional.of(new AccaInsuranceMessage()));
  }

  @Override
  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<AccaInsuranceMessage>(getEntity(), null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, new AccaInsuranceMessage());
    }
  }
}
