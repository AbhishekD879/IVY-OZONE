package com.entain.oxygen.service;

import static java.time.LocalDateTime.*;

import com.entain.oxygen.dto.SSResponseDto;
import com.entain.oxygen.entity.HorseInfo;
import com.entain.oxygen.entity.UserStable;
import com.entain.oxygen.exceptions.EntityNotFoundException;
import com.entain.oxygen.exceptions.UserStableException;
import com.entain.oxygen.repository.UserStableRepository;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.FindAndModifyOptions;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SignalType;
import reactor.util.function.Tuple2;
import reactor.util.function.Tuple3;

@Service
@Slf4j
@SuppressWarnings("java:S1200")
public class UserStableService extends AbstractService<UserStable> {

  @Value("${userStable.favHorsesLimit}")
  private int favHorsesLimit;

  private final UserStableRepository stableRepository;
  private final ReactiveMongoTemplate reactiveMongoTemplate;
  private final HorseRacingDataService horseRacingDataService;

  private static final String NO_STABLES_INFO = "There is no stabled info";
  public static final String DUPLICATE_ERROR_INFO = "Duplicate entry found..operation aborted";

  @Autowired
  public UserStableService(
      UserStableRepository stableRepository,
      ReactiveMongoTemplate reactiveMongoTemplate,
      HorseRacingDataService horseRacingDataService,
      ModelMapper modelMapper) {
    super(stableRepository);
    this.stableRepository = stableRepository;
    this.reactiveMongoTemplate = reactiveMongoTemplate;
    this.horseRacingDataService = horseRacingDataService;
  }

  public Mono<UserStable> getUserStableDataFromDb(Tuple2<String, String> tuple) {
    long startTime = System.currentTimeMillis();

    return stableRepository
        .findByUserNameAndBrandExcludingNotes(tuple.getT2())
        .switchIfEmpty(Mono.error(new EntityNotFoundException(NO_STABLES_INFO)))
        .doFinally(
            (SignalType signalType) -> {
              long endTime = System.currentTimeMillis();
              long duration = endTime - startTime;
              log.debug(
                  "GET CALL User stable data from db  : Time taken for getHorse (get call): {} ms",
                  duration);
            });
  }

  public Mono<UserStable> getHorseNotes(Tuple2<String, String> tuple) {
    long startTime = System.currentTimeMillis();

    return stableRepository
        .getNotesByHorseId(tuple.getT2(), tuple.getT1())
        .switchIfEmpty(Mono.error(new EntityNotFoundException(NO_STABLES_INFO)))
        .doFinally(
            (SignalType signalType) -> {
              long endTime = System.currentTimeMillis();
              long duration = endTime - startTime;
              log.debug(
                  "GET HORSE NOTES: Get User Horse Notes, Time taken for getNotes (get call): {} ms",
                  duration);
            });
  }

  public UserStable populateBookmarkTime(UserStable userStable) {
    LocalDateTime bookmarkTime = now(ZoneOffset.UTC);
    userStable.getMyStable().forEach(horseInfo -> horseInfo.setBookmarkedAt(bookmarkTime));
    return userStable;
  }

  public Mono<UserStable> updateHorseNotes(UserStable userStable) {
    long startTime = System.currentTimeMillis();

    HorseInfo horseInfo = userStable.getMyStable().stream().findFirst().orElse(new HorseInfo());

    Query query =
        new Query(
            Criteria.where("userName")
                .is(userStable.getUserName())
                .and("myStable.horseId")
                .is(horseInfo.getHorseId()));

    Update update = new Update();
    String notes = horseInfo.getNote().isEmpty() ? null : horseInfo.getNote();
    boolean notesIsAvailable = notes == null;
    update.set("myStable.$.note", notes);
    update.set("myStable.$.notesAvailable", !notesIsAvailable);

    FindAndModifyOptions options = FindAndModifyOptions.options().returnNew(true);

    return reactiveMongoTemplate
        .findAndModify(query, update, options, UserStable.class)
        .switchIfEmpty(Mono.error(() -> new EntityNotFoundException(NO_STABLES_INFO)))
        .doFinally(
            (SignalType signalType) -> {
              long endTime = System.currentTimeMillis();
              long duration = endTime - startTime;
              log.debug(
                  "PUT CALL : User Horse updated, Time taken for update is  (put call): {} ms",
                  duration);
            });
  }

