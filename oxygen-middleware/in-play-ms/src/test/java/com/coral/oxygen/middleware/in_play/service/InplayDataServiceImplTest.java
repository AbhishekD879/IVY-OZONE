package com.coral.oxygen.middleware.in_play.service;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.common.configuration.DistributedKey;
import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.service.GenerationStorageService;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.google.gson.Gson;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.mockito.MockedStatic;

public class InplayDataServiceImplTest {

  private DistributedInstance distributedInstance;
  private GenerationStorageService generationStorageService;
  private InplayDataServiceImpl inplayDataService;
  private Gson gson = new Gson();
  private String version = "123";

  @Before
  public void setUp() {
    distributedInstance = mock(DistributedInstance.class);
    generationStorageService = mock(GenerationStorageService.class);
    inplayDataService =
        new InplayDataServiceImpl(gson, distributedInstance, generationStorageService);
  }

  @Test
  public void getVirtualSportDataFail() {
    VirtualSportEvents vs = new VirtualSportEvents("Cricket", 2);
    List<VirtualSportEvents> vsList = Arrays.asList(vs);

    when(distributedInstance.getValue(DistributedKey.VIRTUAL_SPORTS_STRUCTURE_MAP, version))
        .thenReturn(gson.toJson(vsList));

    try (MockedStatic<URLDecoder> urlDecoderStatic = mockStatic(URLDecoder.class)) {
      urlDecoderStatic
          .when(() -> URLDecoder.decode(anyString(), anyString()))
          .thenThrow(new UnsupportedEncodingException());

      assertTrue(inplayDataService.getVirtualSportData(version).isEmpty());
    }
  }
}
