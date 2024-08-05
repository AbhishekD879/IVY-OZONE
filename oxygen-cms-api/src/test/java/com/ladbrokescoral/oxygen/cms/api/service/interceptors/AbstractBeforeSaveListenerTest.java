package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import org.junit.After;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runners.Parameterized.Parameter;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;
import org.springframework.data.mongodb.core.mapping.event.BeforeSaveEvent;

public abstract class AbstractBeforeSaveListenerTest<E extends HasBrand> extends BDDMockito {

  @Rule public MockitoRule rule = MockitoJUnit.rule();

  @Mock protected DeliveryNetworkService context;

  @Parameter(0)
  public String brand;

  @Parameter(1)
  public String path;

  @Parameter(2)
  public String filename;

  protected abstract BasicMongoEventListener<E> getListener();

  protected abstract E getEntity();

  protected abstract List<?> getCollection();

  @Test
  public void shouldBeforeSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener().onBeforeSave(new BeforeSaveEvent<>(getEntity(), null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }
}
