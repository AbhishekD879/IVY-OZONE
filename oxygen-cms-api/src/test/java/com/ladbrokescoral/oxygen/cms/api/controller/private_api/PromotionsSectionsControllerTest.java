package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionSectionDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SectionUpdatingOrDeletingForbidden;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class PromotionsSectionsControllerTest {
  @Mock private PromotionSectionService service;
  @Mock private WysiwygService wysiwygService;
  @Mock private MultipartFile file;

  private PromotionsSections controller;

  @Before
  public void initTest() {
    this.controller = new PromotionsSections(service, wysiwygService);
  }

  @Test
  public void readUnasignedPromotionSectionWhenUserDoesNotCreateSectionBefore() throws Exception {
    UserService userService = mock(UserService.class);
    controller.setUserService(userService);
    final PromotionSection section =
        TestUtil.deserializeWithJackson(
            "controller/private_api/unassignedSection.json", PromotionSection.class);
    doReturn(Optional.empty()).when(service).findOne(anyString());
    doReturn(section).when(service).unassignedSection(anyString());

    final PromotionSection responseEntity = controller.read("bma", "bma");

    assertEquals(section, responseEntity);
  }

  @Test(expected = NotFoundException.class)
  public void readWhenNotFound() throws Exception {
    UserService userService = mock(UserService.class);
    controller.setUserService(userService);
    final PromotionSection section =
        TestUtil.deserializeWithJackson(
            "controller/private_api/unassignedSection.json", PromotionSection.class);
    doReturn(Optional.empty()).when(service).findOne(anyString());

    final PromotionSection responseEntity = controller.read("bma", "123");

    assertEquals(section, responseEntity);
  }

  @Test(expected = SectionUpdatingOrDeletingForbidden.class)
  public void deleteUnassignedPromotionSectionThenThrowException() {
    final ResponseEntity responseEntity = controller.delete("bma", "bma");
  }

  @Test(expected = SectionUpdatingOrDeletingForbidden.class)
  public void updateUnassignedPromotionSectionThenThrowException() {
    final PromotionSection responseEntity =
        controller.update("bma", "bma", new PromotionSectionDto());
  }
}
