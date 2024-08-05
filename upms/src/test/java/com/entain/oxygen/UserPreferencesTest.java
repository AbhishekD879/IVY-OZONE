package com.entain.oxygen;

import com.entain.oxygen.bpp.BppConfigLightProps;
import com.entain.oxygen.bpp.BppConfiguration;
import com.entain.oxygen.entity.UserPreference;
import com.entain.oxygen.exceptions.UserNotFoundException;
import com.entain.oxygen.filter.PreferenceFilter;
import com.entain.oxygen.handler.UserPreferenceHandler;
import com.entain.oxygen.repository.UserPreferenceRepository;
import com.entain.oxygen.router.OptionsHandler;
import com.entain.oxygen.router.UserPreferenceRouter;
import com.entain.oxygen.service.BppService;
import com.entain.oxygen.service.UserPreferenceService;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@ExtendWith(SpringExtension.class)
@WebFluxTest(
    value = {
      UserPreferenceRouter.class,
      UserPreferenceHandler.class,
      UserPreferenceService.class,
      BppConfigLightProps.class,
      OptionsHandler.class,
      PreferenceFilter.class,
    })
@MockBeans({@MockBean(CorsEndpointProperties.class)})
@Import(value = {BppConfiguration.class})
class UserPreferencesTest extends AbstractControllerTest {

  private static final String routePath = "/oddsPreference";

  @MockBean private BppService bppService;

  @MockBean private UserPreferenceRepository repository;

  @Test
  void testTokenWithNull() {

    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .exchange()
        .expectStatus()
        .isBadRequest()
        .expectBody(String.class)
        .isEqualTo("Token Required");
  }