  public Mono<UserStable> deleteByHorseId(Tuple3<String, Boolean, String> tuple) {
    long startTime = System.currentTimeMillis();

    Query query =
        new Query(
            Criteria.where("userName").is(tuple.getT3()).and("myStable.horseId").is(tuple.getT1()));

    Update update = new Update();
    update.pull("myStable", Query.query(Criteria.where("horseId").is(tuple.getT1())));

    boolean isCrc = tuple.getT2();

    if (isCrc) {
      update.push("unbookmarkedHorses", tuple.getT1());
    }

    FindAndModifyOptions options = FindAndModifyOptions.options().returnNew(true);

    return reactiveMongoTemplate
        .findAndModify(query, update, options, UserStable.class)
        .switchIfEmpty(Mono.error(() -> new EntityNotFoundException(NO_STABLES_INFO)))
        .doFinally(
            (SignalType signalType) -> {
              long endTime = System.currentTimeMillis();
              long duration = endTime - startTime;
              log.debug("DELETE CALL: Time taken for deleteHorse (delete call): {} ms", duration);
            });
  }

  public Mono<SSResponseDto> getCachesSSHorseEvents() {
    long startTime = System.currentTimeMillis();

    return Mono.fromSupplier(
            () -> {
              SSResponseDto ssResponseDto = new SSResponseDto();
              ssResponseDto.setChildren(horseRacingDataService.getCachedHorseData());
              return ssResponseDto;
            })
        .doFinally(
            (SignalType signalType) -> {
              long endTime = System.currentTimeMillis();
              long duration = endTime - startTime;
              log.debug("CACHE CALL: Time taken for cached data (cache call): {} ms", duration);
            });
  }

  public Mono<UserStable> saveUserStable(UserStable userStable) {
    long startTime = System.currentTimeMillis();

    Mono<UserStable> userStableMono = stableRepository.findByUserName(userStable.getUserName());

    return userStableMono
        .flatMap(
            (UserStable stable) -> {
              Set<HorseInfo> horseInfoList = stable.getMyStable();

              try {
                horseInfoList = validateAddAndUpdateHorses(horseInfoList, userStable.getMyStable());
              } catch (Exception ex) {
                return Mono.error(
                    new UserStableException(DUPLICATE_ERROR_INFO, HttpStatus.CONFLICT.value()));
              }

              if (horseInfoList.size() > favHorsesLimit)
                return Mono.error(
                    new UserStableException(
                        "MAX HORSES REACHED", HttpStatus.INTERNAL_SERVER_ERROR.value()));
              stable.setMyStable((LinkedHashSet<HorseInfo>) horseInfoList);
              return super.save(stable);
            })
        .switchIfEmpty(
            Mono.defer(
                () -> {
                  if (userStable.getMyStable().size() > favHorsesLimit)
                    return Mono.error(
                        new UserStableException(
                            "MAX HORSES REACHED", HttpStatus.INTERNAL_SERVER_ERROR.value()));

                  return super.save(userStable);
                }))
        .doFinally(
            (SignalType signalType) -> {
              long endTime = System.currentTimeMillis();
              long duration = endTime - startTime;
              log.debug(
                  "POST CALL : User horse added Time taken for addHorse (post call): {} ms",
                  duration);
            });
  }

  private Set<HorseInfo> validateAddAndUpdateHorses(
      Set<HorseInfo> horseInfoList, Set<HorseInfo> newHorses) {

    Map<String, HorseInfo> newHorseMap =
        newHorses.stream().collect(Collectors.toMap(HorseInfo::getHorseId, Function.identity()));

    LinkedHashSet<HorseInfo> updatedHorseInfoList =
        horseInfoList.stream()
            .map(
                (HorseInfo existingHorse) -> {
                  if (newHorseMap.containsKey(existingHorse.getHorseId())) {
                    HorseInfo newHorse = newHorseMap.get(existingHorse.getHorseId());
                    if (newHorse.getIsCrcHorse() != null && newHorse.getIsCrcHorse()) {
                      if (existingHorse.getIsCrcHorse() != null
                          && existingHorse.getIsCrcHorse().equals(newHorse.getIsCrcHorse()))
                        return Mono.error(
                            new UserStableException(
                                DUPLICATE_ERROR_INFO, HttpStatus.CONFLICT.value()));
                      existingHorse.setIsCrcHorse(newHorse.getIsCrcHorse());
                      existingHorse.setBookmarkedAt(newHorse.getBookmarkedAt());
                    } else {
                      return Mono.error(
                          new UserStableException(
                              DUPLICATE_ERROR_INFO, HttpStatus.CONFLICT.value()));
                    }
                  }
                  return existingHorse;
                })
            .map(ob -> (HorseInfo) ob)
            .collect(Collectors.toCollection(LinkedHashSet::new));

    for (HorseInfo newHorse : newHorses) {
      if (!updatedHorseInfoList.contains(newHorse)) updatedHorseInfoList.add(newHorse);
    }

    return updatedHorseInfoList;
  }
}
