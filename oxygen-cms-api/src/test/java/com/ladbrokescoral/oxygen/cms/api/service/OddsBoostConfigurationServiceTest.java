package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostConfigurationRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class OddsBoostConfigurationServiceTest {
  @Mock private OddsBoostConfigurationRepository repository;
  @Mock private SvgEntityService<OddsBoostConfigEntity> svgEntityService;
  @Mock private MultipartFile svgFile;
  private String svgMenuPath = "svgMenuPath";
  private OddsBoostConfigurationService service;

  @Before
  public void init() {
    service = new OddsBoostConfigurationService(repository, svgEntityService, svgMenuPath);
  }

  @Test
  public void getPublicDTOTest() {
    final String brand = "brand";
    OddsBoostConfigEntity entity = getEntity();
    doReturn(Optional.of(entity)).when(repository).findById(brand);

    OddsBoostConfigDTO publicDTO = service.getPublicDTO(brand);
    verify(repository, times(1)).findById(brand);
    assertPublicDTO(publicDTO, entity);
  }

  @Test
  public void attachSvgImageTest() {
    OddsBoostConfigEntity entity = getEntity();
    doReturn(Optional.of(entity))
        .when(svgEntityService)
        .attachSvgImage(entity, svgFile, svgMenuPath);

    service.attachSvgImage(entity, svgFile);
    verify(svgEntityService, times(1)).attachSvgImage(entity, svgFile, svgMenuPath);
  }

  @Test
  public void removeSvgImageTest() {
    OddsBoostConfigEntity entity = getEntity();
    doReturn(Optional.of(entity)).when(svgEntityService).removeSvgImage(entity);

    service.removeSvgImage(entity);
    verify(svgEntityService, times(1)).removeSvgImage(entity);
  }

  private void assertPublicDTO(OddsBoostConfigDTO publicDTO, OddsBoostConfigEntity entity) {
    assertEquals(publicDTO.getLang(), entity.getLang());
    assertEquals(publicDTO.getLoggedInHeaderText(), entity.getLoggedInHeaderText());
    assertEquals(publicDTO.getLoggedOutHeaderText(), entity.getLoggedOutHeaderText());
    assertEquals(publicDTO.getSvg(), entity.getSvg());
    assertEquals(publicDTO.getTermsAndConditionsText(), entity.getTermsAndConditionsText());
    assertEquals(publicDTO.getMoreLink(), entity.getMoreLink());
    assertEquals(publicDTO.getSvgId(), entity.getSvgId());
    assertEquals(publicDTO.getSvgFilename(), entity.getSvgFilename().getFilename());
    assertEquals(publicDTO.isAllowUserToToggleVisibility(), entity.isAllowUserToToggleVisibility());
    assertEquals(publicDTO.getDaysToKeepPopupHidden(), entity.getDaysToKeepPopupHidden());
    assertEquals(publicDTO.getNoTokensText(), entity.getNoTokensText());
    assertEquals(publicDTO.getCountDownTimer(), entity.getCountDownTimer());
  }

  private OddsBoostConfigEntity getEntity() {
    OddsBoostConfigEntity entity = new OddsBoostConfigEntity();
    entity.setEnabled(true);
    entity.setLoggedInHeaderText("loggedIn");
    entity.setLoggedOutHeaderText("loggedOut");
    entity.setTermsAndConditionsText("termsAndCondition");
    entity.setMoreLink("moreLink");
    SvgFilename svgFilename = new SvgFilename();
    svgFilename.setFilename("fileName");
    entity.setLang("en");
    entity.setSvg("svg");
    entity.setSvgId("#amfhcrwtqg");
    entity.setSvgFilename(svgFilename);
    entity.setDaysToKeepPopupHidden(7);
    entity.setCountDownTimer("2");
    entity.setNoTokensText("NO token");
    return entity;
  }
}
