package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.service.SurfaceBetService;
import java.util.HashSet;
import java.util.Set;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

/** @author PBalarangakumar 25-09-2023 */
@RunWith(MockitoJUnitRunner.class)
public class SurfaceBetApiTest {

  @Mock private SurfaceBetService surfaceBetService;

  private SurfaceBetApi surfaceBetApi;

  @Before
  public void init() {

    surfaceBetApi = new SurfaceBetApi(surfaceBetService);
  }

  @Test
  public void findActiveSurfaceBetsByBrand() {
    Set<String> activeSurfaceBets = new HashSet<>();
    activeSurfaceBets.add("selectionId1#surfaceBetId1");
    activeSurfaceBets.add("selectionId2#surfaceBetId2");
    activeSurfaceBets.add("selectionId3#surfaceBetId3");

    when(surfaceBetService.findActiveSurfaceBetsByBrand("bma")).thenReturn(activeSurfaceBets);
    surfaceBetApi.findActiveSurfaceBetsByBrand("bma");
    verify(surfaceBetService, times(1)).findActiveSurfaceBetsByBrand("bma");
  }

  @Test
  public void findActiveSurfaceBetsByBrandEmpty() {
    when(surfaceBetService.findActiveSurfaceBetsByBrand("bma")).thenReturn(new HashSet<>());
    surfaceBetApi.findActiveSurfaceBetsByBrand("bma");
    verify(surfaceBetService, times(1)).findActiveSurfaceBetsByBrand("bma");
  }
}
