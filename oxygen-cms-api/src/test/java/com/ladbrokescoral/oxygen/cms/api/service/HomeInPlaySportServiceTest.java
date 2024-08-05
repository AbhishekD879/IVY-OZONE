package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.mock.mockito.MockBean;

public class HomeInPlaySportServiceTest {
  private HomeInplaySportService service;
  @MockBean private HomeInplaySportRepository repository;
  @MockBean private SportModuleRepository sportModuleRepository;
  @MockBean private SportModuleArchivalRepository sportModuleArchivalRepository;

  @MockBean private ModelMapper modelMapper;
  @MockBean private SegmentService segmentService;

  @Before
  public void init() throws Exception {
    repository = Mockito.mock(HomeInplaySportRepository.class);
    service =
        new HomeInplaySportService(
            repository,
            sportModuleRepository,
            sportModuleArchivalRepository,
            modelMapper,
            segmentService);
  }

  @Test
  public void testDeleteWhenThePointIsNotPresent() {
    Mockito.when(repository.findById("61ded854655d8c6879be78a0")).thenReturn(Optional.empty());
    service.delete("61ded854655d8c6879be78a0");
    verify(repository, times(1)).findById(anyString());
  }

  @Test
  public void testAchivalMap() {
    service.prepareArchivalEntity(null);
    verify(repository, times(0)).save(Mockito.any());
  }
}
