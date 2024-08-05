package com.entain.oxygen.handler;

import com.entain.oxygen.entity.HorseInfo;
import com.entain.oxygen.entity.UserStable;
import com.entain.oxygen.exceptions.EntityNotFoundException;
import com.entain.oxygen.exceptions.ValidationsException;
import com.entain.oxygen.model.UserStableDto;
import com.entain.oxygen.router.StableFacadeHandler;
import com.entain.oxygen.service.CommonService;
import com.entain.oxygen.service.UserStableService;
import com.entain.oxygen.util.RequestContextHolderUtils;
import com.entain.oxygen.util.Validations;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Optional;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;
import reactor.util.function.Tuple2;
import reactor.util.function.Tuple3;
import reactor.util.function.Tuples;

@Component
@AllArgsConstructor
@Slf4j
public class UserStableHandler extends CommonService implements StableFacadeHandler {

  private final UserStableService userStableService;
  private final ModelMapper modelMapper;
  private static final String BRAND = "brand";

  @Override
  public Mono<ServerResponse> saveOperation(ServerRequest request) {
    return request
        .bodyToMono(UserStableDto.class)
        .flatMap(Validations::checkIfValidHorseIdAndBrand)
        .handle(
            (UserStableDto dto, SynchronousSink<Tuple2<UserStableDto, String>> sink) -> {
              try {
                sink.next(
                    Tuples.of(
                        dto, RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .map(
            (Tuple2<UserStableDto, String> tuples) -> {
              UserStableDto dto = tuples.getT1();
              UserStable userStable = modelMapper.map(dto, UserStable.class);
              userStable.setUserName(tuples.getT2());
              return userStableService.populateBookmarkTime(userStable);
            })
        .flatMap(userStableService::saveUserStable)
        .map(userStable -> modelMapper.map(userStable, UserStableDto.class))
        .flatMap(userStable -> this.success(userStable, false))
        .onErrorResume(this::errorWithSpecificHttpStatus);
  }

  @Override
  public Mono<ServerResponse> getOperation(ServerRequest request) {
    String brand = request.pathVariable(BRAND);
    log.info("UserPreferenceHandler:: In Get Operation ");

    return Mono.justOrEmpty(request.pathVariable(BRAND))
        .handle(
            (String brandInput, SynchronousSink<Tuple2<String, String>> sink) -> {
              try {
                sink.next(
                    Tuples.of(
                        brandInput,
                        RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .flatMap(this.userStableService::getUserStableDataFromDb)
        .map(userStable -> modelMapper.map(userStable, UserStableDto.class))
        .flatMap(userStable -> this.success(userStable, false))
        .onErrorResume(
            (Throwable exception) -> {
              if (exception instanceof ValidationsException ve) {
                return this.errorWithSpecificHttpStatus(ve);
              } else {
                UserStableDto userStableDto =
                    UserStableDto.builder().brand(brand).myStable(new LinkedHashSet<>()).build();
                return this.success(userStableDto, false, HttpStatus.OK);
              }
            });
  }

  @Override
  public Mono<ServerResponse> updateOperation(ServerRequest request) {

    return request
        .bodyToMono(UserStableDto.class)
        .flatMap(Validations::validateAndSanitize)
        .handle(
            (UserStableDto dto, SynchronousSink<Tuple2<UserStableDto, String>> sink) -> {
              try {
                sink.next(
                    Tuples.of(
                        dto, RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .flatMap(
            (Tuple2<UserStableDto, String> tuples) -> {
              UserStableDto dto = tuples.getT1();
              UserStable userStable = modelMapper.map(dto, UserStable.class);
              userStable.setUserName(tuples.getT2());
              return this.userStableService.updateHorseNotes(userStable);
            })
        .map(updatedUserStable -> modelMapper.map(updatedUserStable, UserStableDto.class))
        .flatMap(userStableDto -> this.success(userStableDto, false))
        .onErrorResume(this::errorWithSpecificHttpStatus);
  }

  @Override
  public Mono<ServerResponse> deleteOperation(ServerRequest request) {

    String horseId = request.pathVariable("horseId");
    Optional<String> crcHorse = request.queryParam("isCrcHorse");
    boolean isCrcHorse = crcHorse.map(Boolean::parseBoolean).orElse(false);

    return Mono.justOrEmpty(horseId)
        .flatMap(Validations::validateHorseId)
        .handle(
            (String hid, SynchronousSink<Tuple3<String, Boolean, String>> sink) -> {
              try {
                sink.next(
                    Tuples.of(
                        hid,
                        isCrcHorse,
                        RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .flatMap(this.userStableService::deleteByHorseId)
        .map(userStable -> modelMapper.map(userStable, UserStableDto.class))
        .flatMap(userStable -> this.success(userStable, false))
        .onErrorResume(this::errorWithSpecificHttpStatus);
  }

  @Override
  public Mono<ServerResponse> getHorseNotesById(ServerRequest request) {

    String horseId = request.pathVariable("horseId");

    return Mono.justOrEmpty(horseId)
        .flatMap(Validations::validateHorseId)
        .handle(
            (String inputData, SynchronousSink<Tuple2<String, String>> sink) -> {
              try {
                sink.next(
                    Tuples.of(
                        inputData,
                        RequestContextHolderUtils.getSportsBookUser(sink.contextView())));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .flatMap(this.userStableService::getHorseNotes)
        .map(
            userStable ->
                userStable.getMyStable().stream().map(HorseInfo::getNote).findFirst().orElse(""))
        .flatMap(notes -> this.success(notes, false))
        .onErrorResume(
            (Throwable exception) -> {
              if (exception instanceof ValidationsException
                  || exception instanceof EntityNotFoundException)
                return this.errorWithSpecificHttpStatus(exception);

              return this.success("", false, HttpStatus.OK);
            });
  }

  @Override
  public Mono<ServerResponse> getCachedHorseInfo(ServerRequest request) {

    return userStableService
        .getCachesSSHorseEvents()
        .flatMap(events -> this.success(events, false))
        .onErrorResume(error -> this.success(List.of(), false, HttpStatus.NO_CONTENT));
  }
}
