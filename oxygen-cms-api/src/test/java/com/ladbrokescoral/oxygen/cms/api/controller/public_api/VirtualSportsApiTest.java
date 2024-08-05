package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.assertj.core.api.Java6Assertions.assertThat;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.VirtualSportPublicService;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class VirtualSportsApiTest {
  private final String brand = "TestBrand";

  @Mock private VirtualSportPublicService virtualSportPublicService;

  @InjectMocks private VirtualSportsApi api;

  @Test
  public void findVirtualSportsConfigsNoneExist() {
    when(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand))
        .thenReturn(Collections.emptyList());

    assertThat(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand)).isEmpty();
  }

  @Test
  public void findVirtualSportsConfigs() {
    List<VirtualSportDto> expected =
        Collections.singletonList(new VirtualSportDto().setId(UUID.randomUUID().toString()));

    when(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand))
        .thenReturn(expected);

    assertThat(api.findVirtualSportsConfigs(brand)).isSameAs(expected);
  }
}
