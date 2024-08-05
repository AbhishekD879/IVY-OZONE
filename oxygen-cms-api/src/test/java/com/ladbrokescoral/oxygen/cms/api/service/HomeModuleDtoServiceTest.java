package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class HomeModuleDtoServiceTest {
  @Mock private HomeModuleRepository repository;
  @Mock private EventHubService hubService;
  private HomeModuleServiceImpl homeModuleService;

  @Spy private ModelMapper modelMapper;
  HomeModuleServiceImpl homemoduleService;

  HomeModuleArchivalRepository homeModuleArchivalRepository;
  @Mock SegmentService segmentService;

  @Before
  public void setUp() {
    homeModuleService =
        new HomeModuleServiceImpl(
            repository, homeModuleArchivalRepository, modelMapper, segmentService, hubService);
  }

  @Test
  public void testFindAllActive() {
    homeModuleService.findByActiveState(true);
    verify(repository, times(1)).findAllActive(any());
    verify(repository, times(0)).findAllInactive(any());
  }

  @Test
  public void testFindAllInactive() {
    homeModuleService.findByActiveState(false);
    verify(repository, times(0)).findAllActive(any());
    verify(repository, times(1)).findAllInactive(any());
  }
}
