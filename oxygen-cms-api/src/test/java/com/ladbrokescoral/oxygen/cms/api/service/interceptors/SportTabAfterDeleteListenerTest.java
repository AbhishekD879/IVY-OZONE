package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.bson.Document;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class SportTabAfterDeleteListenerTest extends AbstractAfterDeleteListenerModelTest {
  @Getter @InjectMocks private SportTabAfterSaveListener listener;
  @Getter @Spy SportTab entity = new SportTab();
  @Getter private Document model = new Document();
  @Getter private List<?> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/sport-tabs", "12"}});
  }

  @Before
  public void init() {
    model.put("sportId", 12);
    model.put("checkEvents", true);
    model.put("brand", "bma");
    model.put("Name", "outrights");
    model.put("DisplayName", "Outrights");
    model.put("SortOrder", 4.0);
    model.put("Enabled", true);

    entity.setSportId(12);
    entity.setBrand("bma");
    entity.setEnabled(true);
    entity.setCheckEvents(true);
    entity.setName("outrights");
    entity.setDisplayName("Outrights");
    entity.setSortOrder(4.0);
  }

  @After
  public void shouldHaveNoMoreInteractions() {}
}
