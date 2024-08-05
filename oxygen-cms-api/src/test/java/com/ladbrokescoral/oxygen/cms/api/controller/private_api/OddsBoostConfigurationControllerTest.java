package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.OddsBoostConfigurationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class OddsBoostConfigurationControllerTest extends BDDMockito {

  @Mock private OddsBoostConfigurationService service;
  @Mock private MultipartFile file;

  @InjectMocks private OddsBoostConfigurationController controller;

  @Test(expected = NotFoundException.class)
  public void uploadImageWhenEntityNotFoundThenReturnNotFoundTest() {
    doReturn(Optional.empty()).when(service).findOne(anyString());

    controller.uploadImage("bma", file, FileType.SVG);
  }

  @Test
  public void uploadImageWhenFileTypeIsNotCorrectThenReturnBadRequestTest() {

    ResponseEntity response = controller.uploadImage("bma", file, FileType.IMAGE);

    assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    assertEquals("Failed to upload image", response.getBody());
  }

  @Test
  public void uploadImageTest() {
    OddsBoostConfigEntity entity = new OddsBoostConfigEntity();
    doReturn(Optional.of(entity)).when(service).findOne(anyString());
    doReturn(Optional.of(entity)).when(service).attachSvgImage(entity, file);
    doReturn(entity).when(service).save(entity);

    ResponseEntity response = controller.uploadImage("bma", file, FileType.SVG);

    verify(service, times(1)).save(entity);
    assertEquals(HttpStatus.OK, response.getStatusCode());
  }

  @Test(expected = NotFoundException.class)
  public void removeImageWhenEntityNotFoundThenReturnNotFoundTest() {
    doReturn(Optional.empty()).when(service).findOne(anyString());

    controller.removeImage("bma", FileType.SVG);
  }

  @Test
  public void removeImageWhenFileTypeIsNotCorrectThenReturnBadRequestTest() {

    ResponseEntity response = controller.removeImage("bma", FileType.IMAGE);

    assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    assertEquals("Failed to remove image", response.getBody());
  }

  @Test
  public void removeImageTest() {

    OddsBoostConfigEntity entity = new OddsBoostConfigEntity();
    doReturn(Optional.of(entity)).when(service).findOne(anyString());
    doReturn(Optional.of(entity)).when(service).removeSvgImage(entity);
    doReturn(entity).when(service).save(entity);

    ResponseEntity response = controller.removeImage("bma", FileType.SVG);

    verify(service, times(1)).save(entity);
    assertEquals(HttpStatus.OK, response.getStatusCode());
  }

  @Test
  public void readWhenNotFindThenReturnDefaultObject() throws Exception {

    doReturn(Optional.empty()).when(service).findOne("bma");

    OddsBoostConfigEntity response = controller.read("bma");

    verify(service, times(1)).findOne("bma");
    assertEquals(
        response,
        TestUtil.deserializeWithJackson("test/oddsboost_empty.json", OddsBoostConfigEntity.class));
  }

  @Test
  public void updateWhenObjectIsNotCreatedThenCreatedNewObjectAndReturnIt() throws Exception {

    UserService userService = mock(UserService.class);
    controller.setUserService(userService);
    final OddsBoostConfigEntity oddsBoostConfigEntity =
        TestUtil.deserializeWithJackson("test/oddsboost.json", OddsBoostConfigEntity.class);
    doReturn(Optional.empty()).when(service).findOne("bma");
    doReturn(oddsBoostConfigEntity).when(service).prepareModelBeforeSave(oddsBoostConfigEntity);
    doReturn(oddsBoostConfigEntity).when(service).save(oddsBoostConfigEntity);

    OddsBoostConfigEntity response = controller.update("bma", oddsBoostConfigEntity);

    verify(service, times(1)).findOne("bma");
    verify(service, times(1)).prepareModelBeforeSave(oddsBoostConfigEntity);
    verify(service, times(1)).save(oddsBoostConfigEntity);
    assertEquals(response, oddsBoostConfigEntity);
  }

  @Test
  public void updateWhenObjectIsCreatedThenUpdateNewObjectAndReturnIt() throws Exception {
    UserService userService = mock(UserService.class);
    controller.setUserService(userService);
    final OddsBoostConfigEntity oddsBoostConfigEntity =
        TestUtil.deserializeWithJackson("test/created_oddsboost.json", OddsBoostConfigEntity.class);
    final OddsBoostConfigEntity updated =
        TestUtil.deserializeWithJackson("test/oddsboost.json", OddsBoostConfigEntity.class);
    doReturn(Optional.of(oddsBoostConfigEntity)).when(service).findOne("bma");
    doReturn(updated).when(service).update(any(), any());

    OddsBoostConfigEntity response = controller.update("bma", oddsBoostConfigEntity);

    verify(service, times(1)).findOne("bma");
    verify(service, times(1)).update(any(), any());
    assertEquals(response, updated);
  }
}
