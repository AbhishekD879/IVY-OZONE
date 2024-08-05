package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.AssetManagementService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class AssetManagementAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<AssetManagement> {
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  @Mock private AssetManagementService service;
  @Getter @InjectMocks private AssetManagementAfterSaveListener listener;

  @Getter @Mock private AssetManagement entity;
  @Getter private List<AssetManagement> collection = Arrays.asList(entity);

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "asset-management"}});
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
    ReflectionTestUtils.setField(
        listener, "coralAssetmanagementTopic", "coral-cms-assetmanagement");
    ReflectionTestUtils.setField(listener, "ladsAssetmanagementTopic", "cms-assetmanagement");
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<AssetManagement>(getEntity(), null, "footermenus"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
      then(context).should().uploadCFContent(brand, "api/bma/cf", filename, collection);
      ReflectionTestUtils.setField(
          listener,
          brand.equalsIgnoreCase(Brand.BMA)
              ? "coralAssetmanagementTopic"
              : "ladsAssetmanagementTopic",
          brand.equalsIgnoreCase(Brand.BMA) ? "coral-cms-assetmanagement" : "cms-assetmanagement");
    }
  };;;;
}
