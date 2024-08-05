package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.VirtualNextEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualNextEvent;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualNextEventsRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class VirtualNextEventsServiceTest {

  @Mock private VirtualNextEventsRepository repository;

  @Mock private SiteServeApiProvider siteServeApiProvider;

  private VirtualNextEventsService service;

  @BeforeEach
  public void init() {
    this.service = new VirtualNextEventsService(repository, siteServeApiProvider);
  }

  @Test
  void testEventsDisabled() {

    Mockito.when(this.repository.findByBrand(Mockito.anyString()))
        .thenReturn(Collections.singletonList(createEntity()));
    List<VirtualNextEventDto> dtos = this.service.readByBrandAndActive("bma");
    Assertions.assertEquals(0, dtos.size());
  }

  @Test
  void testActiveEvents() {
    VirtualNextEvent entity = createEntity();
    entity.setDisabled(false);
    entity.setBrand("ladbrokes");
    Mockito.when(this.repository.findByBrand(Mockito.anyString()))
        .thenReturn(Collections.singletonList(entity));
    List<VirtualNextEventDto> dtos = this.service.readByBrandAndActive("ladbrokes");
    Assertions.assertEquals(1, dtos.size());
    Assertions.assertEquals("football", dtos.get(0).getTitle());
  }

  private VirtualNextEvent createEntity() {
    VirtualNextEvent entity = new VirtualNextEvent();
    entity.setDisabled(true);
    entity.setId(UUID.randomUUID().toString());
    entity.setTitle("football");
    entity.setClassIds("442");
    entity.setTypeIds("555");
    entity.setBrand("bma");
    return entity;
  }
}
