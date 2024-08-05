package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.service.SignPostingService;
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

@RunWith(Parameterized.class)
public class SignPostingAfterSaveListenerTest extends AbstractAfterSaveListenerTest<SignPosting> {

  @Mock private SignPostingService service;

  @Getter @InjectMocks private SignPostingAfterSaveListener listener;

  @Getter @Spy private SignPosting entity = new SignPosting();

  @Getter private final List<SignPosting> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "signposting"}});
  }

  @Before
  public void init() {
    given(service.findAllByBrand(anyString())).willReturn(Arrays.asList(entity));
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/bma", filename, Arrays.asList(entity));
  }
}