  @Test
  void testTokenWithEmpty() {
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "")
        .exchange()
        .expectStatus()
        .isBadRequest()
        .expectBody(String.class)
        .isEqualTo("Token Required");
  }

  @Test
  void testTokenInvalid() {
    Mockito.when(bppService.favUserdata(Mockito.anyString()))
        .thenReturn(
            Mono.error(new UserNotFoundException("failed to get resp from BPP :: User not Found")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "ddfseref")
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody(String.class)
        .isEqualTo("failed to get resp from BPP :: User not Found");
  }

  @Test
  void testEmptyBrand() {
    mockUserName();
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_empty_brand.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("brand is invalid., refer valid brands->[bma, ladbrokes, connect, retail]");
  }

  @Test
  void testInvalidBrand() {
    mockUserName();
    this.webTestClient
        .post()
        .uri(routePath)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_invalid_brand.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("brand is invalid., refer valid brands->[bma, ladbrokes, connect, retail]");
  }

  @Test
  void testEmptyOddsPreference() {
    mockUserName();
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .header("token", "friure")
        .bodyValue(getResourceByPath("userPreference/request_empty_odd.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("odds preference is invalid., refer valid preferences->[frac, dec, ame]");
  }

  @Test
  void testInvalidOddsPreference() {
    mockUserName();
    this.webTestClient
        .post()
        .uri(routePath)
        .header("token", "friure")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_invalid_odd.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("odds preference is invalid., refer valid preferences->[frac, dec, ame]");
  }

  @Test
  void testBppUnauthorizedException() {

    Mockito.when(bppService.favUserdata(Mockito.any(String.class)))
        .thenReturn(
            Mono.error(new UserNotFoundException("failed to get resp from BPP :: User not Found")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "123x==")
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody(String.class)
        .isEqualTo("failed to get resp from BPP :: User not Found");
  }

  @Test
  void testBppConnectionException() {
    Mockito.when(bppService.favUserdata(Mockito.any(String.class)))
        .thenReturn(
            Mono.error(new UserNotFoundException("failed to get resp from BPP :: User not Found")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "123x==")
        .exchange()
        .expectStatus()
        .is5xxServerError();
  }

  @Test
  void testBppUnknownException() {
    Mockito.when(bppService.favUserdata(Mockito.any(String.class)))
        .thenReturn(Mono.error(new UserNotFoundException("no user in context")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "123x==")
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody(String.class)
        .isEqualTo("no user in context");
  }

  @Test
  void testSaveUserPreference() {
    mockUserName();
    Mockito.when(
            repository.findByUserNameAndBrand(Mockito.any(String.class), Mockito.any(String.class)))
        .thenReturn(Mono.empty());
    Mockito.when(repository.save(Mockito.any(UserPreference.class)))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "123xe==")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .json(getResourceByPath("userPreference/response.json"));
  }

  @Test
  void testSavePreferenceDuplicate() {
    mockUserName();
    Mockito.when(
            repository.findByUserNameAndBrand(Mockito.any(String.class), Mockito.any(String.class)))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "123xe==")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody(String.class)
        .isEqualTo("Odds preference already exists");
  }

  @Test
  void testSavePreferenceForCommonError() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.error(new Exception("internal server error")));
    this.webTestClient
        .post()
        .uri(routePath)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .header("token", "123xe==")
        .exchange()
        .expectStatus()
        .is5xxServerError();
  }

  @Test
  void testGetOperationForNoToken() {
    this.webTestClient
        .get()
        .uri(uriBuilder -> uriBuilder.path(routePath).pathSegment("bma").build())
        .header("token", "")
        .exchange()
        .expectStatus()
        .isBadRequest()
        .expectBody(String.class)
        .isEqualTo("Token Required");
  }

  @Test
  void testGetOperationWithInvalidBrand() {
    mockUserName();
    this.webTestClient
        .get()
        .uri(uriBuilder -> uriBuilder.path(routePath).pathSegment("bn").build())
        .header("token", "dkerie")
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("brand is invalid., refer valid brands->[bma, ladbrokes, connect, retail]");
  }

  @Test
  void testGetOperation() {
    mockUserName();
    Mockito.when(this.repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));

    this.webTestClient
        .get()
        .uri(uriBuilder -> uriBuilder.path(routePath).pathSegment("bma").build())
        .header("token", "123x==")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .json(getResourceByPath("userPreference/response.json"));
  }

  @Test
  void testGetOperationWithEmptyEntity() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.empty());
    this.webTestClient
        .get()
        .uri(uriBuilder -> uriBuilder.path(routePath).pathSegment("bma").build())
        .header("token", "1234X=")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .json(getResourceByPath("userPreference/response_default.json"));
  }

  @Test
  void testGetOperationByBrand() {
    Mockito.when(repository.findAllByBrand(Mockito.anyString()))
        .thenReturn(Flux.just(createUserPreference("bma", "frac")));
    this.webTestClient
        .get()
        .uri(routePath + "/preferences/brand/bma")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .json(getResourceByPath("userPreference/response_flux.json"));
  }

  @Test
  void testGetOperationByBrandNoEntity() {
    Mockito.when(repository.findAllByBrand(Mockito.anyString())).thenReturn(Flux.empty());
    this.webTestClient
        .get()
        .uri(routePath + "/preferences/brand/bma")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody(String.class)
        .isEqualTo("No records available");
  }

  @Test
  void testGetAllOperation() {
    Mockito.when(repository.findAll()).thenReturn(Flux.just(createUserPreference("bma", "frac")));
    this.webTestClient
        .get()
        .uri(routePath)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .json(getResourceByPath("userPreference/response_flux.json"));
  }

  @Test
  void testGetAllOperationNoEntity() {
    Mockito.when(repository.findAll()).thenReturn(Flux.empty());
    this.webTestClient
        .get()
        .uri(routePath)
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody(String.class)
        .isEqualTo("No records available");
  }

  @Test
  void testUpdatePreferenceEmptyOdds() {
    mockUserName();
    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "friure")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_empty_odd.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("odds preference is invalid., refer valid preferences->[frac, dec, ame]");
  }

  @Test
  void testUpdatePreferenceInvalidOdds() {
    mockUserName();
    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "friure")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_invalid_odd.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("odds preference is invalid., refer valid preferences->[frac, dec, ame]");
  }

  @Test
  void testUpdateUserPreferenceEmptyBrand() {
    mockUserName();
    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_empty_brand.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("brand is invalid., refer valid brands->[bma, ladbrokes, connect, retail]");
  }

  @Test
  void testUpdateUserPreferenceInvalidBrand() {
    mockUserName();
    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request_invalid_brand.json"))
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("brand is invalid., refer valid brands->[bma, ladbrokes, connect, retail]");
  }

  @Test
  void testUpdatePreference() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.just(createUserPreference("bma", "ame")));
    Mockito.when(repository.save(Mockito.any(UserPreference.class)))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));

    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .json(getResourceByPath("userPreference/response.json"));
  }

  @Test
  void testUpdatePreferenceWithDuplicate() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));

    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody(String.class)
        .isEqualTo("no need to update :: entity has same odds preference");
  }

  @Test
  void testUpdatePreferenceWithEmptyRecord() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.empty());
    Mockito.when(repository.save(Mockito.any(UserPreference.class)))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));

    this.webTestClient
        .put()
        .uri(routePath)
        .header("token", "dheiuenfue")
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(getResourceByPath("userPreference/request.json"))
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void testDeletePreference() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.just(createUserPreference("bma", "frac")));
    Mockito.when(repository.delete(Mockito.any())).thenReturn(Mono.empty());
    this.webTestClient
        .delete()
        .uri(routePath + "/bma")
        .header("token", "derer")
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void testDeletePreferenceWithInvalidBrand() {
    mockUserName();

    this.webTestClient
        .delete()
        .uri(uriBuilder -> uriBuilder.path(routePath).pathSegment("bm").build())
        .header("token", "3232cd")
        .exchange()
        .expectStatus()
        .is4xxClientError()
        .expectBody(String.class)
        .isEqualTo("brand is invalid., refer valid brands->[bma, ladbrokes, connect, retail]");
  }

  @Test
  void testDeletePreferenceWithEmptyBody() {
    mockUserName();
    Mockito.when(repository.findByUserNameAndBrand(Mockito.anyString(), Mockito.anyString()))
        .thenReturn(Mono.empty());

    this.webTestClient
        .delete()
        .uri(routePath + "/bma")
        .header("token", "dferere")
        .exchange()
        .expectStatus()
        .is2xxSuccessful()
        .expectBody(String.class)
        .isEqualTo("preference not found");
  }

  private void mockUserName() {
    Mockito.when(bppService.favUserdata(Mockito.any(String.class))).thenReturn(Mono.just("test"));
  }

  private UserPreference createUserPreference(String brand, String odds) {
    Map<Object, Object> map = new HashMap<>();
    map.put("oddPreference", odds);
    UserPreference userPreference = new UserPreference();
    userPreference.setId("123");
    userPreference.setUserName("test");
    userPreference.setBrand(brand);
    userPreference.setPreferences(map);
    return userPreference;
  }
}
