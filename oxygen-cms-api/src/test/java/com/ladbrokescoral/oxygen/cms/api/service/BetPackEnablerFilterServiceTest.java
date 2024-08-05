package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.BPMDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackFilterDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerFilterRepository;
import java.lang.reflect.Field;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BetPackEnablerFilterServiceTest {
  @Mock private BetPackEnablerFilterRepository betPackEnablerFilterRepository;

  @InjectMocks private BetPackEnablerFilterService service;
  private List<BetPackFilter> betPackFilters;

  private BetPackFilterDto filterDto;
  @Mock private BPMDto bpmdto;
  private BetPackEntity betPackEntity;

  @Before
  public void init() throws Exception {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    betPackFilters =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/betpack/BetpackFilter.json"),
            new TypeReference<List<BetPackFilter>>() {});
    filterDto = new BetPackFilterDto();
    filterDto.setBrand("coral");
    filterDto.setFilterName("Football");
    filterDto.setFilterActive(true);
    Field activeBetPackLimit =
        BetPackEnablerFilterService.class.getDeclaredField("activeFilterLimit");
    activeBetPackLimit.setAccessible(true);
    activeBetPackLimit.set(service, 8);

    betPackEntity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/Betpack.json", BetPackEntity.class);
  }

  @Test
  public void testFindAllActiveBetPackFilter() {

    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    List<BetPackFilter> betPackFilter = service.findAllActiveBetPackFilter(anyString());
    verify(betPackEnablerFilterRepository, times(1)).findByBrandAndFilterActiveTrue(anyString());
    Assert.assertNotNull(betPackFilter);
  }

  @Test
  public void testDeleteByFilterName() {
    when(betPackEnablerFilterRepository.deleteByFilterName(anyString())).thenReturn(anyLong());
    Long betPackFilter = service.deleteByFilterName("abc");
    verify(betPackEnablerFilterRepository, times(1)).deleteByFilterName(anyString());
    Assert.assertNotNull(betPackFilter);
  }

  @Test
  public void checkActiveFilter_WithInActiveFilterTest() {
    filterDto.setFilterActive(false);
    BetPackFilter betPackFilter = service.checkActiveFilterLimit(anyString(), filterDto);
    Assert.assertNotNull(betPackFilter.getBrand());
  }

  @Test
  public void checkActiveFilter_WithinLimitTest() {
    betPackFilters.remove(7);
    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    Assertions.assertDoesNotThrow(() -> service.checkActiveFilterLimit(anyString(), filterDto));
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void checkActiveFilter_ExceedLimitTest() {
    betPackFilters.add(new BetPackFilter());
    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    service.checkActiveFilterLimit(anyString(), filterDto);
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void checkActiveFilter_EqualLimitTest() {
    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    service.checkActiveFilterLimit(anyString(), filterDto);
  }

  @Test
  public void checkActiveFilter_EqualLimit_ValidId_ActiveFilterTest() {
    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    Assertions.assertDoesNotThrow(
        () -> service.checkActiveFilterLimit("62d9a5bfd1dbe60da8170655", filterDto));
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void checkActiveFilter_EqualLimit_ValidId_InActiveFilterTest() {
    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    service.checkActiveFilterLimit("62d93d2000d5db70deb3a8d7", filterDto);
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void checkActiveFilter_ExceedLimit_InValidId_InActiveFilterTest() {
    betPackFilters.add(new BetPackFilter());
    when(betPackEnablerFilterRepository.findByBrandAndFilterActiveTrue(anyString()))
        .thenReturn(betPackFilters);
    service.checkActiveFilterLimit("invalidId", filterDto);
  }

  @Test
  public void testGetFilterStatus() {
    Instant now = Instant.now().minus(30, ChronoUnit.DAYS);
    betPackEntity.setBetPackEndDate(now);
    betPackEntity.setFilterList(Arrays.asList("NONE"));
    service.getFilterStatus("today", bpmdto, Arrays.asList(betPackEntity));
    assertNotNull(bpmdto);
  }

  @Test
  public void testGetFilterStatusFalse() {
    service.getFilterStatus("today", bpmdto, Arrays.asList(betPackEntity));
    assertNotNull(bpmdto);
  }

  @Test
  public void testGetFilterStatusPastDate() {
    betPackEntity.setBetPackEndDate(Instant.now());
    service.getFilterStatus("today", bpmdto, Arrays.asList(betPackEntity));
    assertNotNull(bpmdto);
  }

  @Test
  public void testValidateSortOrder() {
    filterDto.setSortOrder(1.0);
    service.validateSortOrder(filterDto);
    assertNotNull(filterDto);
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void testValidateSortOrderNullValues() {
    service.validateSortOrder(filterDto);
  }
}
