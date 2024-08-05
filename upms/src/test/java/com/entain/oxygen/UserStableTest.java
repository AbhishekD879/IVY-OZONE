package com.entain.oxygen;

import static com.mongodb.assertions.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.entain.oxygen.bpp.BppConfigLightProps;
import com.entain.oxygen.bpp.BppConfiguration;
import com.entain.oxygen.configuration.SiteServerApiConfig;
import com.entain.oxygen.dto.ChildrenDto;
import com.entain.oxygen.dto.SSResponseDto;
import com.entain.oxygen.entity.HorseInfo;
import com.entain.oxygen.entity.UserStable;
import com.entain.oxygen.exceptions.SiteServeApiInitializationException;
import com.entain.oxygen.filter.PreferenceFilter;
import com.entain.oxygen.handler.UserStableHandler;
import com.entain.oxygen.model.UserStableDto;
import com.entain.oxygen.repository.UserStableRepository;
import com.entain.oxygen.router.OptionsHandler;
import com.entain.oxygen.router.UserStableRouter;
import com.entain.oxygen.service.BppService;
import com.entain.oxygen.service.HorseRacingDataService;
import com.entain.oxygen.service.UserStableService;
import com.entain.oxygen.service.siteserver.SiteServerApiProvider;
import com.entain.oxygen.service.siteserver.SiteServerApiProviderImpl;
import com.entain.oxygen.service.siteserver.SiteServerService;
import com.entain.oxygen.service.siteserver.SiteServerServiceImpl;
import com.entain.oxygen.util.EventTransformerUtil;
import com.entain.oxygen.util.TestUtil;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.time.LocalDateTime;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.modelmapper.ModelMapper;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.context.annotation.Import;
import org.springframework.data.mongodb.core.FindAndModifyOptions;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.UpdateDefinition;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(SpringExtension.class)
@Import(
    value = {
      BppConfiguration.class,
      ModelMapper.class,
      SiteServerServiceImpl.class,
      SiteServerApiProviderImpl.class,
      SiteServerApiConfig.class
    })
@WebFluxTest(
    value = {
      UserStableHandler.class,
      UserStableRouter.class,
      UserStableService.class,
      UserStableRepository.class,
      ModelMapper.class,
      BppConfigLightProps.class,
      OptionsHandler.class,
      PreferenceFilter.class,
      HorseRacingDataService.class
    })
@MockBeans({@MockBean(CorsEndpointProperties.class)})
@Slf4j
@SuppressWarnings("java:S6068")
class UserStableTest extends AbstractControllerTest {
  @Mock private CacheManager cacheManager;
  @Mock private Cache cache;

  @Mock private SiteServerApiConfig config;
  @Mock private SiteServerApi siteServerApi;
  private SiteServerApiProvider siteServerApiProvider = mock(SiteServerApiProviderImpl.class);

  @MockBean private UserStableRepository userStableRepository;
  @MockBean private ReactiveMongoTemplate reactiveMongoTemplate;

  private SiteServerService siteServerService = mock(SiteServerServiceImpl.class);
  @InjectMocks private HorseRacingDataService horseRacingDataService;

  private ModelMapper modelMapper = mock(ModelMapper.class);
  @MockBean private BppService bppService;

  private UserStableService userStableService = mock(UserStableService.class);

  @BeforeEach
  void init() {
    MockitoAnnotations.openMocks(this);
    Mockito.when(bppService.favUserdata(Mockito.any(String.class)))
        .thenReturn(Mono.just("bob1234@gmail.com"));
  }

