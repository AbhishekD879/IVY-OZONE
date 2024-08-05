package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.service.MyStableService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.springframework.context.annotation.Import;

@RunWith(Parameterized.class)
@Import(ModelMapperConfig.class)
public class MyStableAfterSaveListenerTest extends AbstractAfterSaveListenerTest<MyStable> {
  @Mock private MyStableService service;

  @Getter @InjectMocks private MyStableAfterSaveListener listener;

  @Getter @Spy private MyStable entity = new MyStable();

  @Getter private final List<MyStable> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/my-stable", "configuration"}});
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(Arrays.asList(entity));
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/bma/my-stable", filename, Arrays.asList(entity));
  }

  private static MyStable getMyStable() {
    MyStable myStable = new MyStable();
    myStable.setActive(true);
    myStable.setBrand("bma");
    myStable.setId("1");
    myStable.setEntryPointIcon("notes");
    myStable.setEntryPointIcon("EntryIcon");
    myStable.setSignpostingIcon("signposting");
    myStable.setEditLabel("title");

    return myStable;
  }
}
