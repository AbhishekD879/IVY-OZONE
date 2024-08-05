package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgMigration;
import com.ladbrokescoral.oxygen.cms.api.service.SvgMigrationService;
import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class SvgMigrateTest {

  @Mock private SvgMigrationService svgMigrationService;

  private SvgMigrate svgMigrate;

  @Before
  public void setUp() throws Exception {
    svgMigrate = new SvgMigrate(svgMigrationService);
  }

  @Test
  public void testshowAllSvgMigrates() {
    List<SvgMigration> resultList = prepareSvgMigration();
    when(svgMigrationService.findAllByBrand("bma")).thenReturn(resultList);
    ResponseEntity<List<SvgMigrationStatusMin>> list = svgMigrate.showAll("bma");
    Assert.assertEquals(1, list.getBody().size());
  }

  private List<SvgMigration> prepareSvgMigration() {
    SvgMigration migrate = new SvgMigration();
    migrate.setStatus("test status");
    migrate.setMessages("test message");
    migrate.setBrand("bma");
    List<SvgMigration> svgMigrates = new ArrayList<>();
    svgMigrates.add(migrate);
    return svgMigrates;
  }
}