  @Test
  void testSaveOperation() {

    Mockito.when(userStableRepository.findByUserName(any())).thenReturn(Mono.empty());

    when(modelMapper.map(any(), any())).thenReturn(getUserStable());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));

    Mockito.when(userStableService.saveUserStable(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoObj())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody(UserStableDto.class)
        .isEqualTo(getUserStableDto());
  }

  @Test
  void testSaveOperationValidate() {

    Mockito.when(userStableRepository.findByUserName(any()))
        .thenReturn(Mono.just(getUserStableDB()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStableDB());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStableDB()));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoObj())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void testSaveOperationInvalidHorseId() {

    Mockito.when(userStableRepository.findByUserName(any()))
        .thenReturn(Mono.just(getUserStableInvalidId()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStableInvalidId());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStableInvalidId()));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableInvalidIdDto())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is4xxClientError();
  }

  @Test
  void testSaveisCrcHorseNull() {

    UserStableDto userStableDtoObj = new UserStableDto();
    userStableDtoObj.setBrand("bma");
    HorseInfo horseInfoDto = new HorseInfo();
    horseInfoDto.setHorseId("1234");
    horseInfoDto.setIsCrcHorse(null);
    LinkedHashSet<HorseInfo> horseInfoListDto = new LinkedHashSet<>();
    horseInfoListDto.add(horseInfoDto);
    userStableDtoObj.setMyStable(horseInfoListDto);

    Mockito.when(userStableRepository.findByUserName(any()))
        .thenReturn(Mono.just(getUserStableDB()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStableDB());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStableDB()));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(userStableDtoObj)
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is4xxClientError();
  }

  @Test
  void testSaveOperationValidateNullCheck() {

    Mockito.when(userStableRepository.findByUserName(any()))
        .thenReturn(Mono.just(getUserStableDBCheck()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStableDBCheck());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStableDBCheck()));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoNullCheck())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void testSaveOperationValidateFalse() {

    Mockito.when(userStableRepository.findByUserName(any())).thenReturn(Mono.just(getUserStable()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStable());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenThrow(new RuntimeException("Duplicate Entry exception"));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoObj())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is4xxClientError();
  }

  @Test
  void testSaveOperationValidateNormalHorse() {

    Mockito.when(userStableRepository.findByUserName(any()))
        .thenReturn(Mono.just(getUserStableHorse()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStableHorse());

    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenThrow(new RuntimeException("Duplicate Entry exception"));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoHorse())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is4xxClientError();
  }

  @Test
  void testSaveOperationExceededLimit() {

    Mockito.when(userStableRepository.findByUserName(any()))
        .thenReturn(Mono.just(getUserStableGTDesiredHorses()));

    when(modelMapper.map(any(), any())).thenReturn(getUserStableGTDesiredHorses());

    Mockito.when(userStableRepository.save(getUserStableGTDesiredHorses()))
        .thenThrow(new RuntimeException("error"));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDto())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is5xxServerError();
  }

  @Test
  void testSaveOperationExceededLimitSwitchIfEmpty1() {
    Mockito.when(userStableRepository.findByUserName(any())).thenReturn(Mono.empty());
    when(modelMapper.map(any(), any())).thenReturn(getUserStableGTDesiredHorses());

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoGTDesiredHorsesCount())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is5xxServerError();
  }

  @Test
  void testSaveOperationException() {
    Mockito.when(userStableRepository.findByUserName(any(String.class)))
        .thenReturn(Mono.just(getUserStable()));

    Mockito.when(modelMapper.map(any(UserStableDto.class), eq(UserStable.class)))
        .thenReturn(getUserStable());
    Mockito.when(userStableService.populateBookmarkTime(any(UserStable.class)))
        .thenReturn(getUserStable());
    Mockito.when(userStableService.saveUserStable(any(UserStable.class)))
        .thenReturn(Mono.error(new RuntimeException("Some error")));

    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDto())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is4xxClientError();
  }

  @Test
  void testSaveFailed() {
    Mockito.when(userStableRepository.findByUserName(any()))
        .thenThrow(new RuntimeException("failed"));
    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDto())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is5xxServerError();
  }

  @Test
  void testDeleteOperationWhenT3IsFalse() {
    Mockito.when(
            reactiveMongoTemplate.findAndModify(
                any(Query.class),
                any(UpdateDefinition.class),
                any(FindAndModifyOptions.class),
                eq(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));
    this.webTestClient
        .delete()
        .uri("/api/my-stable/deleteByHorseId/bma/879?isCrcHorse=false")
        .header("token", "879")
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void testGetOperation() {

    Mockito.when(userStableRepository.findByUserNameAndBrandExcludingNotes(any(String.class)))
        .thenReturn(Mono.just(getUserStable()));

    Mockito.when(modelMapper.map(any(UserStable.class), eq(UserStableDto.class)))
        .thenReturn(getUserStableDto());

    this.webTestClient
        .get()
        .uri("/api/my-stable/getMyStableDataWithoutNotes/bma")
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(UserStableDto.class)
        .isEqualTo(getUserStableDto());
  }

  @Test
  void testGetOperationFailed() {
    Mockito.when(userStableRepository.findByUserNameAndBrandExcludingNotes(any()))
        .thenReturn(Mono.empty());

    this.webTestClient
        .get()
        .uri("/api/my-stable/getMyStableDataWithoutNotes/bma")
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void testGetOperationException() {
    Mockito.when(userStableRepository.findByUserNameAndBrandExcludingNotes(any(String.class)))
        .thenReturn(Mono.error(new RuntimeException("Entity doesn't Exist!")));

    this.webTestClient
        .get()
        .uri("/api/my-stable/getMyStableDataWithoutNotes/bma")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }

  @Test
  void testGetOperationGetHorseNotesById() {

    Mockito.when(userStableRepository.getNotesByHorseId(any(String.class), any(String.class)))
        .thenReturn(Mono.just(getUserStable()));

    Mockito.when(modelMapper.map(any(UserStable.class), eq(UserStableDto.class)))
        .thenReturn(getUserStableDto());

    this.webTestClient
        .get()
        .uri("/api/my-stable/getNoteByHorseId/bma/123")
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void testGetOperationGetHorseNotesByIdWithException() {
    Mockito.when(userStableRepository.getNotesByHorseId(any(String.class), any(String.class)))
        .thenReturn(Mono.error(new RuntimeException("Entity does not exist")));

    this.webTestClient
        .get()
        .uri("/api/my-stable/getNoteByHorseId/bma/123")
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void testUpdate() {

    Mockito.when(
            reactiveMongoTemplate.findAndModify(
                any(Query.class),
                any(UpdateDefinition.class),
                any(FindAndModifyOptions.class),
                eq(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));
    Mockito.when(modelMapper.map(any(UserStable.class), eq(UserStableDto.class)))
        .thenReturn(getUserStableDto());
    this.webTestClient
        .put()
        .uri("/api/my-stable/updateHorseNote")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDto())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(UserStableDto.class)
        .isEqualTo(getUserStableDto());
  }

  @Test
  void testUpdateWithException() {

    Mockito.when(
            reactiveMongoTemplate.findAndModify(
                any(Query.class),
                any(UpdateDefinition.class),
                any(FindAndModifyOptions.class),
                eq(UserStable.class)))
        .thenReturn(Mono.empty());
    this.webTestClient
        .put()
        .uri("/api/my-stable/updateHorseNote")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDto())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isNotFound();
  }

  @Test
  void testUpdateWithNotesEmpty() {

    Mockito.when(modelMapper.map(any(UserStable.class), eq(UserStableDto.class)))
        .thenReturn(getUserStableDtoNotesNull());
    Mockito.when(
            reactiveMongoTemplate.findAndModify(
                any(Query.class),
                any(UpdateDefinition.class),
                any(FindAndModifyOptions.class),
                eq(UserStable.class)))
        .thenReturn(Mono.just(getUserStableNotesNull()));

    this.webTestClient
        .put()
        .uri("/api/my-stable/updateHorseNote")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getUserStableDtoNotesNull())
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void testDeleteOperation() {

    Mockito.when(
            reactiveMongoTemplate.findAndModify(
                any(Query.class),
                any(UpdateDefinition.class),
                any(FindAndModifyOptions.class),
                eq(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));

    this.webTestClient
        .delete()
        .uri("/api/my-stable/deleteByHorseId/bma/123?isCrcHorse=true")
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void testSaveUserStableInvalidHorseId() {
    UserStable userStable = new UserStable();
    userStable.setUserName("bob1234@gmail.com");

    HorseInfo invalidHorse = new HorseInfo();
    invalidHorse.setHorseId("1");
    userStable.setMyStable(new LinkedHashSet<>(Collections.singleton(invalidHorse)));

    when(userStableRepository.findByUserName(any())).thenReturn(Mono.just(new UserStable()));
    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(userStable)
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }

  @Test
  void testSaveUserStableInvalidHorseIdFirsTime() {
    UserStable userStable = new UserStable();
    userStable.setUserName("bob1234@gmail.com");

    HorseInfo invalidHorse = new HorseInfo();
    invalidHorse.setHorseId("1");
    userStable.setMyStable(new LinkedHashSet<>(Collections.singleton(invalidHorse)));

    when(userStableRepository.findByUserName(any())).thenReturn(Mono.empty());
    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(userStable)
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }

  @Test
  void testSaveUserStableInvalidHorseIdFirsTimeException() {
    UserStable userStable = new UserStable();
    userStable.setUserName("bob1234@gmail.com");

    HorseInfo invalidHorse = new HorseInfo();
    invalidHorse.setHorseId("abc");
    userStable.setMyStable(new LinkedHashSet<>(Collections.singleton(invalidHorse)));

    when(userStableRepository.findByUserName(any())).thenReturn(Mono.empty());
    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(userStable)
        .header("token", "123")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }

  @Test
  void testSaveOperationExceededLimitSwitchIfEmpty() {
    Mockito.when(userStableRepository.findByUserName(any())).thenReturn(Mono.just(getUserStable()));
    UserStableDto userStableDto = getUserStableDto1();
    when(modelMapper.map(any(), any())).thenReturn(getUserStable());
    Mockito.when(userStableRepository.save(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));
    when(userStableService.saveUserStable(any(UserStable.class)))
        .thenReturn(Mono.just(getUserStable()));
    this.webTestClient
        .post()
        .uri("/api/my-stable/addHorse")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(userStableDto)
        .header("token", "123")
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void getCachedHorseInfo() throws NoSuchFieldException, IllegalAccessException {

    UserStableService stableService =
        new UserStableService(null, null, horseRacingDataService, modelMapper);
    List<Event> events = Collections.singletonList(new Event());
    List<ChildrenDto> eventDtoList = EventTransformerUtil.copyEventsToEventDtos(events);
    when(cacheManager.getCache(anyString())).thenReturn(cache);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);
    when(cache.get(eq("uk_ie_ss_horse"), eq(List.class))).thenReturn(eventDtoList);
    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(events));
    setPrivateField(horseRacingDataService, "uKIECache", "UK-IE");
    Mono<SSResponseDto> response = stableService.getCachesSSHorseEvents();

    StepVerifier.create(response)
        .expectNextMatches(
            responseDto -> {
              Assertions.assertNotNull(responseDto);
              return true;
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCachedHorseInfoTestCacheNull() {

    List<Event> ssEventList = TestUtil.readJsonArrayFromFile("mystable/ssEvents.json", Event.class);
    SSResponseDto ssResponseDto = new SSResponseDto();
    List<ChildrenDto> eventDtoList = EventTransformerUtil.copyEventsToEventDtos(ssEventList);
    ssResponseDto.setChildren(eventDtoList);
    when(cacheManager.getCache(anyString())).thenReturn(null);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);
    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(ssEventList));

    List<ChildrenDto> response = horseRacingDataService.getCachedHorseData();

    Assertions.assertNotNull(response);
  }

  @Test
  void getCachedHorseInfoTestCacheNotNull() throws NoSuchFieldException, IllegalAccessException {

    List<Event> ssEventList = TestUtil.readJsonArrayFromFile("mystable/ssEvents.json", Event.class);
    SSResponseDto ssResponseDto = new SSResponseDto();
    List<ChildrenDto> eventDtoList = EventTransformerUtil.copyEventsToEventDtos(ssEventList);
    ssResponseDto.setChildren(eventDtoList);
    when(cacheManager.getCache(anyString())).thenReturn(cache);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);
    when(cache.get(eq("uk_ie_ss_horse"), eq(List.class))).thenReturn(eventDtoList);
    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(ssEventList));
    setPrivateField(horseRacingDataService, "uKIECache", "UK-IE");

    List<ChildrenDto> response = horseRacingDataService.getCachedHorseData();
    Assertions.assertNotNull(response);
  }

  @Test
  void getCachedHorseInfoTestCacheNotNullButNoData()
      throws NoSuchFieldException, IllegalAccessException {

    List<Event> ssEventList = TestUtil.readJsonArrayFromFile("mystable/ssEvents.json", Event.class);
    when(cacheManager.getCache(anyString())).thenReturn(cache);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);
    when(cache.get(eq("uk_ie_ss_horse"), eq(List.class))).thenReturn(null);
    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(ssEventList));

    setPrivateField(horseRacingDataService, "uKIECache", "UK-IE");

    List<ChildrenDto> response = horseRacingDataService.getCachedHorseData();

    Assertions.assertNotNull(response);
  }

  @Test
  void testsSSDatawithNoOutcome() throws NoSuchFieldException, IllegalAccessException {

    List<Event> ssDatawithNoOutcome =
        TestUtil.readJsonArrayFromFile("mystable/ssDatawithNoOutcome.json", Event.class);
    when(cacheManager.getCache(anyString())).thenReturn(cache);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);
    when(cache.get(eq("uk_ie_ss_horse"), eq(List.class))).thenReturn(null);
    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(ssDatawithNoOutcome));
    setPrivateField(horseRacingDataService, "uKIECache", "UK-IE");
    List<ChildrenDto> response = horseRacingDataService.getCachedHorseData();
    Assertions.assertNotNull(response);
  }

  @Test
  void testcopyPrices()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Outcome outcome = new Outcome();
    List<Outcome> outcomes = Collections.singletonList(outcome);
    Method copyOutcomesMethod =
        EventTransformerUtil.class.getDeclaredMethod("copyOutcomes", List.class);
    copyOutcomesMethod.setAccessible(true);
    List<ChildrenDto> result = (List<ChildrenDto>) copyOutcomesMethod.invoke(null, outcomes);
    assertNotNull(result);
  }

  @Test
  void testSiteServerApiException() {

    when(config.siteServerAPI()).thenThrow(new SiteServeApiInitializationException());

    Assertions.assertThrows(
        SiteServeApiInitializationException.class, () -> config.siteServerAPI());
  }

  private UserStableDto getUserStableDto1() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("gramy");
    horseInfo.setHorseId("1");
    horseInfo.setNote("wins every race");
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-09-14T15:49:25.820"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStable getUserStable() {
    UserStable userStable = new UserStable();
    userStable.setUserName("bob1234@gmail.com");
    userStable.setBrand("bma");
    userStable.setId("1234");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("chepstow");
    horseInfo.setHorseId("1234");
    horseInfo.setNote("wins every race");
    horseInfo.setNotesAvailable(true);
    horseInfo.setIsCrcHorse(true);
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-08-14T15:49:25.82"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();

    horseInfoList.add(horseInfo);

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStable getUserStableHorse() {
    UserStable userStable = new UserStable();
    userStable.setBrand("bma");
    userStable.setId("1234");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("1234");
    horseInfo.setIsCrcHorse(false);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();

    horseInfoList.add(horseInfo);

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStable getUserStableGTDesiredHorses() {
    UserStable userStable = new UserStable();
    userStable.setUserName("bob1234@gmail.com");
    userStable.setBrand("bma");
    userStable.setId("1234");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("chepstow");
    horseInfo.setHorseId("1234");
    horseInfo.setNote("wins every race");
    horseInfo.setNotesAvailable(true);
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-08-14T15:49:25.82"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    for (int i = 1; i <= 109; i++) {
      String name = "horse" + i;
      String id = "1" + i;
      LocalDateTime localDateTime = (LocalDateTime.parse("2023-08-14T15:49:25.82"));
      horseInfoList.add(new HorseInfo(id, name, "yes", true, localDateTime, true));
    }

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStable getUserStableNotesNull() {
    UserStable userStable = new UserStable();
    userStable.setUserName("bob1234@gmail.com");
    userStable.setBrand("bma");
    userStable.setId("123");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("chepstow");
    horseInfo.setHorseId("1234");
    horseInfo.setNote("");
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-08-14T15:49:25.82"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStable getUserStableDB() {
    UserStable userStable = new UserStable();
    userStable.setBrand("bma");
    userStable.setId("123");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("1234");
    horseInfo.setIsCrcHorse(false);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStable getUserStableInvalidId() {
    UserStable userStable = new UserStable();
    userStable.setBrand("bma");
    userStable.setId("123");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("abc");
    horseInfo.setIsCrcHorse(false);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStable getUserStableDBCheck() {
    UserStable userStable = new UserStable();
    userStable.setBrand("bma");
    userStable.setId("123");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("123");
    horseInfo.setIsCrcHorse(null);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);

    userStable.setMyStable(horseInfoList);
    return userStable;
  }

  private UserStableDto getUserStableDto() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("chepstow");
    horseInfo.setHorseId("1234");
    horseInfo.setNote("wins every race");
    horseInfo.setIsCrcHorse(true);
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-08-14T15:49:25.82"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStableDto getUserStableDtoObj() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("1234");
    horseInfo.setIsCrcHorse(true);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStableDto getUserStableInvalidIdDto() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("abc");
    horseInfo.setIsCrcHorse(true);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStableDto getUserStableDtoNullCheck() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("123");
    horseInfo.setIsCrcHorse(true);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStableDto getUserStableDtoHorse() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseId("1234");
    horseInfo.setIsCrcHorse(false);
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStableDto getUserStableDtoGTDesiredHorsesCount() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("chepstow");
    horseInfo.setHorseId("1234");
    horseInfo.setNote("wins every race");
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-08-14T15:49:25.82"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    for (int i = 1; i <= 109; i++) {
      String name = "horse" + i;
      String id = "1" + i;
      LocalDateTime localDateTime = (LocalDateTime.parse("2023-08-14T15:49:25.82"));
      horseInfoList.add(new HorseInfo(id, name, "yes", true, localDateTime, true));
    }

    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private UserStableDto getUserStableDtoNotesNull() {
    UserStableDto userStableDto = new UserStableDto();
    userStableDto.setBrand("bma");
    HorseInfo horseInfo = new HorseInfo();
    horseInfo.setHorseName("chepstow");
    horseInfo.setHorseId("1234");
    horseInfo.setNote("");
    horseInfo.setBookmarkedAt(LocalDateTime.parse("2023-08-14T15:49:25.82"));
    LinkedHashSet<HorseInfo> horseInfoList = new LinkedHashSet<>();
    horseInfoList.add(horseInfo);
    userStableDto.setMyStable(horseInfoList);
    return userStableDto;
  }

  private void setPrivateField(Object targetObject, String fieldName, Object newValue)
      throws NoSuchFieldException, IllegalAccessException {
    Field privateField = targetObject.getClass().getDeclaredField(fieldName);
    privateField.setAccessible(true);
    privateField.set(targetObject, newValue);
  }
}
