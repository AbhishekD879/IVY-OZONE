package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import java.io.IOException;
import java.util.Collections;
import java.util.List;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.data.mongodb.core.MongoTemplate;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class BetPackMarketPlacePublicServiceTest implements WithAssertions {

  @Mock private BetPackEnablerRepository repository;

  @Mock private MongoTemplate mongoTemplate;

  @Mock private CustomMongoRepository<BetPackEntity> mongoRepository;

  @InjectMocks private BetPackMarketPlacePublicService service;

  private List<BetPackEntity> betPackEntities;

  @BeforeEach
  void init() throws IOException {
    BetPackMarketPlaceService betPackMarketPlaceService =
        new BetPackMarketPlaceService(mongoRepository, repository);
    service = new BetPackMarketPlacePublicService(betPackMarketPlaceService);
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    betPackEntities =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/betpack/Betpack.json"),
            new TypeReference<List<BetPackEntity>>() {});
  }

  @Test
  void findByAllBetPackTest() {
    given(mongoRepository.findAll()).willReturn(betPackEntities);
    Assertions.assertDoesNotThrow(() -> service.getAllBetPack());
  }

  @Test
  void findActiveBetPackByBrandTest() {
    given(repository.findByBrandAndBetPackActiveTrue(anyString())).willReturn(betPackEntities);
    Assertions.assertDoesNotThrow(() -> service.getActiveBetPackByBrand("bma"));
  }

  @Test
  void findActiveBetPackIdTest() {
    given(repository.findByBrandAndBetPackActiveTrue(anyString())).willReturn(betPackEntities);
    Assertions.assertDoesNotThrow(() -> service.getActiveBetPackId("bma"));
  }

  @Test
  void findAllBetPacksBetweenDateTest() {
    given(mongoTemplate.find(any(), any())).willReturn(Collections.singletonList(betPackEntities));
    Assertions.assertDoesNotThrow(() -> service.findAllBetPacksBetweenDate("bma"));
  }
}
