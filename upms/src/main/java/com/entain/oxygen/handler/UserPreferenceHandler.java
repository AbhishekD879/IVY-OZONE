package com.entain.oxygen.handler;

import com.entain.oxygen.entity.UserPreference;
import com.entain.oxygen.exceptions.PreferenceDtoException;
import com.entain.oxygen.exceptions.UserNotFoundException;
import com.entain.oxygen.model.PreferenceDto;
import com.entain.oxygen.router.PreferenceFacadeHandler;
import com.entain.oxygen.service.CommonService;
import com.entain.oxygen.service.UserPreferenceService;
import com.entain.oxygen.util.RequestContextHolderUtils;
import com.entain.oxygen.util.Validations;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;
import reactor.util.function.Tuple2;
import reactor.util.function.Tuples;

@Component
@Qualifier("userPreferenceHandler")
@RequiredArgsConstructor
@Slf4j
public class UserPreferenceHandler extends CommonService implements PreferenceFacadeHandler {

  private static final String BRAND = "brand";
  private final UserPreferenceService userPreferenceService;

  @Override
  public Mono<ServerResponse> saveOperation(ServerRequest request) {
    log.info("UserPreferenceHandler:: In POST operation");
    return request
        .bodyToMono(PreferenceDto.class)
        .handle(
            (PreferenceDto dto, SynchronousSink<Tuple2<PreferenceDto, String>> sink) -> {
              try {
                Validations.validateBrandAndOdds(dto);
                sink.next(
                    Tuples.of(
                        dto, RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (PreferenceDtoException | UserNotFoundException ex) {
                sink.error(ex);
              }
            })
        .flatMap(userPreferenceService::validatePreference)
        .flatMap(userPreferenceService::saveUserPreference)
        .flatMap(pref -> this.success(pref, true))
        .onErrorResume(this::error);
  }

  @Override
  public Mono<ServerResponse> getOperation(ServerRequest request) {
    log.info("UserPreferenceHandler:: In Get Operation ");

    return Mono.justOrEmpty(request.pathVariable(BRAND))
        .handle(
            (String brand, SynchronousSink<Tuple2<String, String>> sink) -> {
              try {
                Validations.validateBrand(brand);
                sink.next(
                    Tuples.of(
                        brand, RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (PreferenceDtoException | UserNotFoundException ex) {
                sink.error(ex);
              }
            })
        .flatMap(this.userPreferenceService::getUserPreferenceByBrandAndUserName)
        .flatMap(pref -> this.success(pref, true))
        .onErrorResume(this::error);
  }

  @Override
  public Mono<ServerResponse> getAllOddsPreferencesByBrand(ServerRequest request) {
    log.info("UserPreferenceHandler:: In GetAllByBrand Operation");
    Flux<UserPreference> userPreferenceFlux =
        this.userPreferenceService.findAllByBrand(request.pathVariable(BRAND));
    return doGetAll(userPreferenceFlux);
  }

  @Override
  public Mono<ServerResponse> getAllOddsPreference(ServerRequest request) {
    log.info("UserPreferenceHandler:: In GetAll Operation");
    Flux<UserPreference> userPreferenceFlux = this.userPreferenceService.findAllPreferences();
    return doGetAll(userPreferenceFlux);
  }

  @Override
  public Mono<ServerResponse> updateOperation(ServerRequest request) {
    log.info("UserPreferenceHandler:: In UPDATE Operation");
    return request
        .bodyToMono(PreferenceDto.class)
        .handle(
            (PreferenceDto dto, SynchronousSink<Tuple2<PreferenceDto, String>> sink) -> {
              try {
                Validations.validateBrandAndOdds(dto);
                sink.next(
                    Tuples.of(
                        dto, RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (PreferenceDtoException | UserNotFoundException ex) {
                sink.error(ex);
              }
            })
        .flatMap(userPreferenceService::validateAndMapUpdatedPreference)
        .flatMap(userPreferenceService::saveUserPreference)
        .flatMap(pref -> this.success(pref, true))
        .onErrorResume(this::error);
  }

  @Override
  public Mono<ServerResponse> deleteOperation(ServerRequest request) {
    log.info("UserPreferenceHandler:: In Delete Operation");
    return Mono.justOrEmpty(request.pathVariable(BRAND))
        .handle(
            (String brand, SynchronousSink<Tuple2<String, String>> sink) -> {
              try {
                Validations.validateBrand(brand);
                sink.next(
                    Tuples.of(
                        brand, RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (PreferenceDtoException | UserNotFoundException ex) {
                sink.error(ex);
              }
            })
        .flatMap(this.userPreferenceService::findUserPreferenceIfPresent)
        .flatMap(this.userPreferenceService::deletePreference)
        .flatMap(pref -> this.success(pref, true))
        .onErrorResume(this::error);
  }

  private Mono<ServerResponse> doGetAll(Flux<UserPreference> result) {
    return result
        .collectList()
        .flatMap(pref -> this.success(pref, true))
        .onErrorResume(this::error);
  }
}
