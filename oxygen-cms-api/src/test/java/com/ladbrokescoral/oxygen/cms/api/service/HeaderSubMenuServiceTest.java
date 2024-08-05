package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.repository.HeaderSubMenuRepository;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HeaderSubMenuServiceTest {

  @Mock private HeaderSubMenuRepository repository;

  private HeaderSubMenuService headerSubMenuService;

  @Before
  public void setUp() throws Exception {
    headerSubMenuService = new HeaderSubMenuService(repository);
  }

  @Test
  public void testFindAllByBrandAndDisabled() {
    headerSubMenuService.findAllByBrandAndDisabled("bma");
    verify(repository).findAllByBrandAndDisabledOrderBySortOrderAsc("bma", false);
  }
}
