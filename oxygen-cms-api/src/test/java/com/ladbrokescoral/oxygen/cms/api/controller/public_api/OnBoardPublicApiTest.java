package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CrcOnBoardingService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OnBoardPublicService;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.modelmapper.ModelMapper;

class OnBoardPublicApiTest {

  private OnBoardPublicService onBoardPublicService;
  private CrcOnBoardingService crcOnBoardingService;
  private OnBoardPublicApi onBoardPublicApi;

  @BeforeEach
  void setUp() {
    crcOnBoardingService = mock(CrcOnBoardingService.class);
    ModelMapper modelMapper = new ModelMapper();
    onBoardPublicService = new OnBoardPublicService(crcOnBoardingService, modelMapper);
    onBoardPublicApi = new OnBoardPublicApi(onBoardPublicService);
  }

  @Test
  void testGetOnBoardDto() {
    String brand = "ladbrokes";
    List<CrcOnBoarding> emptyCrcOnBoardingList = new ArrayList<>();
    when(crcOnBoardingService.findByBrand(brand)).thenReturn(emptyCrcOnBoardingList);
    OnBoardDto result = onBoardPublicApi.getOnBoardDto(brand);
    assertNotNull(result);
  }

  @Test
  void testGetOnBoard_WithEmptyLists() {
    String brand = "ladbrokes";
    when(crcOnBoardingService.findByBrand(brand)).thenReturn(new ArrayList<>());
    OnBoardDto onBoardDto = onBoardPublicService.getOnBoard(brand);
    assertNotNull(onBoardDto);
  }

  @Test
  void testGetOnBoard_WithNonEmptyLists() {
    String brand = "ladbrokes";
    List<CrcOnBoarding> nonEmptyCrcOnBoardingList = new ArrayList<>();
    nonEmptyCrcOnBoardingList.add(new CrcOnBoarding());
    when(crcOnBoardingService.findByBrand(brand)).thenReturn(nonEmptyCrcOnBoardingList);
    OnBoardDto onBoardDto = onBoardPublicService.getOnBoard(brand);
    assertNotNull(onBoardDto);
  }

  @Test
  void testGetCrcOnBoardingDto() {
    String brand = "ladbrokes";
    CrcOnBoardingDto mockCrcOnBoardingDto = new CrcOnBoardingDto();
    List<CrcOnBoarding> crcOnBoardingList = new ArrayList<>();
    when(crcOnBoardingService.findByBrand(brand)).thenReturn(crcOnBoardingList);
    CrcOnBoardingDto crcOnBoardingDto = onBoardPublicService.getCrcOnBoardingDto(brand);
    assertEquals(mockCrcOnBoardingDto, crcOnBoardingDto);
  }
}
