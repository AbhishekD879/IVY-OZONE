package com.entain.oxygen.service;

import com.entain.oxygen.entity.UserPreference;
import com.entain.oxygen.exceptions.EntityNotFoundException;
import com.entain.oxygen.exceptions.OddPreferenceDuplicateException;
import com.entain.oxygen.model.PreferenceDto;
import com.entain.oxygen.repository.UserPreferenceRepository;
import com.entain.oxygen.util.Preference;
import com.github.benmanes.caffeine.cache.AsyncLoadingCache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;
import reactor.util.function.Tuple2;

@Service
@Slf4j
public class UserPreferenceService extends AbstractService<UserPreference> {

  private static final String ODDS_PREFERENCES = "oddPreference";
  private final UserPreferenceRepository userPreferenceRepository;
  private final int ttl;
  private final int maxSize;

  @Autowired
  public UserPreferenceService(
      UserPreferenceRepository userPreferenceRepository,
      @Value("${cache.ttl}") int ttl,
      @Value("${cache.size}") int maxSize) {
    super(userPreferenceRepository);
    this.userPreferenceRepository = userPreferenceRepository;
    this.ttl = ttl;
    this.maxSize = maxSize;
  }

  public Mono<UserPreference> saveUserPreference(UserPreference userPreference) {
    return super.save(userPreference);
  }

  public Mono<UserPreference> findUserPreferenceByUserNameAndBrand(String userName, String brand) {
    String cacheKey = userName + "::" + brand;
    AsyncLoadingCache<String, UserPreference> cache =
        Caffeine.newBuilder()
            .expireAfterWrite(Duration.ofSeconds(ttl))
            .maximumSize(maxSize)
            .buildAsync(
                (key, executor) ->
                    this.userPreferenceRepository
                        .findByUserNameAndBrand(userName, brand)
                        .toFuture());
    return Mono.fromCompletionStage(cache.get(cacheKey));
  }

  public Flux<UserPreference> findAllPreferences() {
    return super.findAll()
        .switchIfEmpty(
            Flux.defer(() -> Flux.error(new EntityNotFoundException("No records available"))));
  }

  public Flux<UserPreference> findAllByBrand(String brand) {
    return this.userPreferenceRepository
        .findAllByBrand(brand)
        .switchIfEmpty(
            Flux.defer(() -> Flux.error(new EntityNotFoundException("No records available"))));
  }

  public Mono<UserPreference> deletePreference(UserPreference entity) {
    return this.userPreferenceRepository.delete(entity).then(Mono.just(entity));
  }

  public Mono<UserPreference> validatePreference(Tuple2<PreferenceDto, String> tuple) {
    log.debug("mapping user preference for post service");
    PreferenceDto dto = tuple.getT1();
    return this.findUserPreferenceByUserNameAndBrand(tuple.getT2(), dto.getBrand())
        .filter(Objects::nonNull)
        .flatMap(
            userPreference ->
                Mono.error(new OddPreferenceDuplicateException("Odds preference already exists")))
        .switchIfEmpty(
            Mono.defer(
                () ->
                    Mono.just(
                        createUserPreference(
                            tuple.getT2(), dto.getBrand(), dto.getOddPreference(), false))))
        .map(UserPreference.class::cast);
  }

  public Mono<UserPreference> validateAndMapUpdatedPreference(Tuple2<PreferenceDto, String> tuple) {
    log.debug("validating the PUT request");
    PreferenceDto dto = tuple.getT1();
    return this.findUserPreferenceByUserNameAndBrand(tuple.getT2(), dto.getBrand())
        .handle(
            (UserPreference userPreference, SynchronousSink<UserPreference> sink) -> {
              try {
                if (userPreference
                    .getPreferences()
                    .get(ODDS_PREFERENCES)
                    .toString()
                    .equalsIgnoreCase(dto.getOddPreference())) {
                  throw new OddPreferenceDuplicateException(
                      "no need to update :: entity has same odds preference");
                }
                sink.next(userPreference);
              } catch (OddPreferenceDuplicateException ex) {
                sink.error(ex);
              }
            })
        .map(
            (UserPreference userPreference) -> {
              userPreference.getPreferences().put(ODDS_PREFERENCES, dto.getOddPreference());
              return userPreference;
            })
        .switchIfEmpty(
            Mono.defer(
                () ->
                    Mono.just(
                        createUserPreference(
                            tuple.getT2(), dto.getBrand(), dto.getOddPreference(), false))));
  }

  public Mono<UserPreference> findUserPreferenceIfPresent(Tuple2<String, String> tuple) {
    return this.userPreferenceRepository
        .findByUserNameAndBrand(tuple.getT2(), tuple.getT1())
        .switchIfEmpty(
            Mono.defer(() -> Mono.error(new EntityNotFoundException("preference not found"))));
  }

  // default preference set as fractional
  private UserPreference createUserPreference(
      String userName, String brand, String oddsPreference, boolean defaultFlag) {
    String preferenceKey = ODDS_PREFERENCES;
    Map<Object, Object> preferences = new HashMap<>();
    if (defaultFlag) {
      preferences.put(preferenceKey, Preference.FRACTIONAL.value());
    } else {
      preferences.put(preferenceKey, oddsPreference);
    }
    UserPreference userPreference = new UserPreference();
    userPreference.setUserName(userName);
    userPreference.setBrand(brand);
    userPreference.setPreferences(preferences);
    return userPreference;
  }

  public Mono<UserPreference> getUserPreferenceByBrandAndUserName(Tuple2<String, String> tuple) {
    return this.userPreferenceRepository
        .findByUserNameAndBrand(tuple.getT2(), tuple.getT1())
        .switchIfEmpty(
            Mono.defer(
                () -> Mono.just(createUserPreference(tuple.getT2(), tuple.getT1(), "", true))));
  }
}
