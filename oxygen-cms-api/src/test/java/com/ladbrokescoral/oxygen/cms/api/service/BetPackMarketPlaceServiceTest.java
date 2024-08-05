package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerRepository;
import java.lang.reflect.Field;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.data.mongodb.core.MongoTemplate;

@RunWith(MockitoJUnitRunner.class)
public class BetPackMarketPlaceServiceTest {

  @Mock private MongoTemplate mongoTemplate;

  @Mock private BetPackEnablerRepository betPackEnablerRepository;

  @InjectMocks private BetPackMarketPlaceService service;
  private List<BetPackEntity> betPackEntities;

  private BetPackDto betPackDto;

  @Before
  public void init() throws Exception {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    betPackEntities =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/betpack/Betpack.json"),
            new TypeReference<List<BetPackEntity>>() {});
    betPackDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackDtos.json", BetPackDto.class);
    Field activeBetPackLimit =
        BetPackMarketPlaceService.class.getDeclaredField("activeBetPackLimit");
    activeBetPackLimit.setAccessible(true);
    activeBetPackLimit.set(service, 20);
  }

  @Test
  public void testGetActiveBetPackId() {
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    List<String> betPacks = service.getActiveBetPackId(anyString());
    verify(betPackEnablerRepository, times(1)).findByBrandAndBetPackActiveTrue(anyString());
    Assert.assertNotNull(betPacks);
  }

  @Test
  public void testFindAllBetPackEntities() {
    given(betPackEnablerRepository.findAll()).willReturn(betPackEntities);
    List<BetPackEntity> betPacks = service.findAllBetPackEntities();
    verify(betPackEnablerRepository, times(1)).findAll();
    Assert.assertNotNull(betPacks);
  }

  @Test
  public void testFindAllActiveBetPackEntities() {
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    List<BetPackEntity> betPacks = service.findAllActiveBetPackEntities(anyString());
    verify(betPackEnablerRepository, times(1)).findByBrandAndBetPackActiveTrue(anyString());
    Assert.assertNotNull(betPacks);
  }

  @Test
  public void checkActiveBetPack_WithInActiveBetPackTest() {
    betPackDto.setBetPackStartDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackDto.setBetPackActive(false);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    BetPackEntity betPacks = service.checkActiveBetPackLimit(anyString(), betPackDto);
    Assert.assertNotNull(betPacks.getBrand());
  }

  @Test
  public void checkActiveBetPack_WithinLimitTest() {
    betPackDto.setBetPackStartDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().minus(1, ChronoUnit.DAYS));
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    Assertions.assertDoesNotThrow(() -> service.checkActiveBetPackLimit(anyString(), betPackDto));
  }

  private void getRequiredBetPackEntity(List<BetPackEntity> entityList, int size) {
    int i = 1;
    while (i <= size) {
      BetPackEntity betPack = new BetPackEntity();
      betPack.setId(UUID.randomUUID().toString().replaceAll("_", ""));
      entityList.add(betPack);
      i++;
    }
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void checkActiveBetPack_ExceedLimitTest() {
    getRequiredBetPackEntity(betPackEntities, 18);
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    service.checkActiveBetPackLimit(anyString(), betPackDto);
  }

  @Test(expected = BetPackMarketPlaceException.class)
  public void checkActiveBetPack_EqualLimitTest() {
    getRequiredBetPackEntity(betPackEntities, 17);
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    service.checkActiveBetPackLimit(anyString(), betPackDto);
  }

  @Test
  public void checkActiveBetPack_EqualLimit_ValidId_ActiveFilterTest() {
    betPackDto.setBetPackStartDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    getRequiredBetPackEntity(betPackEntities, 17);
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    Assertions.assertDoesNotThrow(
        () -> service.checkActiveBetPackLimit("6284cf4860f795132aa9f0c", betPackDto));
  }

  @Test
  public void checkActiveBetPack_EqualLimit_ValidId_ActiveFilterFalseTest() {
    betPackDto.setBetPackStartDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    getRequiredBetPackEntity(betPackEntities, 17);
    betPackEntities.get(1).setBetPackActive(false);
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    assertThrows(
        BetPackMarketPlaceException.class,
        () -> service.checkActiveBetPackLimit("6284cf4860f795132aa9f0c", betPackDto));
  }

  @Test
  public void checkActiveBetPack__EqualLimit_ValidId_InActiveBetPackTest() {
    getRequiredBetPackEntity(betPackEntities, 17);
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    assertThrows(
        BetPackMarketPlaceException.class,
        () -> service.checkActiveBetPackLimit("62d7e7567954100f21807d8f", betPackDto));
  }

  @Test
  public void checkActiveBetPack_WithinLimit_InValidId_InActiveBetPackTest() {
    betPackDto.setBetPackStartDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().minus(1, ChronoUnit.DAYS));
    given(betPackEnablerRepository.findByBrandAndBetPackActiveTrue(anyString()))
        .willReturn(betPackEntities);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    service.checkActiveBetPackLimit("invalidId", betPackDto);
  }

  @Test
  public void findAllBetPacksBetweenDateTest() {
    betPackEnablerRepository = mock(BetPackEnablerRepository.class, CALLS_REAL_METHODS);
    given(mongoTemplate.find(any(), any())).willReturn(Collections.singletonList(betPackEntities));
    Assertions.assertDoesNotThrow(
        () ->
            betPackEnablerRepository
                .findByBrandAndBetPackEndDateIsAfterOrMaxTokenExpirationDateIsAfter(
                    "bma", Instant.now(), Instant.now()));
    Assertions.assertDoesNotThrow(() -> service.findAllBetPacksBetweenDate("bma"));
  }

  @Test
  public void testValidateSortOrder() {
    betPackDto.setSortOrder(1.0);
    service.validateSortOrder(betPackDto);
    assertNotNull(betPackDto);
  }

  @Test
  public void checkDateValidationAfterStartDateTest() {
    betPackDto.setBetPackStartDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackDto.setBetPackActive(false);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    BetPackEntity betPacks = service.checkDateValidation(anyString(), betPackDto);

    Assert.assertNotNull(betPacks.getBrand());
  }

  @Test
  public void checkDateValidationTest() {
    betPackDto.setBetPackStartDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().plus(1, ChronoUnit.DAYS));
    betPackDto.setBetPackActive(false);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    BetPackEntity betPacks = service.checkDateValidation(anyString(), betPackDto);
    Assert.assertNotNull(betPacks.getBrand());
  }

  @Test
  public void checkDateValidationBeforeStartDateTest() {
    betPackDto.setBetPackStartDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackDto.setMaxTokenExpirationDate(Instant.now().minus(1, ChronoUnit.DAYS));
    betPackDto.setBetPackActive(false);
    given(betPackEnablerRepository.findById(anyString()))
        .willReturn(Optional.of(betPackEntities.get(1)));
    BetPackEntity betPacks = service.checkDateValidation(anyString(), betPackDto);
    Assert.assertNotNull(betPacks.getBrand());
  }

  @Test
  public void testValidateSortOrderNullValues() {
    betPackDto.setSortOrder(null);
    assertThrows(BetPackMarketPlaceException.class, () -> service.validateSortOrder(betPackDto));
  }
}
