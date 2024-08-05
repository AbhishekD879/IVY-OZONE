package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.bson.Document;
import org.junit.After;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runners.Parameterized.Parameter;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;

public abstract class AbstractAfterDeleteListenerModelTest<E extends HasBrand> extends BDDMockito {

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

  protected abstract Document getModel();

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterDelete(new AfterDeleteEvent((Document) getModel(), null, "11"));

    // then
    if (null != getModel()) {
      then(context).should().delete(brand, path, filename);
    }
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context).shouldHaveNoMoreInteractions();
  }
}
