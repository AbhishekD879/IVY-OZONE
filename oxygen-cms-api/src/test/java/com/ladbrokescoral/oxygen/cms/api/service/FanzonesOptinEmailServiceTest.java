package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneOptinEmailDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneOptinEmailAlreadyExistsException;
import com.ladbrokescoral.oxygen.cms.api.mapping.FanzoneOptinEmailMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesOptinEmailRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesOptinEmailServiceTest extends BDDMockito {

  @InjectMocks private FanzonesOptinEmailService fanzonesOptinEmailService;
  @Mock private FanzonesOptinEmailRepository fanzonesOptinEmailRepository;
  private FanzoneOptinEmail fanzoneOptinEmail = createFanzoneOptinEmail();
  private FanzoneOptinEmailDto fanzoneOptinEmailDto = createFanzoneOptinEmailDto();
  @Mock private FanzonesSycRepository fanzonesSycRepository;
  @Mock ModelMapper modelMapper;
  @InjectMocks FanzoneOptinEmailMapper fanzoneOptinEmailMapper;

  @Before
  public void init() {
    fanzonesOptinEmailService =
        new FanzonesOptinEmailService(fanzonesOptinEmailRepository, fanzonesSycRepository);
  }

  @Test
  public void testToEntity() {
    when(modelMapper.map(any(), any())).thenReturn(fanzoneOptinEmail);
    FanzoneOptinEmail fanzoneOptinEmail1 = fanzoneOptinEmailMapper.toEntity(fanzoneOptinEmailDto);
    assertNotNull(fanzoneOptinEmail1);
  }

  @Test
  public void testFindFanzoneOptinEmailByBrand() {
    when(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneOptinEmail));
    assertNotNull(fanzonesOptinEmailService.findFanzoneOptinEmailByBrand(anyString()));
  }

  @Test
  public void testToGetFanzoneOptinEmail() throws Exception {
    Boolean isFanzoneOptinEmailCreated = false;
    try {
      when(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
          .thenReturn(Optional.empty());
      fanzonesOptinEmailService.getFanzoneOptinEmail(
          fanzoneOptinEmail, fanzoneOptinEmail.getBrand());
    } catch (FanzoneOptinEmailAlreadyExistsException e) {
      isFanzoneOptinEmailCreated = true;
    }
    assertFalse(isFanzoneOptinEmailCreated);
  }

  @Test
  public void testToGetFanzoneOptinEmail1() throws Exception {
    Boolean isFanzoneOptinEmailCreated = false;
    try {
      when(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
          .thenReturn(Optional.of(fanzoneOptinEmail));
      fanzonesOptinEmailService.getFanzoneOptinEmail(
          fanzoneOptinEmail, fanzoneOptinEmail.getBrand());
    } catch (FanzoneOptinEmailAlreadyExistsException e) {
      isFanzoneOptinEmailCreated = true;
    }
    assertTrue(isFanzoneOptinEmailCreated);
  }

  @Test
  public void testToSetSeasonStartAndEndDAte() throws Exception {
    Boolean isFanzoneSycPresent = false;
    try {
      when(fanzonesSycRepository.findByBrand(anyString())).thenReturn(Collections.emptyList());
      fanzonesOptinEmailService.setSeasonStartAndEndDateFromFanzoneSyc(
          fanzoneOptinEmail, fanzoneOptinEmail.getBrand());
    } catch (IndexOutOfBoundsException e) {
      isFanzoneSycPresent = true;
    }
    assertFalse(isFanzoneSycPresent);
  }

  private static FanzoneOptinEmail createFanzoneOptinEmail() {
    FanzoneOptinEmail entity = new FanzoneOptinEmail();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFanzoneEmailPopupDescription("Abc");
    entity.setFanzoneEmailPopupDontShowThisAgain("abc");
    entity.setFanzoneEmailPopupOptIn("abc");
    entity.setFanzoneEmailPopupRemindMeLater("abc");
    entity.setFanzoneEmailPopupTitle("abc");
    return entity;
  }

  private static FanzoneOptinEmailDto createFanzoneOptinEmailDto() {
    FanzoneOptinEmailDto entity = new FanzoneOptinEmailDto();
    entity.setBrand("ladbrokes");
    entity.setFanzoneEmailPopupDescription("Abc");
    entity.setFanzoneEmailPopupDontShowThisAgain("abc");
    entity.setFanzoneEmailPopupOptIn("abc");
    entity.setFanzoneEmailPopupRemindMeLater("abc");
    entity.setFanzoneEmailPopupTitle("abc");
    return entity;
  }
}
