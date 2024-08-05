package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.repository.OverlayRepository;
import com.ladbrokescoral.oxygen.cms.api.service.OverlayService;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class OverlayServiceTest {
  @Mock private OverlayRepository overlayRepository;

  private OverlayService overlayService;

  @Test
  public void testFindByBrand() {
    overlayService = new OverlayService(overlayRepository);
    when(overlayRepository.findByBrand("ladbrokes")).thenReturn(getOverlay());
    List<Overlay> list = overlayService.findByBrand("ladbrokes");
    Assert.assertEquals(1, list.size());
  }

  @Test(expected = BadRequestException.class)
  public void testPrepareModelBeforeSave() {
    overlayService = new OverlayService(overlayRepository);
    when(overlayRepository.findOneByBrand("ladbrokes"))
        .thenReturn(Optional.of(getOverlay().get(0)));
    overlayService.prepareModelBeforeSave(getOverlay().get(0));
  }

  @Test
  public void testElsePrepareModelBeforeSave() {
    overlayService = new OverlayService(overlayRepository);
    when(overlayRepository.findOneByBrand("ladbrokes")).thenReturn(Optional.empty());
    Overlay result = overlayService.prepareModelBeforeSave(getOverlay().get(0));
    Assert.assertNotNull(result);
  }

  List<Overlay> getOverlay() {
    List<Overlay> list = new ArrayList<>();
    Overlay overlay = new Overlay();
    overlay.setBrand("ladbrokes");
    overlay.setHeaderTitle("header");
    list.add(overlay);
    return list;
  }
}
